from django.shortcuts import render
from django.views.generic import View


class Index(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'website.html')
