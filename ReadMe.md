# 🐄 LiveStock Tracker API Documentation

## 📖 Overview

The LiveStock Tracker API is a comprehensive RESTful service built with Django REST Framework that enables intelligent livestock management through real-time tracking, health monitoring, camera integration, and multi-channel communication.

**Base URL:** `https://api.livestocktracker.com/api/v1/`

## 🔐 Authentication

All API endpoints require authentication using JWT tokens.

### Get JWT Token

```http
POST /api/auth/token/
```

**Request Body:**
```json
{
    "username": "farmer@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token

```http
POST /api/auth/token/refresh/
```

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Authorization Header

Include the JWT token in all subsequent requests:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## 👤 User Management

### Register User

```http
POST /api/auth/register/
```

**Request Body:**
```json
{
    "username": "john_farmer",
    "email": "john@example.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "farmer",
    "phone_number": "+254712345678"
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "username": "john_farmer",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "farmer",
    "phone_number": "+254712345678",
    "date_joined": "2025-07-18T10:30:00Z"
}
```

### Get User Profile

```http
GET /api/auth/profile/
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "john_farmer",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "farmer",
    "phone_number": "+254712345678",
    "farm_name": "Green Valley Farm",
    "location": "Nairobi, Kenya"
}
```

### Update User Profile

```http
PUT /api/auth/profile/
```

**Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+254712345678",
    "farm_name": "Green Valley Farm",
    "location": "Nairobi, Kenya"
}
```

---

## 🐄 Animal Management

### List Animals

```http
GET /api/animals/
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `search`: Search by tag_id or name
- `breed`: Filter by breed
- `status`: Filter by status (active, sold, deceased)

**Response (200 OK):**
```json
{
    "count": 45,
    "next": "https://api.livestocktracker.com/api/v1/animals/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "tag_id": "COW-001",
            "name": "Bessie",
            "breed": "Holstein",
            "gender": "female",
            "date_of_birth": "2023-03-15",
            "weight": 450.5,
            "color": "black_white",
            "status": "active",
            "location": {
                "latitude": -1.2921,
                "longitude": 36.8219,
                "last_updated": "2025-07-18T14:30:00Z"
            },
            "health_status": "healthy",
            "owner": 1,
            "created_at": "2025-01-10T08:00:00Z",
            "updated_at": "2025-07-18T14:30:00Z"
        }
    ]
}
```

### Create Animal

```http
POST /api/animals/
```

**Request Body:**
```json
{
    "tag_id": "COW-002",
    "name": "Daisy",
    "breed": "Jersey",
    "gender": "female",
    "date_of_birth": "2023-05-20",
    "weight": 380.0,
    "color": "brown",
    "status": "active"
}
```

**Response (201 Created):**
```json
{
    "id": 2,
    "tag_id": "COW-002",
    "name": "Daisy",
    "breed": "Jersey",
    "gender": "female",
    "date_of_birth": "2023-05-20",
    "weight": 380.0,
    "color": "brown",
    "status": "active",
    "location": null,
    "health_status": "healthy",
    "owner": 1,
    "created_at": "2025-07-18T15:00:00Z",
    "updated_at": "2025-07-18T15:00:00Z"
}
```

### Get Animal Details

```http
GET /api/animals/{id}/
```

**Response (200 OK):**
```json
{
    "id": 1,
    "tag_id": "COW-001",
    "name": "Bessie",
    "breed": "Holstein",
    "gender": "female",
    "date_of_birth": "2023-03-15",
    "weight": 450.5,
    "color": "black_white",
    "status": "active",
    "location": {
        "latitude": -1.2921,
        "longitude": 36.8219,
        "last_updated": "2025-07-18T14:30:00Z"
    },
    "health_status": "healthy",
    "owner": 1,
    "recent_health_events": [
        {
            "id": 5,
            "event_type": "vaccination",
            "description": "Annual vaccination - FMD",
            "date": "2025-07-10",
            "veterinarian": "Dr. Sarah Johnson"
        }
    ],
    "created_at": "2025-01-10T08:00:00Z",
    "updated_at": "2025-07-18T14:30:00Z"
}
```

### Update Animal

```http
PUT /api/animals/{id}/
```

**Request Body:**
```json
{
    "weight": 455.0,
    "status": "active",
    "location": {
        "latitude": -1.2925,
        "longitude": 36.8225
    }
}
```

### Delete Animal

```http
DELETE /api/animals/{id}/
```

**Response (204 No Content)**

---

## 🩺 Health Management

### List Health Events

```http
GET /api/health/events/
```

**Query Parameters:**
- `animal_id`: Filter by animal ID
- `event_type`: Filter by event type (vaccination, treatment, checkup, illness)
- `date_from`: Start date (YYYY-MM-DD)
- `date_to`: End date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
    "count": 12,
    "results": [
        {
            "id": 1,
            "animal": {
                "id": 1,
                "tag_id": "COW-001",
                "name": "Bessie"
            },
            "event_type": "vaccination",
            "description": "Annual vaccination - FMD",
            "symptoms": null,
            "treatment": "Foot and Mouth Disease vaccine",
            "medication": "FMD Vaccine 2ml",
            "dosage": "2ml intramuscular",
            "veterinarian": {
                "id": 3,
                "name": "Dr. Sarah Johnson",
                "license_number": "VET-2024-001"
            },
            "cost": 1500.00,
            "next_due_date": "2026-07-10",
            "notes": "Animal responded well to vaccination",
            "event_date": "2025-07-10",
            "created_at": "2025-07-10T09:30:00Z"
        }
    ]
}
```

### Create Health Event

```http
POST /api/health/events/
```

**Request Body:**
```json
{
    "animal_id": 1,
    "event_type": "treatment",
    "description": "Treatment for respiratory infection",
    "symptoms": "Coughing, difficulty breathing, fever",
    "treatment": "Antibiotic treatment",
    "medication": "Amoxicillin",
    "dosage": "500mg twice daily for 7 days",
    "veterinarian_id": 3,
    "cost": 2500.00,
    "notes": "Monitor for improvement over next 3 days"
}
```

**Response (201 Created):**
```json
{
    "id": 13,
    "animal": {
        "id": 1,
        "tag_id": "COW-001",
        "name": "Bessie"
    },
    "event_type": "treatment",
    "description": "Treatment for respiratory infection",
    "symptoms": "Coughing, difficulty breathing, fever",
    "treatment": "Antibiotic treatment",
    "medication": "Amoxicillin",
    "dosage": "500mg twice daily for 7 days",
    "veterinarian": {
        "id": 3,
        "name": "Dr. Sarah Johnson",
        "license_number": "VET-2024-001"
    },
    "cost": 2500.00,
    "next_due_date": null,
    "notes": "Monitor for improvement over next 3 days",
    "event_date": "2025-07-18",
    "created_at": "2025-07-18T15:30:00Z"
}
```

### Get Health Event Details

```http
GET /api/health/events/{id}/
```

### Update Health Event

```http
PUT /api/health/events/{id}/
```

### Delete Health Event

```http
DELETE /api/health/events/{id}/
```

---

## 📸 Camera Management

### List Camera Feeds

```http
GET /api/cameras/
```

**Response (200 OK):**
```json
{
    "count": 3,
    "results": [
        {
            "id": 1,
            "name": "Barn Camera 1",
            "description": "Main barn entrance",
            "stream_url": "rtsp://192.168.1.100:554/live",
            "is_active": true,
            "location": "Main Barn",
            "resolution": "1920x1080",
            "frame_rate": 30,
            "created_at": "2025-07-01T10:00:00Z",
            "last_activity": "2025-07-18T15:45:00Z"
        }
    ]
}
```

### Create Camera Feed

```http
POST /api/cameras/
```

**Request Body:**
```json
{
    "name": "Pasture Camera 1",
    "description": "North pasture monitoring",
    "stream_url": "rtsp://192.168.1.101:554/live",
    "location": "North Pasture",
    "resolution": "1920x1080",
    "frame_rate": 25
}
```

### Get Camera Feed Details

```http
GET /api/cameras/{id}/
```

### Update Camera Feed

```http
PUT /api/cameras/{id}/
```

### Delete Camera Feed

```http
DELETE /api/cameras/{id}/
```

### Get Camera Snapshot

```http
GET /api/cameras/{id}/snapshot/
```

**Response:** Binary image data (JPEG)

---

## 📱 Notifications

### Send SMS Notification

```http
POST /api/notifications/sms/
```

**Request Body:**
```json
{
    "recipients": ["+254712345678", "+254723456789"],
    "message": "Alert: Cow COW-001 has moved outside designated area",
    "priority": "high",
    "animal_id": 1
}
```

**Response (201 Created):**
```json
{
    "id": 1,
    "recipients": ["+254712345678", "+254723456789"],
    "message": "Alert: Cow COW-001 has moved outside designated area",
    "priority": "high",
    "status": "sent",
    "sent_at": "2025-07-18T16:00:00Z",
    "delivery_reports": [
        {
            "phone_number": "+254712345678",
            "status": "delivered",
            "delivered_at": "2025-07-18T16:00:30Z"
        }
    ]
}
```

### Send Voice Call

```http
POST /api/notifications/voice/
```

**Request Body:**
```json
{
    "phone_number": "+254712345678",
    "message": "Urgent: Your cow COW-001 requires immediate attention. Please check the animal.",
    "priority": "critical",
    "animal_id": 1
}
```

### Handle USSD Session

```http
POST /api/notifications/ussd/
```

**Request Body:**
```json
{
    "session_id": "session123",
    "phone_number": "+254712345678",
    "text": "1*2*COW-001"
}
```

**Response (200 OK):**
```json
{
    "response": "CON Animal COW-001 (Bessie)\nStatus: Healthy\nLocation: Main Barn\nLast Updated: 2 hours ago\n\n1. View Health History\n2. Report Issue\n0. Back"
}
```

---

## 🤖 Chatbot Integration

### Send Query to Chatbot

```http
POST /api/chatbot/query/
```

**Request Body:**
```json
{
    "query": "Where is cow COW-001 right now?",
    "context": {
        "user_id": 1,
        "farm_id": 1
    }
}
```

**Response (200 OK):**
```json
{
    "id": "query_123",
    "query": "Where is cow COW-001 right now?",
    "response": "Cow COW-001 (Bessie) is currently located at coordinates -1.2921, 36.8219 in the Main Barn area. Last location update was 30 minutes ago. The animal appears to be healthy and active.",
    "confidence": 0.95,
    "entities": [
        {
            "type": "animal",
            "value": "COW-001",
            "confidence": 0.99
        }
    ],
    "timestamp": "2025-07-18T16:30:00Z"
}
```

### Get Chat History

```http
GET /api/chatbot/history/
```

**Query Parameters:**
- `limit`: Number of conversations to return (default: 10)
- `date_from`: Start date for filtering

---

## 📊 Analytics & Reports

### Get Farm Statistics

```http
GET /api/analytics/farm-stats/
```

**Response (200 OK):**
```json
{
    "total_animals": 45,
    "active_animals": 43,
    "animals_by_breed": {
        "Holstein": 20,
        "Jersey": 15,
        "Angus": 10
    },
    "health_events_this_month": 12,
    "upcoming_vaccinations": 5,
    "alerts_this_week": 3,
    "average_weight": 425.5,
    "location_distribution": {
        "Main Barn": 15,
        "North Pasture": 20,
        "South Pasture": 8
    }
}
```

### Get Health Report

```http
GET /api/analytics/health-report/
```

**Query Parameters:**
- `period`: Report period (week, month, quarter, year)
- `animal_id`: Specific animal ID (optional)

---

## 🔄 Real-time WebSocket Connections

### Animal Tracking WebSocket

```javascript
const ws = new WebSocket('ws://api.livestocktracker.com/ws/animal-tracking/');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Location update:', data);
};

// Sample message format:
{
    "type": "location_update",
    "animal_id": 1,
    "tag_id": "COW-001",
    "location": {
        "latitude": -1.2921,
        "longitude": 36.8219,
        "timestamp": "2025-07-18T16:45:00Z"
    }
}
```

### Alerts WebSocket

```javascript
const ws = new WebSocket('ws://api.livestocktracker.com/ws/alerts/');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Alert received:', data);
};

// Sample alert message:
{
    "type": "health_alert",
    "severity": "high",
    "animal_id": 1,
    "tag_id": "COW-001",
    "message": "Animal showing signs of distress",
    "timestamp": "2025-07-18T16:50:00Z",
    "location": {
        "latitude": -1.2921,
        "longitude": 36.8219
    }
}
```

---

## 🚨 Error Handling

### Standard Error Response Format

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "tag_id": ["This field is required."],
            "weight": ["Must be a positive number."]
        },
        "timestamp": "2025-07-18T17:00:00Z"
    }
}
```

### Common HTTP Status Codes

- **200 OK**: Successful GET, PUT
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

---

## 🔧 Rate Limiting

- **General API**: 1000 requests per hour per user
- **Authentication**: 10 requests per minute
- **SMS/Voice**: 50 requests per hour
- **WebSocket**: 100 connections per user

---

## 📝 API Versioning

The API uses URL-based versioning:
- Current version: `v1`
- Base URL: `https://api.livestocktracker.com/api/v1/`

---

## 🛠️ Development Tools

### Swagger/OpenAPI Documentation

Interactive API documentation available at:
- **Swagger UI**: `https://api.livestocktracker.com/swagger/`
- **ReDoc**: `https://api.livestocktracker.com/redoc/`
- **OpenAPI Schema**: `https://api.livestocktracker.com/swagger.json`



