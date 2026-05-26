from django.contrib import admin
from .models import Word, Definition

class DefinitionInline(admin.TabularInline):
    model = Definition
    extra = 3  # show 3 empty definition rows by default
    fields = ('text', 'order')
    ordering = ['order']

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'definitions_count', 'created_at')
    search_fields = ('text', 'definitions__text')
    inlines = [DefinitionInline]

    def definitions_count(self, obj):
        return obj.definitions.count()
    definitions_count.short_description = "تعداد معانی"