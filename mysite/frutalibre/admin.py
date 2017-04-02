from django.contrib import admin

from .models import Profile, Fruit, State, Location, FruitSnap

admin.site.register(Profile)
admin.site.register(Fruit)
admin.site.register(State)
admin.site.register(Location)
admin.site.register(FruitSnap)
