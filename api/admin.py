from django.contrib import admin

from .models import Job, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')


# admin.site.register(models.Job)
# admin.site.register(models.User)
# admin.site.register(UserAdmin)

admin.site.register(Job)

# Register the User model with the custom admin class
admin.site.register(User, UserAdmin)
