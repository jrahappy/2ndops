from django.contrib import admin
from .models import ICase, ICaseComment


# Register your models here.
class ICaseCommentInline(admin.TabularInline):
    model = ICaseComment
    extra = 1


class ICaseAdmin(admin.ModelAdmin):
    inlines = [ICaseCommentInline]


admin.site.register(ICase, ICaseAdmin)
