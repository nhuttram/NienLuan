from django.db import models
from rest_framework import serializers
from .models import Khach_Hang

class GetAllCourseSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model  = Khach_Hang
        fields = ('id' ,)