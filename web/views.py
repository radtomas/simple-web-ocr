from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from web.forms import ImageForm


class IndexView(View):
    form_class = ImageForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print(form)

            return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})
