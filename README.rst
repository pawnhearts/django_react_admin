Add django_react_admin to your INSTALLED_APPS

Add path('react_admin/', include(django_react_admin.urls.urlpatterns)) to your urls

APIs would be exposed at /react_admin/api/ and /react_admin/ would be html with react-admin

Run ./manage.py build_react_admin

Your STATIC_URL should be /static/