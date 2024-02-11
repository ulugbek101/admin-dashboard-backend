from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Subject, Group, Expense
from users.serializers import TeacherSerializer


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Subject


class GroupSerializer(serializers.ModelSerializer):
    # teacher = TeacherSerializer(read_only=True)
    # subject = SubjectSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Group
        extra_kwargs = {
            'price': {
                'style': {'input_type': 'number'}
            }
        }


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'created', 'owner', 'name', 'amount', 'note']
        model = Expense
        extra_kwargs = {
            'amount': {
                'style': {'input_type': 'number'}
            }
        }
