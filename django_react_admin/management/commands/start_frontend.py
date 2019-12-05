import os
import sys

from django.core.management.base import BaseCommand
from django.core import management
from django.conf import settings
import json
from subprocess import Popen, PIPE
import importlib

from django_react_admin.utils import vuetify, run, fail
from django_react_admin.forms import generate_vue_form


def prepare():
    if not run('which vue >/dev/null'):
        if not run('which yarn >/dev/null'):
            fail('which npm >/dev/null', 'Please install yarn or at least npm')
            fail('npm i -g yarn')
        fail('yarn global add vue-cli')
        run('yarn global add vue-beautify js-beautify')
    else:
        fail('vue create -m yarn -n -p default frontend')
        os.chdir('frontend/')
        run('yarn add vuelidate')
        run('yarn add vue-resource')
    with open('src/main.js', 'r') as f:
        mainjs = f.read()
    if 'vuelidate' not in mainjs:
        with open('src/main.js', 'w') as f:
            f.write(mainjs.replace("import Vue from 'vue'", '''import Vue from 'vue'
import Vuelidate from 'vuelidate'
Vue.use(Vuelidate)'''))



def apis():
    yield ''
    from django.urls import get_resolver
    for func, url in get_resolver().reverse_dict.items():
        try:
            func = func
            url = url[0][0][0]
            for method, action in getattr(func, 'actions', {}).items():
                params = func.cls.lookup_field if action == 'retrieve' else 'params'
                
                yield f"""{func.initkwargs['basename']}_{action}: ({params}) => {{
                    this.$http.{method}('{url}').then(r => {{
                       alert(r) 
                    }},
                    """
        except:
            pass


class Command(BaseCommand):
    help = 'Generate vue form'

    # def add_arguments(self, parser):
    #     parser.add_argument('args', metavar='viewset', nargs='+', help='ViewSet or serializer class')

    def handle(self, *args, **options):
        # print(''.join(apis()))
        path = os.getcwd()
        prepare()
        os.chdir(path)
        from rest_framework.viewsets import ModelViewSet
        for viewset in ModelViewSet.__subclasses__():
            if viewset.__module__ != 'django_react_admin.views':
                name = viewset().get_serializer_class().Meta.model._meta.model_name.title()
                code = vuetify(generate_vue_form(viewset))
                path = f'frontend/src/components/{name}.vue'
                if os.path.exists(path) and input(f'Overwrite {path}? y/n ') != 'y':
                    continue
                open(path, 'w').write(code)
                with open(path, 'w') as f:
                    f.write(code)
