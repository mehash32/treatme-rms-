from django.contrib import admin
from .models import Comment, Review, Voucher

# Register your models here.
admin.site.register(Comment)
admin.site.register(Review)
admin.site.register(Voucher)
