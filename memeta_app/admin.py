from django.contrib import admin
from .models import Course, CardFront, CardBack, Card, Preferences, Session, Rep, SessionLog, IllKnow, HonoredIllKnow

admin.site.register(Course)
admin.site.register(CardFront)
admin.site.register(CardBack)
admin.site.register(Card)
admin.site.register(Preferences)
admin.site.register(Session)
admin.site.register(Rep)
admin.site.register(SessionLog)
admin.site.register(IllKnow)
admin.site.register(HonoredIllKnow)