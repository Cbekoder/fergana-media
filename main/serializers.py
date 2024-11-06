from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'first_name', 'last_name', 'photo', 'position', 'licence_no']

class StaffPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['photo']


class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = ['is_test_mode', 'test_mode_info', 'phone', "email", "domain", "instagram", "telegram", "youtube", "facebook", "address"]

