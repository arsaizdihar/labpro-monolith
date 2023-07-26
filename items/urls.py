from django.urls import path
from .views import CatalogView, ItemDetailView, HistoryView

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('barang/<id>/', ItemDetailView.as_view(), name='detail'),
    path('history', HistoryView.as_view(), name='history')
]
