from django.contrib import admin
from .models import *



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'user')
    list_filter = ('date', 'category')
    search_fields = ('title', 'text')
 


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)



admin.site.register(Post, PostAdmin)
admin.site.register(Ip)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile)
