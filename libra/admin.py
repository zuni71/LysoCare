from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.User)
admin.site.register(models.Answer)
# admin.site.register(models.RatingQuestion)
# admin.site.register(models.YesNoQuestion)


class DataAdmin(admin.ModelAdmin):
    def export_as_csv(self, request, queryset):
        pass
    actions = ['export_as_csv']
