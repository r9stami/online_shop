from django.contrib import admin

from product.models import Information,Product, Category, Color, Size , HeadImage ,Like ,  Comment


class InformationInline(admin.TabularInline):
    model = Information


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_public', 'price',)
    list_filter = ('title', 'is_public', 'price')
    search_fields = ('title','is_public')
    inlines = [InformationInline]


admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Like)
admin.site.register(HeadImage)
admin.site.register(Information)
admin.site.register(Comment)
