from django.contrib import admin
from .models import Post, Category, Subcategory, Tag
from markdownx.admin import MarkdownxModelAdmin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'created_at', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)  # Makes it easier to select tags in the admin
    list_filter = ('category', 'tags')
    search_fields = ('title', 'content')