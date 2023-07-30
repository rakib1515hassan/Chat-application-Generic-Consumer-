from django.contrib import admin

from ChatApp.models import Group, Chat
# Register your models here.

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'name' )



@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ( 'id','user', 'group', 'content', 'create_at' )