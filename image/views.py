from django.conf import settings
from django.views.generic import FormView

from api.serializers import ImageSerializer
from .forms import ImageForm
from .models import Image


class OCRForm(FormView):
    form_class = ImageForm
    template_name = 'ocr_form.html'

    def get_context_data(self, **kwargs):
        context = super(OCRForm, self).get_context_data()
        image_id = self.kwargs.get("image_id")
        custom_context = {"backend_url": settings.BACKEND_URL}
        if image_id:
            image = Image.objects.get(id=image_id)
            custom_context["image"] = ImageSerializer(image).data
        return {
            **context,
            **custom_context
        }
