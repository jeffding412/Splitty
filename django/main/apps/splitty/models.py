from __future__ import unicode_literals
from django.db import models
import bcrypt

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['username']) < 1:
            errors["username"] = "Username is a required field"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        user = User.objects.filter(username=postData['username'])
        if user and not bcrypt.checkpw(postData['password'].encode(), user[0].password_hash.encode()):
            errors['failure'] = "Invalid Credentials"

        return errors

class User(models.Model):
    username = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()