from django.core.management.base import BaseCommand

from optparse import make_option

from core.models import (User, Grant, VisualizationRevision, Preference, DataStreamRevision, DatasetRevision, Role,
                         VisualizationI18n, DatastreamI18n)
from core.choices import StatusChoices
import json
from django.db.models import Q



class Command(BaseCommand):

    role_migration_dict = {
        'ao-editor': 'ao-editor',
        'ao-user': '',
        'ao-viewer': '',
        'ao-member': '',
        'ao-ops': '',
        'ao-publisher-premier': 'ao-publisher',
        'ao-publisher-plus': 'ao-publisher',
        'ao-enhancer-premier': 'ao-editor',
        'ao-enhancer-plus': 'ao-editor',
        'ao-collector-premier': 'ao-editor',
        'ao-collector-plus': 'ao-editor',
        'ao-free-user': '',
        'ao-publisher': 'ao-publisher',
        'ao-enhancer': 'ao-editor',
        'ao-collector': 'ao-editor',
        'ao-account-admin': 'ao-account-admin',
    }

    def chanageResourcesStatus(self, resources):
        for res in resources:
            if res.status == 2:
                res.status = StatusChoices.PENDING_REVIEW # 1
            elif res.status == 4:
                res.status = StatusChoices.DRAFT # 0
            elif res.status == 5:
                res.status = StatusChoices.DRAFT # 0
            res.save()

    def changeStatus(self):
        self.chanageResourcesStatus(VisualizationRevision.objects.all())
        self.chanageResourcesStatus(DataStreamRevision.objects.all())
        self.chanageResourcesStatus(DatasetRevision.objects.all())

    def migrateRoles(self):
        for key, value in self.role_migration_dict.items():
            if key != value:
                try:
                    key_role = Role.objects.get(code=key)
                    value_role = Role.objects.get(code=key)
                except Role.DoesNotExist:
                    pass
                else:
                    for grant in key_role.grant_set.all():
                            Grant.objects.get_or_create(
                                user=grant.user, 
                                role=value_role, 
                                privilege=grant.privilege, 
                                guest=grant.guest)

    def migrateUserRoles(self):
        role_dict = {}
        for key, value in self.role_migration_dict.items():
            try: 
                role_dict[key]=Role.objects.get(code=key)
            except Role.DoesNotExist:
                pass

        for user in User.objects.all():
            user_codes=user.roles.all().values_list('code', flat=True)
            for code in user_codes:
                if self.role_migration_dict[code] and code != self.role_migration_dict[code]:
                    user.roles.add(role_dict[self.role_migration_dict[code]])
                    user.roles.remove(role_dict[code])

    def handle(self, *args, **options):

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

        for home in Preference.objects.filter(Q(key="account.home")| Q(key="account.preview")):
            config = json.loads(home.value)

            try:
                if 'config' in config and 'sliderSection' in config['config'] and config['config']['sliderSection']:
                    sliderSection=[]
                    for slider in config['config']['sliderSection']:
                        sliderSection.append({u'type': slider['type'].replace("chart","vz"), u'id': slider['id']})

                    config['config']['sliderSection']=sliderSection
                home.value=json.dumps(config)
                home.save()
            except TypeError:
                pass
                
            # actualizo estados
            self.changeStatus() 
            self.migrateRoles()
            self.migrateUserRoles()



        # VisualizationI18n
        visualization_revisions = VisualizationRevision.objects.exclude(user__account__id__in=[5990, 5991])
        for visualization_revision in visualization_revisions:
            try:
                datastreami18n = DatastreamI18n.objects.filter(datastream_revision__datastream=visualization_revision.visualization.datastream.pk).latest('id')
                title = datastreami18n.title
                description = datastreami18n.description
                notes = datastreami18n.notes
            except:
                if visualization_revision.user.language == 'es':
                    title = 'Nombre'
                    description = 'Descripcion'
                    notes = ''
                else:
                    title = 'Name'
                    description = 'Description'
                    notes = ''

            obj, created = VisualizationI18n.objects.get_or_create(
                language=visualization_revision.user.language,
                visualization_revision=visualization_revision,
                created_at=visualization_revision.created_at,
                title=title,
                description=description,
                notes=notes
            )
