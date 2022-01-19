"""market_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import CategoryListView, ApartmentViewSet, CommentViewSet, LikesViewSet, RatingViewSet, \
    ApartmentImageViewSet, FavoritesListView, FavoritesCreateView, FavoriteDetailView
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(

    openapi.Info(

        title='Shop API from bootcamp',

        description='Our shop',

        default_version='v1'

    ),

    public=True

)





router = DefaultRouter()
router.register('apartments', ApartmentViewSet)
router.register('images', ApartmentImageViewSet)
router.register('rating', RatingViewSet)
router.register('likes', LikesViewSet)
router.register('comments', CommentViewSet)


urlpatterns = [
    path('docs/', schema_view.with_ui('swagger')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/categories/', CategoryListView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/', include(router.urls)),
    path('v1/api/favorites/', FavoritesListView.as_view()),
    path('v1/api/favorites/create/', FavoritesCreateView.as_view()),
    path('v1/api/favorites/<int:pk>/', FavoriteDetailView.as_view()),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)