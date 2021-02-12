from django.urls import path

from index.views import Index, CompareView, PortfolioList, HedgefundList

app_name = 'index'

urlpatterns = [
    path('', Index.as_view(), name='intro'),
    path('hedgefund/', HedgefundList.as_view(), name='hedgefund'),
    path('compare/', CompareView.as_view(), name='compare'),
    path('portfolio/', PortfolioList.as_view(), name='portfolio'),
]
