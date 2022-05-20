from django.db import models
from django.contrib.auth.models import  User

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

    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'Partenaire'


class Categorie(models.Model):
    nom = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

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
        db_table = 'Plats'



