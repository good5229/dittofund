import requests
from bs4 import BeautifulSoup
from django.test import TestCase

from .models import HedgeFund, Portfolio, Data


# Create your tests here.
class Receive_Test(TestCase):
    def test_xml_parse(self):
        # Given : 헤지펀드, 포트폴리오 오브젝트
        HedgeFund.objects.create(name='test_hedge')
        self.assertEqual(HedgeFund.objects.all().count(), 1)

        URL = "https://www.sec.gov/Archives/edgar/data/921669/000156761920019587/form13fInfoTable.xml"
        test_portfolio = Portfolio.objects.create(years=2020, period=1,
                                                  name=HedgeFund.objects.filter(name='test_hedge').first(), url=URL)
        self.assertEqual(Portfolio.objects.all().count(), 1)

        # When : 헤지펀드와 포트폴리오의 URL이 주어졌을 때
        YEAR = 2020
        PERIOD = 1
        response = requests.get(Portfolio.objects.filter(years=YEAR, period=PERIOD).first().url).text
        data = BeautifulSoup(response, 'xml')

        # Then : XML파일을 Parse하여 데이터를 분리하고
        name_list = data('nameOfIssuer')
        title_of_class = data('titleOfClass')
        cusip = data('cusip')
        sshPrnamt = data('sshPrnamt')
        value = data('value')
        # 분리된 데이터마다 데이터 객체를 생성한다.
        Dataset = Data.objects.all()
        for i in range(len(name_list)):
            data_name = name_list[i].text,
            if not Dataset.filter(portfolio=test_portfolio, name=data_name[0],
                                  title_of_class__contains=title_of_class[i].text, cusip=cusip[i].text):
                Data.objects.create(portfolio=test_portfolio, name=data_name[0],
                                    title_of_class=title_of_class[i].text, cusip=cusip[i].text,
                                    shares=sshPrnamt[i].text, values=value[i].text)
            else:
                Data_previous = Data.objects.get(portfolio=test_portfolio, name=data_name[0],
                                                 title_of_class=title_of_class[i].text, cusip=cusip[i].text)
                ### Data previous에서 검색되는 객체가 없어서 shares가 NoneType으로 나
                Data_previous.shares += int(sshPrnamt[i].text)
                Data_previous.values += int(value[i].text)
                Data_previous.save()

        # 읽어온 row의 갯수와 생성된 데이터 객체를 비교한다.
        for datum in Data.objects.all():
            print(datum)
        self.assertEqual(Data.objects.all().count(), 16)
