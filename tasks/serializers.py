from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import Task, Category

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    A serializer for user registration.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class CategorySerializer(serializers.ModelSerializer):
    """
    A serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'owner']
        read_only_fields = ['owner']
        extra_kwargs = {
            'name': {'validators': [UniqueValidator(queryset=Category.objects.all())]}
        }


class TaskSerializer(serializers.ModelSerializer):
    """
    A serializer for the Task model.
    """
    # This field is used for representing the category name in GET requests
    category = serializers.StringRelatedField(read_only=True)
    
    # This field is used for assigning a category in POST and PUT requests
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True, 
        required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'category', 'category_id', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']
