# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from core.models import *
import urllib2

class Command(BaseCommand):
    help = "List all accounts."

    def handle(self, *args, **options):
        print "ID;Account Name;Status;Level;Domain;Api Domain;URI;status"
        for account in Account.objects.all():
            try:
                domain= Preference.objects.get(account=account, key="account.domain").value
            except Preference.DoesNotExist:
                domain = "Sin Definir"

            try:
                api_domain= Preference.objects.get(account=account, key="account.api.domain").value
            except Preference.DoesNotExist:
                api_domain = "Sin Definir"

            try:
                if Preference.objects.filter(account=account, key="account.microsite.https", value__in=["ok","on","true","True","On"]).count():
                    uri="https://"
                else:
                    uri="http://"

                uri+="%s/home" % domain
                status = urllib2.urlopen(uri, timeout=20).getcode()
            except Preference.DoesNotExist:
                uri="-"
                status=999
            except urllib2.HTTPError:
                status=404
            print "%s;%s;%s;%s;%s;%s;%s;%s" % (account.id,account.name, account.get_status_display(), account.level, domain, api_domain,uri,status)
