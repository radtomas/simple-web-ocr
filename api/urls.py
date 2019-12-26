from django.conf.urls import url
from django.urls import path, include

from api import views


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
    path(r'ocr-process/', views.OCRProcessView.as_view()),
    path(r'ocr-process/<str:task_id>/', views.OCRProcessView.as_view())
]


