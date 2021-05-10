from django.urls import path

from image import views

urlpatterns = [
    path('', views.OCRForm.as_view(), name='ocr_form')
]
