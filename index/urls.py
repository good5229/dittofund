from django.urls import path

from index.views import Index, HedgefundView, CompareView, PortfolioView

app_name = 'index'

urlpatterns = [
    path('', Index.as_view(), name='intro'),
    path('hedgefund/', HedgefundView.as_view(), name='hedgefund'),
    path('compare/', CompareView.as_view(), name='compare'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
]
