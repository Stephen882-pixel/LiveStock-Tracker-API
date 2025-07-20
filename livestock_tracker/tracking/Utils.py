from django.contrib.gis.geos import  Point
from django.contrib.gis.db.models.functions import Distance
from django.utils import timezone
from datetime import timedelta
import logging

from .models import (
    GrazingZone, AnimalLocation, GeofenceEvent,
    AnimalGrazingAssignment, NotificationContact
)
from .notifications import send_geofence_notification

logger = logging.getLogger(__name__)


def check_geofence_status(location_record):
    """
    Check if an animal location is within assigned grazing zones
    and generate geofence events if necessary
    """
    try:
        animal = location_record.animal
        current_point = location_record.location

        # Get active zones assigned to this animal
        assigned_zones = GrazingZone.objects.filter(
            animal_assignments__animal=animal,
            animal_assignments__is_active=True,
            is_active=True
        )

        # Check which assigned zones contain the current location
        zones_containing_animal = []
        for zone in assigned_zones:
            if zone.boundary.contains(current_point):
                # Check time-based restrictions if they exist
                if is_within_access_hours(zone):
                    zones_containing_animal.append(zone)

        # Update location record with current zones
        location_record.inside_zones.set(zones_containing_animal)
        location_record.is_within_boundary = len(zones_containing_animal) > 0
        location_record.save()

        # Process geofence events
        process_geofence_events(location_record, zones_containing_animal, assigned_zones)

        logger.info(f"Processed geofence check for {animal.tag_id}: "
                    f"In {len(zones_containing_animal)} of {assigned_zones.count()} zones")

    except Exception as e:
        logger.error(f"Error processing geofence for location {location_record.id}: {str(e)}")


def is_within_access_hours(zone):
    """Check if current time is within zone access hours"""
    if not zone.access_start_time or not zone.access_end_time:
        return True  # No time restrictions

    current_time = timezone.now().time()

    # Handle overnight periods (e.g., 22:00 - 06:00)
    if zone.access_start_time > zone.access_end_time:
        return current_time >= zone.access_start_time or current_time <= zone.access_end_time
    else:
        return zone.access_start_time <= current_time <= zone.access_end_time


def process_geofence_events(location_record, current_zones, assigned_zones):
    """Process and create geofence events based on zone status changes"""
    animal = location_record.animal

    # Get the previous location to compare zone status
    previous_location = AnimalLocation.objects.filter(
        animal=animal,
        recorded_at__lt=location_record.recorded_at
    ).order_by('-recorded_at').first()

    if previous_location:
        previous_zones = set(previous_location.inside_zones.all())
    else:
        previous_zones = set()

    current_zones_set = set(current_zones)

    # Detect zone entries
    entered_zones = current_zones_set - previous_zones
    for zone in entered_zones:
        create_geofence_event(
            animal=animal,
            zone=zone,
            location_record=location_record,
            event_type='entry',
            severity=determine_event_severity(zone, 'entry')
        )

    # Detect zone exits
    exited_zones = previous_zones - current_zones_set
    for zone in exited_zones:
        create_geofence_event(
            animal=animal,
            zone=zone,
            location_record=location_record,
            event_type='exit',
            severity=determine_event_severity(zone, 'exit')
        )

    # Check for boundary violations (animal outside all assigned zones)
    if assigned_zones.exists() and not current_zones:
        # Check if this is a new violation or continuing one
        recent_violation = GeofenceEvent.objects.filter(
            animal=animal,
            event_type__in=['violation', 'timeout'],
            created_at__gte=timezone.now() - timedelta(minutes=30)
        ).exists()

        if not recent_violation:
            create_geofence_event(
                animal=animal,
                zone=None,
                location_record=location_record,
                event_type='violation',
                severity='high',
                distance_from_boundary=calculate_distance_from_nearest_zone(
                    location_record.location, assigned_zones
                )
            )

    # Check for extended time outside zones
    check_extended_outside_time(animal, location_record, assigned_zones, current_zones)


def create_geofence_event(animal, zone, location_record, event_type, severity='medium',
                          distance_from_boundary=None, duration_outside=None):
    """Create a geofence event and trigger notifications"""
    try:
        event = GeofenceEvent.objects.create(
            animal=animal,
            zone=zone,
            location_record=location_record,
            event_type=event_type,
            severity=severity,
            distance_from_boundary=distance_from_boundary,
            duration_outside=duration_outside
        )

        # Trigger notifications for high severity events
        if severity in ['high', 'critical']:
            send_geofence_notification(event)

        logger.info(f"Created geofence event: {animal.tag_id} - {event_type} - {severity}")
        return event

    except Exception as e:
        logger.error(f"Error creating geofence event: {str(e)}")
        return None


def determine_event_severity(zone, event_type):
    """Determine the severity level of a geofence event"""
    if not zone:
        return 'high'  # Boundary violation without specific zone

    severity_map = {
        'restricted': {
            'entry': 'critical',
            'exit': 'low'
        },
        'quarantine': {
            'entry': 'medium',
            'exit': 'critical'
        },
        'grazing': {
            'entry': 'low',
            'exit': 'medium'
        },
        'watering': {
            'entry': 'low',
            'exit': 'low'
        },
        'shelter': {
            'entry': 'low',
            'exit': 'low'
        }
    }

    return severity_map.get(zone.zone_type, {}).get(event_type, 'medium')


def calculate_distance_from_nearest_zone(point, zones):
    """Calculate distance from a point to the nearest zone boundary"""
    try:
        min_distance = None
        for zone in zones:
            distance = zone.boundary.distance(point)
            if min_distance is None or distance < min_distance:
                min_distance = distance

        # Convert from degrees to meters (approximate)
        if min_distance is not None:
            return min_distance * 111000  # Rough conversion from degrees to meters

        return None
    except Exception as e:
        logger.error(f"Error calculating distance from zones: {str(e)}")
        return None


def check_extended_outside_time(animal, current_location, assigned_zones, current_zones):
    """Check if animal has been outside assigned zones for extended period"""
    if assigned_zones.exists() and not current_zones:
        # Find the last time animal was in any assigned zone
        last_inside = AnimalLocation.objects.filter(
            animal=animal,
            inside_zones__in=assigned_zones,
            recorded_at__lt=current_location.recorded_at
        ).order_by('-recorded_at').first()

        if last_inside:
            time_outside = current_location.recorded_at - last_inside.recorded_at

            # Create timeout event if outside for more than 2 hours
            if time_outside > timedelta(hours=2):
                # Check if we already created a timeout event recently
                recent_timeout = GeofenceEvent.objects.filter(
                    animal=animal,
                    event_type='timeout',
                    created_at__gte=timezone.now() - timedelta(hours=1)
                ).exists()

                if not recent_timeout:
                    create_geofence_event(
                        animal=animal,
                        zone=None,
                        location_record=current_location,
                        event_type='timeout',
                        severity='critical',
                        duration_outside=time_outside,
                        distance_from_boundary=calculate_distance_from_nearest_zone(
                            current_location.location, assigned_zones
                        )
                    )


def get_animal_location_history(animal, hours=24):
    """Get location history for an animal within specified hours"""
    cutoff_time = timezone.now() - timedelta(hours=hours)
    return AnimalLocation.objects.filter(
        animal=animal,
        recorded_at__gte=cutoff_time
    ).select_related('device').prefetch_related('inside_zones').order_by('-recorded_at')


def get_zone_occupancy_stats(zone):
    """Get occupancy statistics for a grazing zone"""
    try:
        # Get current occupancy (animals in zone in last hour)
        current_time = timezone.now()
        hour_ago = current_time - timedelta(hours=1)

        current_animals = AnimalLocation.objects.filter(
            inside_zones=zone,
            recorded_at__gte=hour_ago
        ).values('animal').distinct().count()

        # Get daily occupancy (unique animals in last 24 hours)
        day_ago = current_time - timedelta(days=1)
        daily_animals = AnimalLocation.objects.filter(
            inside_zones=zone,
            recorded_at__gte=day_ago
        ).values('animal').distinct().count()

        # Get assigned animals count
        assigned_animals = AnimalGrazingAssignment.objects.filter(
            zone=zone,
            is_active=True
        ).count()

        occupancy_percentage = 0
        if zone.max_capacity:
            occupancy_percentage = (current_animals / zone.max_capacity) * 100

        return {
            'current_occupancy': current_animals,
            'daily_unique_visitors': daily_animals,
            'assigned_animals': assigned_animals,
            'max_capacity': zone.max_capacity,
            'occupancy_percentage': round(occupancy_percentage, 2),
            'is_overcrowded': zone.max_capacity and current_animals > zone.max_capacity
        }

    except Exception as e:
        logger.error(f"Error calculating zone occupancy for {zone.name}: {str(e)}")
        return {
            'current_occupancy': 0,
            'daily_unique_visitors': 0,
            'assigned_animals': 0,
            'max_capacity': zone.max_capacity,
            'occupancy_percentage': 0,
            'is_overcrowded': False
        }


def check_device_health(device):
    """Check the health status of a tracking device"""
    health_issues = []

    # Check battery level
    if device.last_battery_level is not None:
        if device.last_battery_level <= 10:
            health_issues.append('Critical battery level')
        elif device.last_battery_level <= 20:
            health_issues.append('Low battery level')

    # Check signal strength
    if device.last_signal_strength is not None:
        if device.last_signal_strength < 20:
            health_issues.append('Poor signal strength')

    # Check last update time
    if device.location_records.exists():
        last_update = device.location_records.order_by('-recorded_at').first()
        time_since_update = timezone.now() - last_update.recorded_at
        expected_interval = timedelta(minutes=device.update_interval_minutes * 2)  # Allow 2x interval

        if time_since_update > expected_interval:
            health_issues.append('Delayed updates')

    return {
        'is_healthy': len(health_issues) == 0,
        'issues': health_issues,
        'last_battery_level': device.last_battery_level,
        'last_signal_strength': device.last_signal_strength,
        'status': device.status
    }


def generate_location_summary_report(animal, start_date, end_date):
    """Generate a summary report of animal locations for a date range"""
    try:
        locations = AnimalLocation.objects.filter(
            animal=animal,
            recorded_at__range=[start_date, end_date]
        ).select_related('device').prefetch_related('inside_zones').order_by('recorded_at')

        if not locations.exists():
            return None

        # Calculate statistics
        total_locations = locations.count()
        total_distance = 0
        zones_visited = set()
        time_in_zones = {}

        previous_location = None
        for location in locations:
            # Calculate distance traveled
            if previous_location:
                # Simple distance calculation (should use proper geodesic calculation)
                distance = location.location.distance(previous_location.location) * 111000  # Convert to meters
                total_distance += distance

            # Track zones visited
            for zone in location.inside_zones.all():
                zones_visited.add(zone.name)
                if zone.name not in time_in_zones:
                    time_in_zones[zone.name] = timedelta(0)

            previous_location = location

        # Calculate time spent in each zone (simplified)
        for location in locations:
            for zone in location.inside_zones.all():
                # Add update interval to time in zone
                time_in_zones[zone.name] += timedelta(minutes=location.device.update_interval_minutes)

        return {
            'animal': {
                'tag_id': animal.tag_id,
                'name': animal.name
            },
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'statistics': {
                'total_locations': total_locations,
                'total_distance_km': round(total_distance / 1000, 2),
                'zones_visited': list(zones_visited),
                'zones_visited_count': len(zones_visited),
                'time_in_zones': {
                    zone: str(duration) for zone, duration in time_in_zones.items()
                }
            }
        }

    except Exception as e:
        logger.error(f"Error generating location summary for {animal.tag_id}: {str(e)}")
        return None