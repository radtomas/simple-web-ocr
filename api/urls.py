from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"image", views.ImageViewSet)

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'test-task/', views.TestTaskRun.as_view()),
    url(r'ocr-process/', views.OCRProcessView.as_view()),
    url(r'ocr-process/<str:task_id>/', views.OCRProcessView.as_view())
]


