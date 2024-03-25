from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Subject, Group, Expense, Pupil
from users.serializers import TeacherSerializer

Teacher = get_user_model()

class SubjectSerializer(serializers.ModelSerializer):
    groups_count = serializers.SerializerMethodField()
    pupils_count = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Subject

    def get_groups_count(self, subject):
        return subject.group_set.count()

    def get_pupils_count(self, subject):
        return Pupil.objects.filter(group__subject=subject).count()


class GroupSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), write_only=True)
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), write_only=True)

    class Meta:
        fields = '__all__'
        model = Group
        extra_kwargs = {
            'price': {
                'style': {'input_type': 'number'}
            }
        }
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        teacher = instance.teacher
        subject = instance.subject

        representation['teacher'] = f'{teacher.first_name} {teacher.last_name}'
        representation['subject'] = subject.name
        representation['pupils'] = instance.pupil_set.count()
        return representation

    def create(self, validated_data):
        teacher = validated_data.pop('teacher')
        subject = validated_data.pop('subject')
        group = Group.objects.create(teacher=teacher, subject=subject, **validated_data)
        return group

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'created', 'owner', 'name', 'amount', 'note']
        model = Expense
        extra_kwargs = {
            'amount': {
                'style': {'input_type': 'number'}
            }
        }
