import logging
from django.db.models.signals import post_migrate
from django.apps import AppConfig

logger = logging.getLogger('engine')


class ForumConfig(AppConfig):
    name = 'myforum.forum'

    def ready(self):
        from . import signals
        # Triggered upon app initialization.
        post_migrate.connect(init_awards, sender=self)


def init_awards(sender, **kwargs):
    "Initializes the badges"
    from myforum.forum.models import Badge
    from myforum.forum.awards import ALL_AWARDS

    for obj in ALL_AWARDS:
        badge = Badge.objects.filter(name=obj.name)
        if badge:
            continue
        badge = Badge.objects.create(name=obj.name)

        # Badge descriptions may change.
        if badge.desc != obj.desc:
            badge.desc = obj.desc
            badge.icon = obj.icon
            badge.type = obj.type
            badge.save()

        logger.debug("initializing badge %s" % badge)
