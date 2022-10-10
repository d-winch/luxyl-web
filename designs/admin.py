from django.contrib import admin
from .models import Design

class DesignAdmin(admin.ModelAdmin):
    list_display = [
        'design_code',
        'title',
        'png',
    ]
    
    search_fields = ('design_code', 'title',)
    
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Design, DesignAdmin)