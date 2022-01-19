# from django.db import models
# from django.contrib.auth import get_user_model
# from main.models import Apartment
#
#
# class Order (models.Model):
#     user = models.ForeignKey(get_user_model(),
#                              on_delete=models.RESTRICT,
#                              related_name='orders')
#     total_sum = models.DecimalField(max_digits=18,decimal_places=2)
#     address = models.CharField(max_length=100)
#     notes = models.CharField(max_length=255, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     products = models.ManyToManyField(Apartment, through='OrderItem')
#
#
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order,
#                               on_delete=models.RESTRICT,
#                               related_name='items')
#     product = models.ForeignKey(Apartment,
#                                 on_delete=models.RESTRICT,
#                                 related_name='apartments')
#     quantity = models.SmallIntegerField(default=1)
#
