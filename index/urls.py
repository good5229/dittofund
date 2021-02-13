from django.urls import path

from index.views import Index, CompareView, PortfolioList, HedgefundList, HedgefundDetail, PortfolioDetail, \
    PortfolioCreate

app_name = 'index'

urlpatterns = [
    path('', Index.as_view(), name='intro'),
    path('hedgefund/', HedgefundList.as_view(), name='hedgefund'),
    path('hedgefund/<int:pk>/', HedgefundDetail.as_view()),
    path('compare/', CompareView.as_view(), name='compare'),
    path('portfolio/', PortfolioList.as_view(), name='portfolio'),
    path('portfolio/<int:pk>/', PortfolioDetail.as_view()),
    path('create_portfolio/', PortfolioCreate.as_view()),

]
