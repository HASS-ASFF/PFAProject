from distutils.command.upload import upload
from email.mime import image
from hashlib import blake2b
from unicodedata import category
from django.db import models
from django.contrib.auth.models import  User
from django.contrib.auth import get_user_model


User = get_user_model()

sexe = (
    ("H","Homme"),
    ("F","Femme"),
)


class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    is_staff=models.BooleanField(default=False)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email=models.CharField(max_length=200,null=True,blank=True)
    sexe = models.CharField(max_length=30, choices=sexe)
    adresse = models.CharField(max_length=100,blank=True)
    code_postal = models.CharField(blank=True, max_length=10, null=True)
    num_tel = models.CharField(max_length=30,blank=True)
    picture=models.ImageField(default='profile2.png',null=True,blank=True)

    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'Client'


class Partenaire(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    is_staff=models.BooleanField(default=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    email=models.CharField(max_length=200,null=True,blank=True)
    sexe = models.CharField(max_length=30, choices=sexe)
    adresse = models.CharField(max_length=100)
    code_postal = models.CharField(blank=True, max_length=10, null=True)
    num_tel = models.CharField(max_length=30)
    picture=models.ImageField(default='profile2.png',null=True,blank=True)

    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'Partenaire'


class Categorie(models.Model):
    nom = models.CharField(max_length=30)
    description = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'Categories_Plat'

class Plat(models.Model):
    nom = models.CharField(max_length=30)
    img_plat=models.ImageField(upload_to="plats/",null=True,blank=True)
    description = models.CharField(max_length=100)
    Prix=models.FloatField(blank=True)
    id_cat=models.ForeignKey(Categorie,on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'Plat'


class MenuItem(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    prix = models.FloatField()
    category = models.ManyToManyField('Categorie',related_name='item')


    def __str__(self):
        return self.nom
    


class Restaurant(models.Model):
    nom = models.CharField(max_length=30)
    adresse = models.CharField(max_length=100)
    code_postal = models.CharField(blank=True, max_length=10, null=True)
    image = models.ImageField(upload_to='resto_images/',blank=True)
    num_tel = models.CharField(max_length=30,blank=True)
    rest_like = models.ManyToManyField(Client, related_name='like',blank=True, null=True)
    rest_dislike = models.ManyToManyField(Client, related_name='dislike',blank=True, null=True)
    menu = models.ManyToManyField('MenuItem',related_name='liste_menu',blank=True, null=True)

    class Meta:
        db_table = 'Restaurant'

    def __str__(self) -> str:
        return self.nom

class Commande(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    prix = models.FloatField()
    items = models.ManyToManyField('MenuItem',related_name='order',blank=True)

    def __str__(self) -> str:
        return "Order created on : "+self.date_creation