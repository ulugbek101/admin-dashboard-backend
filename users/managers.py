from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
   def create_user(self, first_name, last_name, email):
       self.model.create()