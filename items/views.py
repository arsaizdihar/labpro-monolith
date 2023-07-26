from math import ceil
from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from .models import BuyHistory

from items.api import buy_item, get_item_detail, get_items_catalog, get_items_count


class CatalogView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get('page', 1))
            page = max(page, 1)
        except ValueError:
            page = 1
        response = get_items_catalog(page)
        count_response = get_items_count()
        if response.ok and count_response.ok:
            items = response.json()["data"]
            context = {
                'items': items,
                'page': page,
                'startnum': (page - 1) * 10,
                'page_total': ceil(count_response.json()["data"] / 10),
            }
            return render(request, 'items/catalog.html', context=context)
        return render(request, '404.html')


class ItemDetailView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request, id, *args, **kwargs):
        response = get_item_detail(id)
        if response.ok:
            item = response.json()["data"]
            context = {
                'item': item,
            }
            return render(request, 'items/detail.html', context=context)
        return render(request, '404.html')

    def post(self, request, id, *args, **kwargs):
        response = get_item_detail(id)
        if not response.ok:
            return render(request, '404.html')
        item = response.json()["data"]
        final = request.POST.get('final')
        stok = item["stok"]
        try:
            buy_amount = int(request.POST.get('amount'))
        except ValueError:
            messages.add_message(request, messages.ERROR,
                                 "Jumlah pembelian harus angka")
            return render(request, 'items/detail.html', context=context)
        if buy_amount <= 0:
            messages.add_message(
                request, messages.ERROR, "Jumlah pembelian harus positif")
            return render(request, 'items/detail.html', context=context)
        context = {
            'item': item,
        }
        if (stok < buy_amount):
            messages.add_message(request, messages.ERROR, "Stok tidak cukup")
            return render(request, 'items/detail.html', context=context)
        if final:
            response = buy_item(id, buy_amount)
            if not response.ok:
                print(response.json())
                messages.add_message(
                    request, messages.ERROR, "Gagal membeli barang")
                return render(request, 'items/detail.html', context=context)
            BuyHistory.objects.create(
                name=item["nama"], amount=buy_amount, price=item["harga"], total=buy_amount * item["harga"], user=request.user)
            messages.add_message(request, messages.SUCCESS,
                                 "Berhasil membeli barang")
            return redirect('history')
        context['buy_amount'] = buy_amount
        context['total_price'] = buy_amount * item["harga"]
        return render(request, 'items/buy.html', context=context)


class HistoryView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request, *args, **kwargs):
        try:
            page = int(request.GET.get('page', 1))
            page = max(page, 1)
        except ValueError:
            page = 1

        buy_histories = BuyHistory.objects.filter(user=request.user).all()
        paginator = Paginator(buy_histories, 10)
        context = {
            'histories': paginator.get_page(page),
            'page': page,
            'startnum': (page - 1) * 10,
            'page_total': ceil(paginator.count / 10),
        }
        return render(request, 'items/history.html', context=context)
