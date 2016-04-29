# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError

from core.models import *

class Command(BaseCommand):
    help = "List all accounts."

    def handle(self, *args, **options):
        print "ID;Account Name;Status;Level;Domain;Api Domain"
        for account in Account.objects.all():
            try:
                domain= Preference.objects.get(account=account, key="account.domain").value
                api_domain= Preference.objects.get(account=account, key="account.api.domain").value
            except:
                domain = "Sin Definir"
                api_domain = "Sin Definir"
            print "%s;%s;%s;%s;%s;%s" % (account.id,account.name, account.get_status_display(), account.level, domain, api_domain)
