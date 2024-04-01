from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Pupil, Group, Expense

User = get_user_model()


@receiver(signal=pre_delete, sender=Pupil)
def change_payment_information_on_pupil_delete(sender, instance, **kwargs):
    for payment in instance.payment_set.all():
        payment.pupil_fullname = instance.full_name
        payment.save()


@receiver(signal=pre_delete, sender=Group)
def change_payment_information_on_group_delete(sender, instance, **kwargs):
    for payment in instance.payment_set.all():
        payment.group_name = instance.name
        payment.save()


@receiver(signal=pre_delete, sender=User)
def change_payment_information_on_user_delete(sender, instance, **kwargs):
    for payment in instance.payment_set.all():
        payment.owner_fullname = f"{instance.first_name} {instance.last_name}"
        payment.save()

    for expense in instance.expense_set.all():
        expense.owner_fullname = f"{instance.first_name} {instance.last_name}"
        expense.save()
