from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django_resized import ResizedImageField
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    """all category database model"""
    name = models.CharField(max_length=100, default="")
    slug = models.SlugField(default="", null=True, max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    """all products database model"""
    name = models.CharField(max_length=200, default="", null=True)
    description = models.CharField(max_length=2000, default="", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price =  models.PositiveIntegerField(default=0, null=True)
    image = ResizedImageField(size=[100, 100], upload_to='images', null=True)
    slug = models.SlugField(max_length=200, null=True)
    count = models.PositiveIntegerField(default=0)
    extra_desc = models.CharField(max_length=600, default="")

    class Meta:
        ordering = ['-count']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Review(models.Model):
    """all product reviews database model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=500, default="")
    stars = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'User: {self.user}, Product: {self.product}'

class CartItem(models.Model):
    """all items in the cart model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)    
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.name} x {self.quantity}'

class Profile(models.Model):
    """all user profile model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.user.username
