from django.db import models


class Shelf(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    medicine = models.CharField(max_length=200, unique=True)
    price = models.FloatField(verbose_name="Price for the medicine")
    add_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.medicine
    