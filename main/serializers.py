from django.db.models import Avg
from rest_framework import serializers

from main.models import Category, Apartment, ApartmentImage, Comment, Likes, Rating, Favorites


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImage
        fields = ('image',)

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    # def _get_image_url(self, obj):
    #     if obj.image:
    #         url = obj.image.url
    #         return url
    #     return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        apartment = Apartment.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            ApartmentImage.objects.create(image=image,
                                     apartment=apartment)
        return apartment

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            ApartmentImage.objects.create(image=image,
                                     apartment=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = ApartmentImageSerializer(instance.images.all(),
                                                       many=True).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.rating.aggregate(Avg('rating'))

        return representation


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class RatingSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        apartment = validated_data.get('apartment')
        rating = Rating.objects.get_or_create(user=user, apartment=apartment)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating


class LikesSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        apartment = validated_data.get('apartment')
        like = Likes.objects.get_or_create(author=author, apartment=apartment)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like


class FavoritesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Favorites
        fields = '__all__'