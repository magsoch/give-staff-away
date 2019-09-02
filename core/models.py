from django.contrib.auth.models import User
from django.db import models

# Create your models here.
CLOTHES = (
    ('1', 'ubrania, które nadają się do ponownego użycia'),
    ('2', 'ubrania do wyrzucenia'),
    ('3', 'zabawki'),
    ('4', 'książki'),
    ('5', 'inne')
)

FOR_WHO = (
    ('1', 'Męskie'),
    ('2', 'Damskie'),
    ('3', 'Dziecięce dla dziewczynki'),
    ('4', 'Dziecięce dla chłopca')
)

PURPOSE = (
    ('1', 'Sezon jesień-zima'),
    ('2', 'Sezon wiosna-lato')
)

GENDER = (
    ('1', 'Chłopiec'),
    ('2', 'Dziewczynka')
)

AGE = (
    ('1', '0-2'),
    ('2', '3-5'),
    ('3', '6-8'),
    ('4', '9-12'),
    ('5', '12-15'),
    ('6', '15+')
)

BOOKS = (
    ('1', 'dla dorosłych'),
    ('2', 'dla dzieci'),
    ('3', 'dla młodzieży'),
    ('4', 'edukacyjne')
)


LOCATION = (
    ('1', 'dolnośląskie'),
    ('2', 'kujawsko-pomorskie'),
    ('3', 'lubelskie'),
    ('4', 'lubuskie'),
    ('5', 'łódzkie'),
    ('6', 'małopolskie'),
    ('7', 'mazowieckie'),
    ('8', 'opolskie'),
    ('9', 'podkarpackie'),
    ('10', 'podlaskie'),
    ('11', 'pomorskie'),
    ('12', 'śląskie'),
    ('13', 'świętokrzyskie'),
    ('14', 'warmińsko-mazurskie'),
    ('15', 'wielkopolskie'),
    ('16', 'zachodniopomorskie'),
)

HELP = (
    ('1', 'dzieciom'),
    ('2', 'samotnym matkom'),
    ('3', 'bezdomnym'),
    ('4', 'niepełnosprawnym'),
    ('5', 'osobom starszym'),
    ('6', 'bezrobotnym'),
)


class Clothes(models.Model):
    type = models.CharField(max_length=255, null=True)
    for_who = models.CharField(max_length=255, null=True)
    purpose = models.CharField(max_length=255, null=True)


class Toys(models.Model):
    toys = models.CharField(max_length=128, null=True)


class Books(models.Model):
    books = models.CharField(max_length=128, null=True)


class Others(models.Model):
    others = models.TextField(null=True)


class Bags(models.Model):
    number_of_bags = models.IntegerField()


class Help(models.Model):
    for_who = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.for_who


class Charity(models.Model):
    location = models.CharField(max_length=50, choices=LOCATION)
    help = models.ManyToManyField(Help)
    charity_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.charity_name


class Address(models.Model):
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=6)
    phone = models.IntegerField()
    more_info = models.TextField(null=True)
    date = models.DateField()
    time = models.TimeField()


class Donate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clothes = models.ForeignKey(Clothes, on_delete=models.SET_NULL, null=True)
    useless_clothes = models.BooleanField(default=False)
    toys = models.ForeignKey(Toys, on_delete=models.SET_NULL, null=True)
    books = models.ForeignKey(Books, on_delete=models.SET_NULL, null=True)
    others = models.ForeignKey(Others, on_delete=models.SET_NULL, null=True)
    bags = models.ForeignKey(Bags, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    form_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name="Odebrany")
    status_change = models.DateTimeField('status', null=True)

