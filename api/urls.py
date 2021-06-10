from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"image", views.ImageViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('test-task/', views.TestTaskRun.as_view()),
    path('ocr-process/', views.OCRProcessAPIView.as_view(), name="ocr_process"),
    path('ocr-process/<str:image_id>/', views.OCRProcessAPIView.as_view(), name="ocr_process")
]


