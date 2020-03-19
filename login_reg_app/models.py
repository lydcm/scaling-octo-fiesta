from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # email should be in valid format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # password must be at least 8 characters, one uppercase, one lowercase, one numeric digit
        PW_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$')
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"
        if not PW_REGEX.match(postData["password"]):
            errors["password"] = "Password should be at least 8 characters, and contain 1 uppercase, 1 lowercase, and 1 number"   
        if postData["password"] != postData["confirm_password"]:
            errors["password_conf"] = "Passwords do not match!"     
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First Name should be at least 2 characters, letters only"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters, letters only"
        return errors    

class UserInfo(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
