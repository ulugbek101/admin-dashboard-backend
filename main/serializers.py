from rest_framework import serializers

from .models import Subject, Group, Expense, Pupil
from users.serializers import TeacherSerializer


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
    teacher = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    pupils_count = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Group
        extra_kwargs = {
            'price': {
                'style': {'input_type': 'number'}
            }
        }

    def get_subject(self, object):
        subject = object.subject
        serializer = SubjectSerializer(subject)
        return serializer.data.get('name')

    def get_teacher(self, object):
        teacher = object.teacher
        serializer = TeacherSerializer(teacher)
        return f"{serializer.data.get('first_name')} {serializer.data.get('last_name')}"

    def get_pupils_count(self, object):
        pupils_count = object.pupil_set.count()
        return pupils_count

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'created', 'owner', 'name', 'amount', 'note']
        model = Expense
        extra_kwargs = {
            'amount': {
                'style': {'input_type': 'number'}
            }
        }
