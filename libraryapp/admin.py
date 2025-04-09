from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(TakenBook)
admin.site.register(CommentsAndRating)
admin.site.register(Tag)
