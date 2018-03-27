from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt


class UserManager(models.Manager):
    def register_validation(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user_exist = User.objects.filter(email=postData['email'])
        errors = []
        if len(postData['name']) < 2:
            errors.append("Name must have at least two characters, letters only")
        if len(postData['username']) < 2:
            errors.append("Username must have at least two characters, letters only")
        if len(postData['location']) < 2:
            errors.append("Location must have at least two characters, letters only")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append('Email must be valid')
        elif len(user_exist) > 0:
            errors.append("User exist with that email, please use another email")    
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['password'] != postData['confirm']:
            errors.append("Password and confim pw must match")
        if len(errors) > 0:
            return (False, errors)
        
        else:
            u = User.objects.create(
                name=postData['name'],
                username=postData['username'],
                location=postData['location'],
                email=postData['email'],
                password=bcrypt.hashpw(postData['password'].encode('utf8'), bcrypt.gensalt()))
            return (True, u)

    def login_validation(self, postData):
        email_regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
        errors = []
        if not email_regex.match(postData['email']):
            errors.append('Email must be valid')
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")

        if len(errors) > 0:
            return (False, errors)

        else:
            u = User.objects.filter(email=postData['email'])
            if u: 
                if bcrypt.checkpw(postData['password'].encode(), u[0].password.encode()):
                    return (True, u[0]) 
                    
                else:
                    errors.append("Password is incorrect") 
                    return(False, errors)
            else:
                print "did not find email"
                errors.append("No user exists with this email") 
                return(False, errors)  

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    
    def __str__(self):
	    return 'name: {}, username {}'.format(self.name, self.username)

