from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


class CatalogView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request, *args, **kwargs):
        return render(request, 'items/catalog.html')
