import logging
from urllib.request import urlopen, Request

import hjson
import mistune
from django.conf import settings
from django.template import loader

from myforum.utils.decorators import spool


#
# Do not use logging in tasks! Deadlocking may occur!
#
# https://github.com/unbit/uwsgi/issues/1369


def message(msg, level=0):
    print(f"{msg}")


@spool(pass_arguments=True)
def detect_location(ip, user_id):
    """
    Fills the user location based on url.
    """
    from myforum.accounts.models import Profile

    msg = f"location check for \tid={user_id}\tip={ip}"

    # The lookup needs to be turned on.
    if not settings.LOCATION_LOOKUP:
        message(f"skip {msg}")
        return

    message(f"execute {msg}")

    # Get the profile for the user
    profile = Profile.objects.filter(user__id=user_id).first()

    # Skip value if it has the word unknown in it
    def get(data, attr):
        value = data.get(attr, '')
        return "" if "unknown" in value.lower() else value.title()

    # Check and log location.
    if not profile.location:
        try:
            url = f"http://api.hostip.info/get_json.php?ip={ip}"
            message(url)
            message(f"{ip}, {profile.user}, {url}")
            req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urlopen(req, timeout=3).read()
            data = hjson.loads(resp)

            city = get(data, "city")
            country = get(data, "country_name")
            location = city or country

            msg = f"location result for \tid={user_id}\tip={ip}\tloc={location}"
            if location:
                Profile.objects.filter(user=profile.user).update(location=location)
                message(f"updated profile {msg}")
            else:
                message(f"empty location {msg}")

        except Exception as exc:
            message(exc)


@spool(pass_arguments=True)
def create_messages(template, rec_list, sender=None, extra_context={}):
    """
    Create batch message from sender to a given recipient_list
    """
    from myforum.accounts.models import User, Message, MessageBody

    # Get the sender
    name, email = settings.ADMINS[0]
    sender = sender or User.objects.filter(email=email).first()

    # Load the template and context
    tmpl = loader.get_template(template_name=template)
    context = dict(sender=sender)
    context.update(extra_context)

    body = tmpl.render(context)
    html = mistune.markdown(body, escape=False)

    msgs = []
    for rec in rec_list:
        body = MessageBody.objects.create(body=body, html=html)
        msg = Message.objects.create(sender=sender, recipient=rec, body=body)
        msgs.append(msg)

    return msgs
