from django.conf import settings
from django.views.generic import FormView

from .forms import ImageForm


class OCRForm(FormView):
    form_class = ImageForm
    template_name = 'ocr_form.html'

    def get_context_data(self, **kwargs):
        context = super(OCRForm, self).get_context_data()
        return {
            **context,
            "backend_url": settings.BACKEND_URL
        }
