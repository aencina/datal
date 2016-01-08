from django.core.management.base import BaseCommand

from optparse import make_option

from core.models import User, Grant, VisualizationRevision, Preference

import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        print('FIXING USER GRANTS')

        # TODO: Debemos buscar los usuarios con Roles que no usamos mas y cambiarlos por los nuevos
        # TODO
        for rev in VisualizationRevision.objects.all():
            imp = json.loads(rev.impl_details)

            if 'labelSelection' in imp['chart']:
                header = imp['chart']['labelSelection'].replace(' ', '')
                answer = []
                for mh in header.split(','):
                    if ':' not in mh:
                        answer.append("%s:%s" % (mh, mh))
                    else:
                        answer.append(mh)
                imp['chart']['labelSelection'] = ','.join(answer)
            if 'headerSelection' in imp['chart']:
                header = imp['chart']['headerSelection'].replace(' ', '')
                answer = []
                for mh in header.split(','):
                    if ':' not in mh:
                        answer.append("%s:%s" % (mh, mh))
                    else:
                        answer.append(mh)
                imp['chart']['headerSelection'] = ','.join(answer)

            spaces=('latitudSelection', 'longitudSelection', 'traceSelection', 'data')

            for s in spaces:
                if s in imp['chart']:
                    imp['chart'][s] = imp['chart'][s].replace(' ', '')
                elif s in imp:
                    imp[s] = imp[s].replace(' ', '')

            renames=( ("zoomLevel", "zoom"),
                ("mapCenter","center"),
            )
            for rename in renames:
                if rename[0] in imp['chart']:
                    imp['chart'][rename[1]]=imp['chart'][rename[0]]
                    imp['chart'].pop(rename[0])

            if 'headerSelection' in imp['chart'] and imp['chart']['headerSelection'] == ":":
                imp['chart']['headerSelection'] = ''

            rev.impl_details = json.dumps(imp)
            rev.save()


#############################
## Preferencias
## del account.home.config.sliderSection cambiamos los type:chart a type:vz

        for home in Preference.objects.filter(key="account.home"):
            config = json.loads(home.value)

            if 'config' in config and 'sliderSection' in config['config'] and config['config']['sliderSection']:
                sliderSection=[]
                for slider in config['config']['sliderSection']:
                    sliderSection.append({u'type': slider['type'].replace("chart","vz"), u'id': slider['id']})

                config['config']['sliderSection']=sliderSection
            home.value=json.dumps(config)
            home.save()
                
            
