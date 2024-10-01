from django.contrib import admin
from app.models import post,Tag,Comments,Profile,WebsiteMeta

# Register your models here.
admin.site.register(post)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(Profile)
admin.site.register(WebsiteMeta)