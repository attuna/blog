from django.contrib import admin
from .models import Comment, Post, Tag


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['author', 'image', 'created_on', 'tags', 'content', 'title']


admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)

