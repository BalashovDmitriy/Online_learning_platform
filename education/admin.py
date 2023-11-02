from django.contrib import admin

from education.models import Course, Lesson, Payment, Subscription
from users.models import User

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Payment)
admin.site.register(Subscription)
admin.site.register(User)
