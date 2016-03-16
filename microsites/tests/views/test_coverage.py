from django.test import SimpleTestCase
from django.test import Client
from django.core.management import call_command
from core import models

#coverage run --source=microsites manage.py test --settings="microsites.settings"  --nologcapture --where=microsites/
#coverage report --skip-covered -m

class CommonViewTestCase(SimpleTestCase):
    fixtures = [
        '../core/fixtures/accountlevel.json',
        '../core/fixtures/account.json',
        '../core/fixtures/preference.json',
        '../core/fixtures/user.json',
        '../core/fixtures/role.json',
        '../core/fixtures/privilege.json',
        '../core/fixtures/grant.json',
        '../core/fixtures/application.json',
        '../core/fixtures/category.json',
        '../core/fixtures/categoryi18n.json',
        '../core/fixtures/dataset.json',
        '../core/fixtures/dataseti18n.json',
        '../core/fixtures/datasetrevision.json',
        '../core/fixtures/datastream.json',
        '../core/fixtures/datastreami18n.json',
        '../core/fixtures/datastreamrevision.json',
        '../core/fixtures/tag.json',
        '../core/fixtures/visualization.json',
        '../core/fixtures/visualizationi18n.json',
        '../core/fixtures/visualizationrevision.json',
    ]

    def test_home_coverage(self):
        # Basic path
        resp = self.client.get('/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/', follow=True, SERVER_NAME="junarprueba.site.staging.junar.com")
        self.assertEqual(resp.status_code, 200)

        # HTTP_ACCEPT_LANGUAGE https://github.com/datal-org/datal/blob/develop/microsites/middlewares/auth.py#L24
        resp = self.client.get('/', follow=True, SERVER_NAME="microsites.dev:8080", HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(resp.status_code, 200)

        # REQUEST_URI https://github.com/datal-org/datal/blob/develop/microsites/middlewares/ioc.py#L53
        resp = self.client.get('/', follow=True, SERVER_NAME="microsites.dev:8080", REQUEST_URI='/')
        self.assertEqual(resp.status_code, 200)

        # language https://github.com/datal-org/datal/blob/develop/microsites/middlewares/locale.py#L10
        resp = self.client.get('/?locale=en', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # No home, redirect
        cabierta = models.Account.objects.get(id=1)
        home = models.Preference.objects.get(account=cabierta, key='account.home')
        
        home_value = home.value
        home.value = ''
        home.save()
        
        resp = self.client.get('/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain[-1][0], 'http://microsites.dev:8080/search/')
        
        home.value = home_value
        home.save()

        # No account
        resp = self.client.get('/', follow=True, SERVER_NAME="unanoexiste.junar.com")
        self.assertEqual(resp.status_code, 403)

    def test_update_list_coverage(self):
        resp = self.client.post('/home/update_list', follow=True, SERVER_NAME="microsites.dev:8080",
            data={ 'order': 0, 'category_filters': '', 'entity_filters': '2', 'type_filters':'vz'} )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/home/update_list', data={ 'order': 1, 'category_filters': 'Finanzas'}, follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # No federated account
        resp = self.client.post('/home/update_list', data={ 'order': 1, 'category_filters': 'Finanzas'}, follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)

        # Validation fail
        resp = self.client.post('/home/update_list', data={ 'type': '23$%*43'}, follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)


    def test_update_categories_coverage(self):
        resp = self.client.get('/home/update_categories', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/home/update_categories?account_id=2', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

    def test_browse_coverage(self):
        # Basic path
        resp = self.client.get('/datastreams/category/finanzas/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

    def test_search_coverage(self):
        # Basic path
        resp = self.client.get('/search/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # sin dataset       
        resp = self.client.get('/search', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)

        # sin dataset       
        resp = self.client.get('/search/?resource=dt', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 404)

        # empty result       
        resp = self.client.get('/search/?page=4', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # caracteres raors
        resp = self.client.get('/search/?q=-?', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # invlid form       
        resp = self.client.get('/search/?tag=--', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 404)

    def test_sitemap_coverage(self):
        resp = self.client.get('/sitemap', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

    def setUp(self):
        call_command('loaddata', *self.fixtures)

    def test_custom_coverage(self):
        resp = self.client.get('/a/comoUsarlo', follow=True, SERVER_NAME="junarprueba.site.staging.junar.com")
        self.assertEqual(resp.status_code, 200)

        # no existe
        resp = self.client.get('/a/asdfasdf/', follow=True, SERVER_NAME="junarprueba.site.staging.junar.com")
        self.assertEqual(resp.status_code, 404)

    def test_is_live_coverage(self):
        resp = self.client.get('/is_live', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)

    def test_catalog_coverage(self):
        resp = self.client.get('/catalog.xml', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)

    def test_visualization_coverage(self):
        # Basic path
        resp = self.client.get('/visualizations/1736/-', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # not found
        resp = self.client.get('/visualizations/1742/-', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 404)

        # mapchart
        resp = self.client.get('/visualizations/1742/-', follow=True, SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 200)
    
    def test_visualization_embed_coverage(self):
        # Basic path
        resp = self.client.get('/visualizations/embed/NOMIN-DE-INICI-DE-INVER/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # not found 404
        resp = self.client.get('/visualizations/embed/MAP-OF-TRAFF-ACCID/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

    def test_datastream_coverage(self):
        # Basic path
        resp = self.client.get('/datastreams/43445/-', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)
    
    def test_datastream_embed_coverage(self):
        # Basic path
        resp = self.client.get('/datastreams/embed/OPERA-DEL-EN-MILLO-DE/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # not found 404
        resp = self.client.get('/datastreams/embed/ASDFJASDFAS/', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

    def test_dataset_coverage(self):
        # Basic path
        resp = self.client.get('/datasets/61634/-', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)
    
    def test_dataset_download_coverage(self):
        # url descarga
        resp = self.client.get('/datasets/72539-a.download/', SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 302)

        # url no descarga
        resp = self.client.get('/datasets/72545-a.download/', SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 403)

        # Self-publish descarga
        with self.settings(USE_DATASTORE=''):
            resp = self.client.get('/datasets/72543-a.download/', SERVER_NAME="opencity.site.demo.junar.com")
            self.assertEqual(resp.status_code, 200)

        # Self-publish No descarga
        resp = self.client.get('/datasets/72537-a.download/', SERVER_NAME="opencity.site.demo.junar.com")
        self.assertEqual(resp.status_code, 403)

        # not found 404
        resp = self.client.get('/datasets/23414231-a.download', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 404)