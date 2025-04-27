from django.urls import path
from .views import ItemView, CategoryView, SupplierView, StockSummaryView, LowStockItemsView

urlpatterns = [
    path('items/tambah/', ItemView.as_view()),       
    path('items/', ItemView.as_view()),               
    path('kategori/tambah/', CategoryView.as_view()), 
    path('kategori/', CategoryView.as_view()),        
    path('supplier/tambah/', SupplierView.as_view()), 
    path('supplier/', SupplierView.as_view()),        
    path('summary/stock/', StockSummaryView.as_view()),  
    path('items/low-stock/', LowStockItemsView.as_view()), 
]
