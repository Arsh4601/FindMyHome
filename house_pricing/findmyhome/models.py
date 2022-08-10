from django.db import models


class Feedback(models.Model):

    date=models.DateField()
    fid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=254)
    comment=models.CharField(max_length=200)

    def __str__(self) -> str:
        return "{} {}".format(self.date,self.name)

