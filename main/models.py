import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    teacher = models.ForeignKey(User, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    def __str__(self):
        return self.name


class Pupil(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Ism')
    last_name = models.CharField(max_length=200, verbose_name='Familiya')
    phone_number = models.CharField(max_length=12, null=True)
    group = models.ForeignKey(
        to=Group, on_delete=models.PROTECT, verbose_name='Guruh')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        unique_together = (
            ('first_name', 'last_name', 'group'),
        )

    # @property
    # def payments(self):
    #     return self.payment_set.filter(month__month=str(date.today().month))

    # @property
    # def is_fully_paid(self):
    #     for payment in self.payment_set.all():
    #         if payment.month == str(date.today())[:-3] and payment.amount == self.group.price:
    #             return True
    #     return False

    # @property
    # def get_phone_number(self):
    #     parsed_number = phonenumbers.parse(f"{self.phone_number.country_code}{self.phone_number.national_number}", "UZ")
    #     formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    #     return formatted_number

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Expense(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    owner_fullname = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    note = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    @property
    def get_owner_fullname(self):
        return f"{self.owner.first_name} {self.owner.last_name}" if self.owner else self.owner_fullname

    def __str__(self):
        return self.name
