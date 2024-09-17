from django.contrib import admin
from .models import Product, Review, CartItem, Category, Profile

# Register your models here.
@admin.register(Product)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Profile)
@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }