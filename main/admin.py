from django.contrib import admin

from .models import Category, Apartment, ApartmentImage, Comment, Likes, Rating, Favorites


class ApartmentImageInLine(admin.TabularInline):
    model = ApartmentImage
    max_num = 50
    min_num = 1


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    inlines = [ApartmentImageInLine,]


admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Favorites)