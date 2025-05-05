from django.contrib import admin

# Register your models here.
import decimal
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from django.db.models import Sum

from .models import Blog, BlogImage,Tags,Category, Reel



class TagsInline(admin.TabularInline):
    model = Tags

class BlogImageInline(admin.TabularInline):
    model = BlogImage


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm
    list_filter = ('category',)
    search_fields = ('title','category__name')
    search_help_text = 'Search by title or category'

    def display_images(self, obj):
        images = obj.images.all()
        if images:
            return mark_safe(", ".join([f'<img src="{image.image.url}" width="50" height="50" />' for image in images]))
        return "No images"

    display_images.short_description = 'Images'
    display_images.allow_tags = True
    inlines = [BlogImageInline]

    def get_list_display(self, request):
        return ('id','title', 'category', 'display_images')


admin.site.register(Blog, BlogAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Reel)
