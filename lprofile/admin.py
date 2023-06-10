from django.contrib import admin
from .models import posts, profile1, comments, jobs

# Register your models here.
admin.site.register(posts)
admin.site.register(profile1)
admin.site.register(comments)
admin.site.register(jobs)