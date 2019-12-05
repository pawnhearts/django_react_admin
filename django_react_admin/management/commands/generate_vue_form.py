import subprocess, os, sys

from django.core.management.base import BaseCommand
from django.core import management
from subprocess import Popen, PIPE
import importlib

from django_react_admin.forms import generate_vue_form


class Command(BaseCommand):
    help = 'Generate vue form'

    def add_arguments(self, parser):
        parser.add_argument('args', metavar='viewset', nargs='+', help='ViewSet or serializer class')

    def handle(self, *args, **options):
        mod, cls = args[0].rsplit('.', 1)
        mod = importlib.import_module(mod)
        obj = getattr(mod, cls)

        res = generate_vue_form(obj)
        try:
            ps = Popen(['npx', 'vue-beautify'], stdin=PIPE, stdout=PIPE)
            stdout, stderr = ps.communicate(res.encode('utf-8'))
            if ps.wait() == 0:
                print(stdout.decode('utf-8'))
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            print(res)

