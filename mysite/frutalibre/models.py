from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import pytz


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
class Profile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, blank=True)
    # locationOriginal = models.CharField(max_length=500, blank=True)
    # locationNow = models.CharField(max_length=500, blank=True)
    locationOriginal = models.ForeignKey('Location', related_name='location_original', on_delete=models.PROTECT)
    locationNow = models.ForeignKey('Location', related_name='location_now', on_delete=models.PROTECT)

    fruits = models.ManyToManyField('Fruit')

    fieldvalue_tags = models.CharField('Field:Value tags', help_text="(Field1:\"Value1\")(Field2:\"Value2\")  eg.: (Color:\"Rojo\")(Carro:{Marca:\"Toyota\", Modelo:\"Rav4\", Año:2017})(Opciones:[1, 3, 5])", max_length=1000, blank=True) # TODO Add all relevant info here to see how to model in the future...

    def __str__(self):
        # return "{0}".format(self.user.name)
        return "{0}".format(self.email)


### Signals puestas aqui mismo
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
###


class Fruit(models.Model):
    name = models.CharField(max_length=100)

    seasonDescription = models.CharField(max_length=500)
    idealEnvironment = models.CharField(max_length=500)

    fieldvalue_tags = models.CharField('Field:Value tags', help_text="(Field1:\"Value1\")(Field2:\"Value2\")  eg.: (Color:\"Rojo\")(Carro:{Marca:\"Toyota\", Modelo:\"Rav4\", Año:2017})(Opciones:[1, 3, 5])", max_length=1000, blank=True) # TODO Add all relevant info here to see how to model in the future...

    def __str__(self):
        return "{0}".format(self.name)


class State(models.Model):
    name = models.CharField(max_length=50)

    fieldvalue_tags = models.CharField('Field:Value tags', help_text="(Field1:\"Value1\")(Field2:\"Value2\")  eg.: (Color:\"Rojo\")(Carro:{Marca:\"Toyota\", Modelo:\"Rav4\", Año:2017})(Opciones:[1, 3, 5])", max_length=1000, blank=True) # TODO Add all relevant info here to see how to model in the future...

    def __str__(self):
        return "{0}".format(self.name)


class Location(models.Model): # This was a BAD name!!! Because we are using legit locations (lat lng) in newer models!
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.PROTECT)

    fieldvalue_tags = models.CharField('Field:Value tags', help_text="(Field1:\"Value1\")(Field2:\"Value2\")  eg.: (Color:\"Rojo\")(Carro:{Marca:\"Toyota\", Modelo:\"Rav4\", Año:2017})(Opciones:[1, 3, 5])", max_length=1000, blank=True) # TODO Add all relevant info here to see how to model in the future...

    def __str__(self):
        return "{0}, {1}".format(self.name, self.state.name)


class MapPin(models.Model):
    lat = models.DecimalField('Latitude', max_digits=9, decimal_places=6)
    lng = models.DecimalField('Longitude', max_digits=9, decimal_places=6)

    # in case other...

    fieldvalue_tags = models.CharField('Field:Value tags', help_text="(Field1:\"Value1\")(Field2:\"Value2\")  eg.: (Color:\"Rojo\")(Carro:{Marca:\"Toyota\", Modelo:\"Rav4\", Año:2017})(Opciones:[1, 3, 5])", max_length=1000, blank=True) # TODO Add all relevant info here to see how to model in the future...

    def __str__(self):
        return "{0}".format(self.name)


class FruitSnap(MapPin): # snap = event = location + time
    ACCESSIBILITY = (
        ('E', 'Easy'),
        ('R', 'Regular'),
        ('C', 'Complicated'),
    )
    STARS = (
        (0, ''),
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    )

    fruit = models.ForeignKey(Fruit, on_delete=models.PROTECT)
    time = models.DateTimeField()

    imageUrl = models.CharField(max_length=300)

    accesibility = models.CharField(max_length=2, choices=ACCESSIBILITY)
    quality = models.PositiveSmallIntegerField(choices=STARS)

    # fieldvalue_tags = models.CharField('Field:Value tags', help_text="(Field1:\"Value1\")(Field2:\"Value2\")  eg.: (Color:\"Rojo\")(Carro:{Marca:\"Toyota\", Modelo:\"Rav4\", Año:2017})(Opciones:[1, 3, 5])", max_length=1000, blank=True) # TODO Add all relevant info here to see how to model in the future...

    def __str__(self):
        pr_time = self.time.astimezone(pytz.timezone('America/Puerto_Rico'))
        return "{0} ({1})".format(self.fruit.name, pr_time.strftime('%a. %m.%d %-I:%M%p'))
