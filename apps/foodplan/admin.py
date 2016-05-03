from django.contrib import admin

from . import models


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    prepopulated_fields = {'slug': ('title', )}


class DinnerPlanAdmin(admin.ModelAdmin):
    exclude = ('end_date',)

admin.site.register(models.DinnerPlan, DinnerPlanAdmin)
admin.site.register(models.DinnerPlanItem)
admin.site.register(models.Recipe, RecipeAdmin)
