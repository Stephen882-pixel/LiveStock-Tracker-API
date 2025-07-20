from rest_framework import  serializers
from .models import  Animal,Breed

class BreedSerializer(serializers.ModelSerializer):
    animals_count = serializers.SerializerMethodField()


    class Meta:
        model = Breed
        fields = ['id','name','description','origin_country','created_at','updated_at','animals_count']

    def get_animals_count(self,obj):
        return obj.animals.filter(status='active').count()


class AnimalListSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source='breed.name',read_only=True)
    age_in_years = serializers.ReadOnlyField()

    class Meta:
        model = Animal
        fields = ['id','tag_id','name','breed','breed__name','gender','color','status','location','date_of_birth','weight','age_in_years','health_status','created_at','updated_at']


class AnimalDetailSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source='breed.name', read_only=True)
    # age_in_years = serializers.ReadOnlyField()

    class Meta:
        model = Animal
        fields = ['id','tag_id','name','breed','breed_name','gender','color','status','location','date_of_birth','weight','health_status','age_in_years','created_at','updated_at']


    def validate_tag_id(self,value):
        """Ensure the tag id is unique"""
        if Animal.objects.filter(tag_id=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise  serializers.ValidationError("An animal with this tag ID already exists.")
        return  value

    def validate_weight(self,value):
        """validate weight is positive"""
        if value<=0:
            raise serializers.ValidationError("Weight must be greater than 0")
        return value

class AnimalCreateSerializer(serializers.ModelSerializer):
    breed = serializers.CharField()

    class Meta:
        model = Animal
        fields = ['tag_id','name','breed','gender','date_of_birth',
                  'weight','color','status','location','health_status','notes']

    def validate_tag_id(self, value):
        """Ensure tag_id is unique"""
        if Animal.objects.filter(tag_id=value).exists():
            raise serializers.ValidationError("An animal with this tag ID already exists.")
        return value

    def validate_weight(self, value):
        """Validate weight is positive"""
        if value <= 0:
            raise serializers.ValidationError("Weight must be greater than 0.")
        return value

    def validate_breed(self,value):
        """Validate that the breed exists"""
        try:
            breed = Breed.objects.get(name=value)
            return breed
        except Breed.DoesNotExist:
            raise  serializers.ValidationError(f"Breed '{value}' does not exist")

    def to_representation(self, instance):
        """Return a detailed representation after creatio"""
        return AnimalDetailSerializer(instance).data
