from django.utils.translation import ugettext_lazy
from django.conf import settings

from model_utils import Choices

from core.plugins_point import DatalPluginPoint

VISUALIZATION_TYPES = (
    ('columnchart', 'columnchart'),
    ('barchart', 'barchart'),
    ('linechart', 'linechart'),
    ('piechart', 'piechart'),
    ('areachart', 'areachart'),
    ('mapchart', 'mapchart')
)

VISUALIZATION_TEMPLATES = (
    ('basicchart', 'basicchart'),
    ('piechart', 'piechart'),
    ('mapchart', 'mapchart'),
    ('geochart', 'geochart')
)

BOOLEAN_FIELD = (
    ('true', 'true'),
    ('false', 'false')
)

INCLUDE_EXCLUDE = (
    ('include', 'include'),
    ('exclude', 'exclude'),
    ('previous', 'previous'),
    ('given', 'given')
)

MAP_TYPE_FIELD = (
    ('hybrid', 'hybrid'),
    ('satellite', 'satellite'),
    ('terrain', 'terrain'),
    ('roadmap', 'roadmap'),
    ('map', 'map')
)

VISUALIZATION_LIBS = (
    ('google', 'Google Charts'),
    ('d3', 'D3')
)

RESOURCES_CHOICES = (
    (settings.TYPE_DATASET, ugettext_lazy('MODEL_DATASET_LABEL')),
    (settings.TYPE_DATASTREAM, ugettext_lazy('MODEL_DATASTREAM_LABEL')),
    (settings.TYPE_VISUALIZATION, ugettext_lazy('MODEL_VISUALIZATION_LABEL')),
)

class AccountRoles():
    PUBLISHER='ao-publisher'
    EDITOR='ao-editor'
    ADMIN='ao-account-admin'

    ALL=(PUBLISHER, EDITOR, ADMIN)

class ChannelTypes():
    WEB = 0
    API = 1


class StatusChoices():
    DRAFT = 0
    PENDING_REVIEW = 1
    UNDER_REVIEW = 2
    PUBLISHED = 3
    UNPUBLISHED = 4
    REJECTED = 5
    APPROVED = 6

CHANNEL_TYPES = (
    (ChannelTypes.WEB, ugettext_lazy('CHANNEL_TYPE_WEB')),
    (ChannelTypes.API, ugettext_lazy('CHANNEL_TYPE_API'))
)


class ActionStreams():
    """ Actions on resourses for save"""
    CREATE = 0
    DELETE = 1
    PUBLISH = 2
    UNPUBLISH = 3
    REJECT = 4
    ACCEPT = 5
    REVIEW = 6
    EDIT = 7

# TODO: Create just one STATUS_CHOICES after we remove in a clean way UNDER_REVIEW and REJECTED choices
STATUS_CHOICES = Choices(
    (StatusChoices.DRAFT, ugettext_lazy('MODEL_STATUS_DRAFT')),
    (StatusChoices.PENDING_REVIEW, ugettext_lazy('MODEL_STATUS_PENDING_REVIEW')),
    (StatusChoices.UNDER_REVIEW, ugettext_lazy('MODEL_STATUS_UNDER_REVIEW')),
    (StatusChoices.PUBLISHED, ugettext_lazy('MODEL_STATUS_PUBLISHED')),
    (StatusChoices.UNPUBLISHED, ugettext_lazy('MODEL_STATUS_UNPUBLISHED')),
    (StatusChoices.REJECTED, ugettext_lazy('MODEL_STATUS_REJECTED')),
    (StatusChoices.APPROVED, ugettext_lazy('MODEL_STATUS_APPROVED'))
    )

STATUS_CHOICES_REST = Choices(
    (StatusChoices.DRAFT, "draft"),
    (StatusChoices.PENDING_REVIEW, "pending"),
    (StatusChoices.UNDER_REVIEW, "under_review"),
    (StatusChoices.APPROVED, "approved"),
    (StatusChoices.PUBLISHED, "published"),
    (StatusChoices.UNPUBLISHED, "unpublished"),
    (StatusChoices.REJECTED, "rejected")
    )

VALID_STATUS_CHOICES = (
     (StatusChoices.DRAFT,  ugettext_lazy('MODEL_STATUS_DRAFT')),
     (StatusChoices.PENDING_REVIEW,  ugettext_lazy('MODEL_STATUS_PENDING_REVIEW')),
     (StatusChoices.PUBLISHED,  ugettext_lazy('MODEL_STATUS_PUBLISHED')),
     (StatusChoices.APPROVED,  ugettext_lazy('MODEL_STATUS_APPROVED'))
)

LANGUAGE_CHOICES = (
     ('en',  ugettext_lazy( 'MODEL-LANGUAJE-EN' )),
     ('es',  ugettext_lazy( 'MODEL-LANGUAJE-ES' ))
)

ODATA_LICENSES = (
    ('', ugettext_lazy('APP-SELECTOPTION-TEXT')),
    (ugettext_lazy('APP-LICENSES-CONTENT'), (
        ('http://creativecommons.org/licenses/by/4.0/', 'Attribution (CC BY)'),
        ('http://creativecommons.org/licenses/by-sa/4.0/', 'Attribution ShareAlike (CC BY-SA)'),
        ('http://www.gnu.org/licenses/fdl-1.3.en.html', 'The GNU Free Documentation License')
    )),
    (ugettext_lazy('APP-LICENSES-DATA'), (
        ('http://opendefinition.org/licenses/odc-pddl/', 'Open Data Commons Public Domain Dedication and Licence (PDDL)'),
        ('http://opendatacommons.org/licenses/by/','Open Data Commons Attribution License'),
        ('http://opendatacommons.org/licenses/odbl/','Open Data Commons Open Database License (ODbL)'),
        ('http://creativecommons.org/publicdomain/zero/1.0/','Creative Commons CC0 Public Domain Dedication')
    ))
)

ODATA_FREQUENCY = Choices(
    ('', ugettext_lazy('APP-SELECTOPTION-TEXT')),
    ("yearly", ugettext_lazy('APP-YEARLY-TEXT')),
    ("monthly", ugettext_lazy('APP-MONTHLY-TEXT')),
    ("weekly", ugettext_lazy('APP-WEEKLY-TEXT')),
    ("daily", ugettext_lazy('APP-DAILY-TEXT')),
    ("hourly", ugettext_lazy('APP-HOURLY-TEXT')),
    ("ondemand", ugettext_lazy('APP-ONDEMAND-TEXT')),
    # ("other", ugettext_lazy('APP-OTHER-TEXT')),
)


class SourceImplementationChoices():
    HTML = 0
    SOAP = 1
    DALLAS = 2
    XML = 3
    XLS = 4
    PDF = 5
    DOC = 6
    ODT = 7
    ODP = 8
    ODS = 9
    CSV = 10
    KML = 11
    KMZ = 12
    GIS0 = 13
    REST = 14
    GIS1 = 15
    ARC0 = 16
    IBEN = 17
    IMAGE = 18
    ZIP = 19
    TSV = 20
    PUS = 21
    TXT = 22

SOURCE_IMPLEMENTATION_CHOICES = (
     (SourceImplementationChoices.HTML, 'HTML')
    ,(SourceImplementationChoices.SOAP, 'SOAP/XML')
    ,(SourceImplementationChoices.DALLAS, 'DALLAS')
    ,(SourceImplementationChoices.XML, 'XML')
    ,(SourceImplementationChoices.XLS, 'XLS')
    ,(SourceImplementationChoices.PDF, 'PDF')
    ,(SourceImplementationChoices.DOC, 'DOC')
    ,(SourceImplementationChoices.ODT, 'ODT')
    ,(SourceImplementationChoices.ODP, 'ODP')
    ,(SourceImplementationChoices.ODS, 'ODS')
    ,(SourceImplementationChoices.CSV, 'CSV')
    ,(SourceImplementationChoices.KML, 'KML')
    ,(SourceImplementationChoices.KMZ, 'KMZ')
    ,(SourceImplementationChoices.GIS0, 'geoportal/GetRecords')
    ,(SourceImplementationChoices.REST, 'REST/JSON')
    ,(SourceImplementationChoices.GIS1, 'geoportal/getxml')
    ,(SourceImplementationChoices.ARC0, 'MapServer/find')
    ,(SourceImplementationChoices.IBEN, 'iBencinas')
    ,(SourceImplementationChoices.IMAGE, 'IMAGE')
    ,(SourceImplementationChoices.ZIP, 'ZIP')
    ,(SourceImplementationChoices.TSV, 'TSV')
    ,(SourceImplementationChoices.TXT, 'TXT')
    ,(SourceImplementationChoices.PUS, 'PublicStuff')
)

SOURCE_IMPLEMENTATION_EXTENSION_CHOICES = (
     (SourceImplementationChoices.HTML, ["html", "htm"] )
    #,(SourceImplementationChoices.SOAP, 'SOAP/XML')
    #,(SourceImplementationChoices.DALLAS, 'DALLAS')
    ,(SourceImplementationChoices.XML, ["xml"])
    ,(SourceImplementationChoices.XLS, ["xlsx", "xlsm", "xls", "xltx", "xltm", "xlsb", "xlam", "xll"])
    ,(SourceImplementationChoices.PDF, ["pdf"])
    ,(SourceImplementationChoices.DOC, ["doc", "docx", "docm", "dotx", "dotm"])
    ,(SourceImplementationChoices.ODT, ["odt"])
    #,(SourceImplementationChoices.ODP, 'ODP')
    ,(SourceImplementationChoices.ODS, ["ods"])
    ,(SourceImplementationChoices.CSV, ["csv"])
    ,(SourceImplementationChoices.KML, ["kml"])
    ,(SourceImplementationChoices.KMZ, ["kmz"])
    #,(SourceImplementationChoices.GIS0, 'geoportal/GetRecords')
    #,(SourceImplementationChoices.REST, 'REST/JSON')
    #,(SourceImplementationChoices.GIS1, 'geoportal/getxml')
    #,(SourceImplementationChoices.ARC0, 'MapServer/find')
    #,(SourceImplementationChoices.IBEN, 'iBencinas')
    ,(SourceImplementationChoices.IMAGE, ["png", "jpg", "jpeg", "gif"])
    ,(SourceImplementationChoices.ZIP, ["zip", "gz", "tar"])
    ,(SourceImplementationChoices.TSV, ["tsv", "tab"])
    #,(SourceImplementationChoices.PUS, 'PublicStuff')
    ,(SourceImplementationChoices.TXT, ["txt"])
)

SOURCE_EXTENSION_LIST = sorted([extension for source_id, extensions in SOURCE_IMPLEMENTATION_EXTENSION_CHOICES
                           for extension in extensions])

SOURCE_IMPLEMENTATION_MIMETYPE_CHOICES = (
     (SourceImplementationChoices.HTML, ["text/html"])
    #,(SourceImplementationChoices.SOAP, 'SOAP/XML')
    #,(SourceImplementationChoices.DALLAS, 'DALLAS')
    ,(SourceImplementationChoices.XML, ["text/xml"])
    ,(SourceImplementationChoices.XLS, ["application/vnd.ms-excel",
                                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"])
    ,(SourceImplementationChoices.PDF, ["application/pdf"])
    ,(SourceImplementationChoices.DOC, ["application/vnd.ms-xpsdocument",
                                        "application/msword"])
    ,(SourceImplementationChoices.ODT, ["application/vnd.oasis.opendocument.text",
                                        "application/vnd.oasis.opendocument.text-web"])
    #,(SourceImplementationChoices.ODP, 'ODP')
    ,(SourceImplementationChoices.ODS, ["application/vnd.oasis.opendocument.spreadsheet"])
    ,(SourceImplementationChoices.CSV, ["text/x-comma-separated-values",
                                        "text/csv"])
    ,(SourceImplementationChoices.KML, ["application/vnd.google-earth.kml+xml"])
    #,(SourceImplementationChoices.KMZ, 'KMZ')
    #,(SourceImplementationChoices.GIS0, 'geoportal/GetRecords')
    #,(SourceImplementationChoices.REST, 'REST/JSON')
    #,(SourceImplementationChoices.GIS1, 'geoportal/getxml')
    #,(SourceImplementationChoices.ARC0, 'MapServer/find')
    #,(SourceImplementationChoices.IBEN, 'iBencinas')
    ,(SourceImplementationChoices.IMAGE, ["image/jpeg",
                                          "image/png",
                                          "image/gif"])
    ,(SourceImplementationChoices.ZIP, ["application/zip",
                                        "application/x-gzip",
                                        "application/x-tar"])
    ,(SourceImplementationChoices.TSV, ["text/tab-separated-values"])
    #,(SourceImplementationChoices.PUS, 'PublicStuff')
    ,(SourceImplementationChoices.TXT, ["text/plain"])
)

SOURCE_MIMETYPE_LIST = sorted([mimetype for source_id, mimetypes in SOURCE_IMPLEMENTATION_MIMETYPE_CHOICES
                           for mimetype in mimetypes])

DATASTREAM_IMPL_VALID_CHOICES = [
    SourceImplementationChoices.HTML,
    SourceImplementationChoices.XML, 
    SourceImplementationChoices.XLS, 
    SourceImplementationChoices.CSV, 
    SourceImplementationChoices.KML, 
    SourceImplementationChoices.KMZ, 
    SourceImplementationChoices.DOC,
    SourceImplementationChoices.TSV,
    SourceImplementationChoices.TXT]

# These are the impl_type that are not valid to create a Data View from Self Publish
DATASTREAM_IMPL_NOT_VALID_CHOICES = list( set(dict(SOURCE_IMPLEMENTATION_CHOICES).keys()) - set(DATASTREAM_IMPL_VALID_CHOICES) )

WEBSERVICE_IMPLEMENTATION_CHOICES = (
    (SourceImplementationChoices.REST, 'REST/JSON'),
    (SourceImplementationChoices.SOAP, 'SOAP/XML')
)


class CollectTypeChoices():
    SELF_PUBLISH = 0 # an uploaded file
    URL = 1 # a web page for scrape internal tables
    WEBSERVICE = 2 # api or webservice

COLLECT_TYPE_CHOICES = (
     (CollectTypeChoices.SELF_PUBLISH, 'SELF PUBLISH') # an uploaded file
    ,(CollectTypeChoices.URL, 'URL') # a web page for scrape internal tables
    ,(CollectTypeChoices.WEBSERVICE, 'WEBSERVICE') # api or webservice
)

COLLECT_TYPE_FILTERABLES = [
     CollectTypeChoices.SELF_PUBLISH
    ,CollectTypeChoices.URL
]

COUNTRY_CHOICES = (
    ('US', ugettext_lazy( 'MODEL-COUNTRY-US'))
    ,('AR', ugettext_lazy( 'MODEL-COUNTRY-AR' ))
    ,('CL', ugettext_lazy( 'MODEL-COUNTRY-CL' ))
    ,('BR', ugettext_lazy( 'MODEL-COUNTRY-BR' ))
    ,('UY', ugettext_lazy( 'MODEL-COUNTRY-UY' ))
    ,('MX', ugettext_lazy( 'MODEL-COUNTRY-MX' ))
    ,('CR', ugettext_lazy( 'MODEL-COUNTRY-CR' ))
    ,('999', ugettext_lazy( 'MODEL-COUNTRY-OC' ))
)

OCUPATION_CHOICES = (
    ('00', ugettext_lazy( 'MODEL-OCUPATION-FI' ))
    ,('01', ugettext_lazy( 'MODEL-OCUPATION-AN' ))
    ,('02', ugettext_lazy( 'MODEL-OCUPATION-MA' ))
    ,('03', ugettext_lazy( 'MODEL-OCUPATION-EN' ))
    ,('04', ugettext_lazy( 'MODEL-OCUPATION-OT' ))
)

THRESHOLD_NAME_CHOICES = (
     ('self_publish.can_upload', 'self_publish.can_upload')
    ,('private_datastream.can_create', 'private_datastream.can_create')
    ,('api.account_monthly_calls', 'api.account_monthly_calls')
    ,('workspace.create_user_limit', 'workspace.create_user_limit')
    ,('workspace.create_dataset_limit', 'workspace.create_dataset_limit')
)

ACCOUNT_PREFERENCES_AVAILABLE_KEYS = (
    #STRING codigo CSS ---------------------------
     ('ds.detail.full.css', 'ds.detail.full.css') 
    ,('ds.embed.full.css', 'ds.embed.full.css')
    ,('chart.detail.full.css', 'chart.detail.full.css')
    ,('chart.embed.full.css', 'chart.embed.full.css')
    ,('db.detail.full.css', 'db.detail.full.css')
    ,('search.full.css', 'search.full.css')
    ,('home.full.css', 'home.full.css')
    ,('developers.full.css', 'developers.full.css')

    # STRING codigo JS ---------------------------
    ,('ds.detail.full.javascript', 'ds.detail.full.javascript') 
    ,('ds.embed.full.javascript', 'ds.embed.full.javascript')
    ,('chart.detail.full.javascript', 'chart.detail.full.javascript')
    ,('chart.embed.full.javascript', 'chart.embed.full.javascript')
    ,('db.detail.full.javascript', 'db.detail.full.javascript')
    ,('search.full.javascript', 'search.full.javascript')
    ,('home.full.javascript', 'home.full.javascript')
    ,('developers.full.javascript', 'developers.full.javascript')

    
    ,('account.name', 'account.name') 
    ,('account.bio', 'account.bio') 
    ,('account.link', 'account.link')
    ,('account.logo', 'account.logo')
    ,('account.url', 'account.url')
    ,('account.domain', 'account.domain')
    ,('account.api.domain', 'account.api.domain')
    ,('account.hot.datastreams', 'account.hot.datastreams')
    ,('account.hot.visualizations', 'account.hot.visualizations')
    ,('account.favicon', 'account.favicon')
    ,('account.page.titles', 'account.page.titles')
    ,('account.comments', 'account.comments')
    ,('account.email', 'account.email')
    ,('account.contact.person.name', 'account.contact.person.name')
    ,('account.contact.person.email', 'account.contact.person.email')
    ,('account.contact.person.phone', 'account.contact.person.phone')
    ,('account.contact.person.country', 'account.contact.person.country')
    ,('account.language', 'account.language')
    ,('branding.header', 'branding.header')
    ,('account.header.uri', 'account.header.uri')
    ,('account.header.height', 'account.header.height')
    ,('branding.footer', 'branding.footer')
    ,('account.footer.uri', 'account.footer.uri')
    ,('account.footer.height', 'account.footer.height')
    ,('enable.embed.options', 'enable.embed.options')
    ,('enable.junar.footer', 'enable.junar.footer')
    ,('account.enable.sharing', 'account.enable.sharing') # BOOLEAN
    ,('account.enable.notes', 'account.enable.notes') # BOOLEAN
    ,('account.title.color', 'account.title.color')
    ,('account.button.bg.color', 'account.button.bg.color')
    ,('account.button.border.color', 'account.button.border.color')
    ,('account.button.font.color', 'account.button.font.color')
    ,('account.mouseover.bg.color', 'account.mouseover.bg.color')
    ,('account.mouseover.border.color', 'account.mouseover.border.color')
    ,('account.mouseover.title.color', 'account.mouseover.title.color')
    ,('account.mouseover.text.color', 'account.mouseover.text.color')
    ,('account.header.bg.color', 'account.header.bg.color')
    ,('account.header.border.color', 'account.header.border.color')
    ,('account.has.home', 'account.has.home')
    ,('account.home', 'account.home')
    ,('account.home.featured.content', 'account.home.featured.content')
    ,('account.home.main.content', 'account.home.main.content')
    ,('account.home.search.content', 'account.home.search.content')
    ,('account.home.filters', 'account.home.filters')
    ,('account.home.footer.left', 'account.home.footer.left')
    ,('account.home.footer.right', 'account.home.footer.right')
    ,('account.home.noslider', 'account.home.noslider')
    ,('account.default.category', 'account.default.category')
    ,('account.pivottable', 'account.pivottable')
    ,('account.bucket.name', 'account.bucket.name')
    ,('account.dataset.download', 'account.dataset.download')
    ,('account.hidelastupdate', 'account.hidelastupdate')
    ,('account.has.db.sidebar', 'account.has.db.sidebar')
    ,('account.embed.powered.by', 'account.embed.powered.by')
    ,('account.pivottable.helplink', 'account.pivottable.helplink')
    ,('account.footer.opendatalicense', 'account.footer.opendatalicense')
    ,('account.preview', 'account.preview')
    ,('account.bigdata.namespace', 'account.bigdata.namespace')
    ,('account.transparency.domain', 'account.transparency.domain')
    ,('account.transparency.country', 'account.transparency.country')
    ,('account.transparency.createdcategories', 'account.transparency.createdcategories')
    ,('account.transparency.categories', 'account.transparency.categories')
    ,('account.contact.dataperson.email', 'account.contact.dataperson.email')
    ,('account.dataset.showhome', 'account.dataset.showhome')
    ,('account.description.enhancement', 'account.description.enhancement')
    ,('account.search.tips', 'account.search.tips')

    # TODO: Mover al plugin
    ,('account.featured.dashboards', 'account.featured.dashboards'),

    # https for microsites or api
    ('account.microsite.https', 'account.microsite.https'),
    ('account.api.https', 'account.api.https'),
)

API_APPLICATION_TYPE_CHOICES = (
    ('01', 'UNLIMITED - 01'),
)


class TicketChoices:
    def __init__(self):
        pass

    PASSWORD_RECOVERY = 'PASS'
    API_AUTHORIZATION = 'API'
    USER_ACTIVATION = 'USER_ACTIVATION'
