from django.shortcuts import render
from django.views import View

from .forms import ImageForm
from .utils import ImageProcess


class IndexView(View):
    form_class = ImageForm
    template_name = 'ocr_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            image_process = ImageProcess(
                form.cleaned_data['url'],
                form.cleaned_data['language'],
                form.cleaned_data['enforce_process']
            )
            context['image'] = image_process.process_image()

        return render(request, self.template_name, context)
