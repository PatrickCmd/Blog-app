from django.contrib import admin

from .models import (Author, Category, Tag, Post, Feedback)


class AuthorAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'activation_key', 'email_validated')
    # search_fields = ['name', 'email']
    # ordering = ['-name']
    # list_filter = ['active']
    # date_hierarchy = 'created_on'


class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'slug')
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'slug')
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'pub_date', 'author', 'category')
    search_fields = ['title', 'content']
    ordering = ['-pub_date']
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    # filter_horizontal = ('tags', )
    raw_id_fields = ('tags',)
    # prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('slug',)
    fields = ('title', 'slug', 'content', 'author', 'category', 'tags',)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','date',)
    search_fields = ('name', 'email',)
    date_hierarchy = 'date'


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Feedback, FeedbackAdmin)
