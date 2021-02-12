# Create your views here.
import xml.etree.ElementTree as ET

import requests
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'index/introduce.html'


class HedgefundView(TemplateView):
    template_name = 'index/hedgefund/hedgefund_index.html'


class CompareView(TemplateView):
    template_name = 'index/compare/compare_index.html'


class PortfolioView(TemplateView):
    template_name = 'index/portfolio/portfolio_index.html'

    def get(self, request, pk):
        URL = "https://www.sec.gov/Archives/edgar/data/921669/000156761920019587/form13fInfoTable.xml"
        xml = requests.get(URL).text
        root = ET.fromstring(xml.text)
        result = ''
        for str in root.iter('str'):
            if (str.attrib.get('name') == 'status'):
                result = str.text
