from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload_image/', views.upload_image, name='upload_image'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


