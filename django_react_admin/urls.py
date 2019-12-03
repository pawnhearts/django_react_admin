from django_react_admin import views
from django.urls import path, include
from django.http import HttpRequest, HttpResponse

def show_index_html(request):
    with open('static/django_react_admin/index.html', 'r') as f:
        return HttpResponse(f.read())

urlpatterns = [
    path('api/', include(views.urlpatterns)),
    path('', show_index_html, name='react_admin_index_html')
]
