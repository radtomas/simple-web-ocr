from django.urls import path

from web import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='ocr_form')
]
