from django import forms
from django.forms.forms import Form
from core.models import *
import urllib2

logger = logging.getLogger(__name__)

class MetaForm(Form):
    def __init__(self, *args, **kwargs):
         metadata = kwargs.pop('metadata')
         super(MetaForm, self).__init__(*args, **kwargs)
         self.metadata_to_fields(metadata)

    def metadata_to_fields(self, p_meta_data):
        l_fieldInputs = {}

        try:
            import simplejson
            p_response = simplejson.loads(p_meta_data)
        except:
            return l_fieldInputs

        for l_field in p_response['fields']:
            l_name = l_field['name']
            l_label = l_field['label']
            l_isRequired = l_field['required']
            l_regex = l_field['validation']

            self.fields["cust-"+l_name] = forms.RegexField(label=l_label, max_length=256, required=l_isRequired, regex=l_regex, widget=forms.TextInput(attrs={'Name': 'cust-'+ l_name, 'validation' : l_regex , 'required': l_isRequired}))


    def output_json(self):
        l_lists = {}

        try:
            import simplejson
        except:
            return l_lists

        l_lists["field_values"] = []
        for name, field in self.fields.items():
            l_row  = {}
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
            l_row[name] = value
            l_lists["field_values"].append(l_row)

        return simplejson.dumps(l_lists)

    def set_values(self, p_meta_data):
        l_fieldInputs = {}

        try:
            import simplejson
            p_response = simplejson.loads(p_meta_data)
        except:
            return l_fieldInputs

        for l_field in p_response['field_values']:
            for key in l_field.keys():
                l_name = key
                l_value = l_field[key]
            self.fields[l_name].initial = l_value

class MimeTypeForm(forms.Form):
    url = forms.CharField(required=True)

    def get_mimetype(self, url):
        try:
            request = urllib2.Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:11.0) Gecko/20100101 Firefox/11.0"})
            connection = urllib2.urlopen(request)
            mimetype = connection.info().getheader('Content-Type').strip().replace('"', '')
            try:
                opener = urllib2.build_opener(SmartRedirectHandler())
                f = opener.open(url)
                status = f.status
                url = f.url
            except:
                status = 200
                url = url
        except Exception as e:
            logger.exception("Error en parseo de mimetype de url")
            mimetype = ''
            status = ''

        return (mimetype, status, url)