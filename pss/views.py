from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Sum, F, Avg
from .models import Item, Category, Supplier
import json

@method_decorator(csrf_exempt, name='dispatch')
class ItemView(View):
    def post(self, request):
        data = json.loads(request.body)
        item = Item.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            quantity=data['quantity'],
            category_id=data['category_id'],
            supplier_id=data['supplier_id'],
            created_by_id=data['created_by_id'],
        )
        return JsonResponse({'message': 'Item created', 'item_id': item.id})

    def get(self, request):
        items = Item.objects.all()
        data = [{
            'id': item.id,
            'name': item.name,
            'price': float(item.price),
            'quantity': item.quantity,
            'category': item.category.name,
            'supplier': item.supplier.name
        } for item in items]
        return JsonResponse(data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def post(self, request):
        data = json.loads(request.body)
        category = Category.objects.create(
            name=data['name'],
            description=data['description'],
            created_by_id=data['created_by_id'],
        )
        return JsonResponse({'message': 'Category created', 'category_id': category.id})

    def get(self, request):
        categories = Category.objects.all()
        data = [{
            'id': cat.id,
            'name': cat.name,
            'description': cat.description
        } for cat in categories]
        return JsonResponse(data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class SupplierView(View):
    def post(self, request):
        data = json.loads(request.body)
        supplier = Supplier.objects.create(
            name=data['name'],
            contact_info=data['contact_info'],
            created_by_id=data['created_by_id'],
        )
        return JsonResponse({'message': 'Supplier created', 'supplier_id': supplier.id})

    def get(self, request):
        suppliers = Supplier.objects.all()
        data = [{
            'id': sup.id,
            'name': sup.name,
            'contact_info': sup.contact_info
        } for sup in suppliers]
        return JsonResponse(data, safe=False)

class StockSummaryView(View):
    def get(self, request):
        total_quantity = Item.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        total_stock_value = Item.objects.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or 0
        average_price = Item.objects.aggregate(Avg('price'))['price__avg'] or 0

        summary = {
            'total_quantity': total_quantity,
            'total_stock_value': float(total_stock_value),
            'average_price': float(average_price),
        }
        return JsonResponse(summary)

class LowStockItemsView(View):
    def get(self, request):
        threshold = int(request.GET.get('threshold', 5))  # default threshold = 5
        items = Item.objects.filter(quantity__lt=threshold)
        data = [{
            'id': item.id,
            'name': item.name,
            'quantity': item.quantity,
        } for item in items]
        return JsonResponse(data, safe=False)
