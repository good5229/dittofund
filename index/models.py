from django.db import models


# Create your models here.
class HedgeFund(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{name}'


class Portfolio(models.Model):
    years = models.IntegerField()
    period = models.IntegerField()
    name = models.ForeignKey(HedgeFund, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)

    def __str__(self):
        return f'{years}년 {period}분기 - {name} 보고서'


class Data(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cusip = models.CharField(max_length=50)
    title_of_class = models.CharField(max_length=100)
    values = models.IntegerField()
    shares = models.IntegerField()

    def __str__(self):
        return f'{name} - {shares}'
