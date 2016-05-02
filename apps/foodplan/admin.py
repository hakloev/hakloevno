from django.contrib import admin

from . import models


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(models.WeekPlan)
admin.site.register(models.WeekPlanRecipes)
admin.site.register(models.Recipe, RecipeAdmin)
