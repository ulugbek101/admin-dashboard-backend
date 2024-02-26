from rest_framework import serializers

from .models import Subject, Group, Expense, Pupil


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
