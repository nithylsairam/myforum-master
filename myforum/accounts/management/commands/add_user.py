"""
Takes as input a CVS file with two columns

Email, Name, Handler

"""
import csv
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from myforum.accounts import util
from myforum.accounts.models import User, Profile

logger = logging.getLogger("engine")


class Command(BaseCommand):
    help = "Add users"

    def add_arguments(self, parser):

        parser.add_argument('--fname', help="The CSV file with the users to be added. Must have headers: Name, Email")

    def handle(self, *args, **options):

        # Get the filename.
        fname = options['fname']

        if not os.path.isfile(fname):
            logger.error(f'Not a valid filename: {fname}')
            return

        stream = open(fname, 'rU')
        for row in csv.DictReader(stream):
            name = row.get("Name", '')
            email = row.get("Email", '')
            handler = row.get("Handler", '')

            # All fields must be filled in.
            if not (name and email):
                logger.error(f"Invalid row: {row}")
                continue

            # Fix capitalization.
            name = name.strip()
            email = email.strip().lower()
            handler = handler.strip()

            if User.objects.filter(email=email).exists():
                logger.info(f"Skipped creation. User with email={email} already exists.")
            else:
                username = handler or util.get_uuid(16)
                user = User.objects.create(email=email, username=username, first_name=name)
                user.set_password(settings.SECRET_KEY)
                user.save()
                logger.info(f"Created user name={name} email={email}")
