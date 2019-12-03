import subprocess, os, sys

from django.core.management.base import BaseCommand
from django.core import management


class Command(BaseCommand):
    help = 'Build react-admin'

    def handle(self, *args, **options):
        cwd = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../src')
        ps = subprocess.Popen("yarn install", shell=True, cwd=cwd)
        ps.wait() and sys.exit(1)
        ps = subprocess.Popen("yarn build", shell=True, cwd=cwd)
        ps.wait() and sys.exit(1)
        management.call_command('collectstatic')
