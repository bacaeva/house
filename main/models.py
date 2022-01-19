from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from account.models import MyUser


class Category (models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70, primary_key=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Apartment(models.Model):
    title = models.CharField(max_length=250)
    rooms = models.IntegerField(choices=((i, i) for i in range(1, 10)))
    description = models.TextField()
    category = models.ForeignKey(Category,
                               on_delete=models.CASCADE,
                               related_name='apartments')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class ApartmentImage(models.Model):
    image = models.ImageField(upload_to='images')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return str(self.comment)


class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="rating")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating) + " | " + self.apartment.title + " | " + str(self.user)


class Likes(models.Model):
    likes = models.BooleanField(default=False)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return str(self.likes)


class Favorites(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='favorites')
    favorites = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.favorites} - {self.apartment}'