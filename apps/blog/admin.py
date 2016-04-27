from django.contrib import admin
from django.db.models import TextField
from django_markdown.admin import MarkdownModelAdmin
from django_markdown.widgets import AdminMarkdownWidget

from . import models


class BlogEntryAdmin(MarkdownModelAdmin):
    list_display = ('title', 'created')
    prepopulated_fields = {'slug': ('title',)}
    # Temporary solution, while waiting for django_markdown to support Django 1.9
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

admin.site.register(models.BlogEntry, BlogEntryAdmin)
admin.site.register(models.Tag)
