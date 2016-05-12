from django.contrib import admin

from . import models


class DinnerPlanItemInline(admin.TabularInline):
    """
    Adds inline form with DinnerPlanItems for the DinnerPlanAdmin
    """
    model = models.DinnerPlanItem
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'slug')
    prepopulated_fields = {'slug': ('title', )}


class DinnerPlanAdmin(admin.ModelAdmin):
    exclude = ('end_date',)
    inlines = [
        DinnerPlanItemInline,
    ]


admin.site.register(models.DinnerPlan, DinnerPlanAdmin)
admin.site.register(models.DinnerPlanItem)
admin.site.register(models.Recipe, RecipeAdmin)
