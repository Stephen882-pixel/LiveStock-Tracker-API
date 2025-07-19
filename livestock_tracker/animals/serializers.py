from symtable import Class

from rest_framework import  serializers
from .models import  Animal,Breed

class BreedSerializer(serializers.ModelSerializer):
    animals_count = serializers.SerializerMethodField()


    class Meta:
        model = Breed
        fields = ['id','name','description','origin_country','created_at','updated_at']

    def get_animals_count(self,obj):
        return obj.animals.filter(status='active').count()


class AnimalListSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source='breed.name',read_only=True)
    age_in_years = serializers.ReadOnlyField()

    class Meta:
        model = Animal
        fields = ['id','tag_id','name','breed','breed_name','gender','date_of_birth','weight','health_status','created_at','updated_at']


class AnimalDetailSerializer(serializers.ModelSerializer):
    breed_name = serializers.CharField(source='breed.name', read_only=True)

    class Meta:
        model = Animal
        fields = ['id','tag_id','name','breed','breed_name','gender','date_of_birth','weight','health_status','created_at','updated_at']


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
    class Meta:
        model = Animal
        fields = ['tag_id','name','breed','gender','date_of_birth',
                  'weight','health_status','notes']

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

