from django.contrib import admin

from .models import User, Meeting, Rolelist, Attendee, Buglist, Eventlist

# Register your models here.
admin.site.register(User)
admin.site.register(Buglist)
admin.site.register(Meeting)
admin.site.register(Rolelist)
admin.site.register(Attendee)
admin.site.register(Eventlist)
