from django_react_admin import views
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', include(views.urlpatterns)),
    path('', TemplateView.as_view(template_name='django_react_admin/index.html'), name='react_admin_index_html')
]
