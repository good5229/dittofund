# Create your views here.
import pprint

import requests
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .models import HedgeFund, Portfolio, Data


class Index(TemplateView):
    template_name = 'index/introduce.html'


class HedgefundList(ListView):
    model = HedgeFund

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HedgefundList, self).get_context_data()
        context['hedgefunds'] = HedgeFund.objects.all()
        return context


class HedgefundDetail(DetailView):
    model = HedgeFund

    def get_context_data(self, **kwargs):
        context = super(HedgefundDetail, self).get_context_data()
        context['portfolios'] = Portfolio.objects.filter(name=self.object.pk).all()
        return context


class CompareView(TemplateView):
    template_name = 'index/compare/../templates/index/compare_index.html'


class PortfolioList(ListView):
    model = Portfolio

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PortfolioList, self).get_context_data()
        context['portfolios'] = Portfolio.objects.all()
        return context


class PortfolioDetail(DetailView):
    model = Portfolio

    def get_context_data(self, **kwargs):
        context = super(PortfolioDetail, self).get_context_data()
        context['data'] = Data.objects.filter(portfolio=self.object.pk).all()
        previous_year = self.object.years
        previous_period = self.object.period - 1
        if self.object.period == 1:
            previous_period == 4
            previous_year == self.object.years - 1
        previous_portfolio = Portfolio.objects.filter(name=self.object.name, years=previous_year,
                                                      period=previous_period).first()

        if previous_portfolio:
            context['previous_data'] = Data.objects.filter(portfolio=previous_portfolio.pk).all()
            context['subtract'] = []
            for datum in Data.objects.filter(portfolio=self.object.pk).all():
                previous = Data.objects.filter(portfolio=previous_portfolio, name=datum.name, cusip=datum.cusip,
                                               title_of_class=datum.title_of_class).first()
                if previous:
                    subtract = datum.shares - previous.shares
                    context['subtract'].append([datum.name, subtract])
                else:
                    context['subtract'].append("NEW")

            pprint.pprint(context['subtract'])

        return context


class PortfolioCreate(CreateView, LoginRequiredMixin):
    model = Portfolio
    fields = ['name', 'years', 'period', 'url']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            response = super(PortfolioCreate, self).form_valid(form)
            response_data = requests.get(
                Portfolio.objects.filter(years=self.object.years, period=self.object.period).first().url).text
            data = BeautifulSoup(response_data, 'xml')

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
                if not Dataset.filter(portfolio=self.object, name=data_name[0],
                                      title_of_class__contains=title_of_class[i].text, cusip=cusip[i].text):
                    Data.objects.create(portfolio=self.object, name=data_name[0],
                                        title_of_class=title_of_class[i].text, cusip=cusip[i].text,
                                        shares=sshPrnamt[i].text, values=value[i].text)
                else:
                    Data_previous = Data.objects.get(portfolio=self.object, name=data_name[0],
                                                     title_of_class=title_of_class[i].text, cusip=cusip[i].text)
                    Data_previous.shares += int(sshPrnamt[i].text)
                    Data_previous.values += int(value[i].text)
                    Data_previous.save()
            return response
        else:
            return redirect('/index/')


def add_portfolio_data(request, pk):
    portfolio = Portfolio.objects.filter(pk=pk).first()
    response = requests.get(portfolio.url).text
    data = BeautifulSoup(response, 'xml')

    # Then : XML파일을 Parse하여 데이터를 분리하고
    name_list = data('nameOfIssuer')
    title_of_class = data('titleOfClass')
    cusip = data('cusip')
    sshPrnamt = data('sshPrnamt')
    value = data('value')
    # 분리된 데이터마다 데이터 객체를 생성한다.
    for i in range(len(name_list)):
        data_name = name_list[i].text,

        Data.objects.create(portfolio=portfolio, name=data_name[0],
                            title_of_class=title_of_class[i].text, cusip=cusip[i].text,
                            shares=sshPrnamt[i].text, values=value[i].text)
