import requests
from bs4 import BeautifulSoup
from django.test import TestCase
import pprint

# Create your tests here.
class Test(TestCase):
    def test_xml_parse(self):
        URL = "https://www.sec.gov/Archives/edgar/data/921669/000156761920019587/form13fInfoTable.xml"
        response = requests.get(URL).text
        data = BeautifulSoup(response, 'xml')
        pprint.pprint(data)
        name_list = data('nameOfIssuer')
        arr = {}
        for name in name_list:
            if name.text not in arr:
                arr[name.text] = int(data('sshPrnamt'))
            else:
                arr[name.text] += int(data('sshPrnamt'))
        print(arr)
        test_arr = ['Cheniere Energy Inc']
        self.assertFalse(True)
        input = input()