import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger('engine')


class Command(BaseCommand):
    help = 'Used to test markdown rendering'

    def handle(self, *args, **options):

        from myforum.utils import markdown

        print(markdown.test())