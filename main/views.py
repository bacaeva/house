from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from main.models import Category, Apartment, Comment, Likes, Rating, Favorites
from main.permissions import IsAuthor
from main.serializers import CategorySerializer, ApartmentSerializer, CommentSerializer, LikesSerializer, \
    RatingSerializer, ApartmentImageSerializer, FavoritesSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def get_permissions(self):
    #     if self.action in ['list', 'retrieve']:
    #         return []
    #     return [IsAdminUser()]


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', ]:
            permissions = [IsAuthenticated, ]
        else:
            permissions = [ ]
        return [permission() for permission in permissions]

    # def get_permissions(self):
    #     if self.action in ['list', 'create','update','destroy','retrieve']:
    #         return []
    #     elif self.action == 'reviews':
    #         if self.request.method == "POST":
    #             return []
    #         return [IsAuthenticated()]
    #     return [IsAdminUser()]

    @action(methods=['GET'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset().filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(address__icontains=q)
    )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        days_count = int(self.request.query_params.get('days', 0))
        if days_count > 0:
            start_date = timezone.now() - timedelta(days=days_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset


class ApartmentImageViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentImageSerializer

    # def get_serializer_context(self):
    #     return {'request':self.request}



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated ]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthenticated]


class FavoritesCreateView(generics.CreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = self.request.user
        queryset = Favorites.objects.filter(author=qs, favorites=True)
        return queryset


class FavoritesListView(generics.ListAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]


class FavoriteDetailView(generics.RetrieveDestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticated]