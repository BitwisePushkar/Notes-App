from django.contrib import admin
from .models import Info


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_text_preview', 'created_at_display')
    search_fields = ('title', 'text')
    list_filter = ('title',)
    fields = ('title', 'text')
    list_per_page = 20
    ordering = ('-id',)
    list_display_links = ('id', 'title')
    
    def get_text_preview(self, obj):
        if len(obj.text) > 50:
            return obj.text[:50] + '...'
        return obj.text
    get_text_preview.short_description = 'Text Preview'
    
    def created_at_display(self, obj):
        return 'N/A'
    created_at_display.short_description = 'Created At'
    actions = ['delete_selected']
    
    def delete_selected(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} Info object(s) deleted successfully.')
    delete_selected.short_description = 'Delete selected Info objects'