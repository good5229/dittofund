from django.db import models


# Create your models here.
class HedgeFund(models.Model):
    # 1. 모델의 데이터를 다음과 같이 정의한다.
    # - 헤지펀드의 명칭(텍스트)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Portfolio(models.Model):
    # 1. 모델의 데이터를 다음과 같이 정의한다.
    # - 포트폴리오의 작성 년도(정수)
    # - 포트폴리오의 작성 분기(1,2,3,4 중 하나의 정수)
    # - 포트폴리오의 이름(100글자 이하의 텍스트)
    # - 포트폴리오 XML의 URL (500글자 이하의 텍스트)
    years = models.IntegerField()
    period = models.IntegerField()
    name = models.ForeignKey(HedgeFund, on_delete=models.CASCADE)
    url = models.CharField(max_length=500)

    def __str__(self):
        return f'{self.years}년 {self.period}분기 - {self.name} 보고서'


class Data(models.Model):
    # - 모델의 데이터를 다음과 같이 정의한다.
    # - 속한 포트폴리오(ForeignKey - portfolio)
    # - 종목명(100자 이하의 TextField)
    # - CUSIP(20자 이하의 TextField)
    # - 클래스(50자 이하의 TextField)
    # - 현재가치(정수형)
    # - 주식 수(정수형)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cusip = models.CharField(max_length=50)
    title_of_class = models.CharField(max_length=100)
    values = models.IntegerField()
    shares = models.IntegerField()

    def __str__(self):
        return f'{self.name} - {self.shares}'
