from django.contrib import admin
from .models.user import User
from .models.profile import Profile
# from .models.follow import Follow

admin.site.register(User)
admin.site.register(Profile)
# admin.site.register(Follow)