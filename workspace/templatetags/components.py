from django import template
from core.models import *
from django.conf import settings
from core.choices import *
from core.forms import MetaForm
from workspace.manageDataviews.forms import CreateDataStreamForm

register = template.Library()

def get_activity_type(activity):

    from core.choices import ActionStreams
    
    activity_name=""

    # 0 - CREATE
    if int(activity) == (ActionStreams.CREATE):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASCREATED')
    # 1 - DELETE
    elif int(activity) == int(ActionStreams.DELETE):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASDELETED')
    # 2 - PUBLISH
    elif int(activity) == int(ActionStreams.PUBLISH):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASPUBLISHED')
    # 3 - UNPUBLISH
    elif int(activity) == int(ActionStreams.UNPUBLISH):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASUNPUBLISHED')
    # 4 - REJECT
    elif int(activity) == int(ActionStreams.REJECT):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASREJECTED')
    # 5 - ACCEPT
    elif int(activity) == int(ActionStreams.ACCEPT):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASACCEPTED')
    # 6 - REVIEW
    elif int(activity) == int(ActionStreams.REVIEW):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASSENTTOREVIEW')
    # 7 - EDIT
    elif int(activity) == int(ActionStreams.EDIT):
        activity_name = ugettext_lazy('LANDINGPAGE-ACTIVITY-HASEDITED')

    return activity_name

register.assignment_tag(get_activity_type)
