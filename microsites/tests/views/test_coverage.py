from django.test import SimpleTestCase
from django.test import Client
from django.core.management import call_command
from core import models

#coverage run --source=microsites manage.py test --settings="microsites.settings"  --nologcapture --where=microsites/
#coverage report --skip-covered -m

class CommonViewTestCase(SimpleTestCase):
    fixtures = [
        './tests/fixtures/accountlevel.json',
        './tests/fixtures/account.json',
        './tests/fixtures/preference.json',
        './tests/fixtures/user.json',
        './tests/fixtures/role.json',
        './tests/fixtures/privilege.json',
        './tests/fixtures/grant.json',
        './tests/fixtures/application.json',
        './tests/fixtures/category.json',
        './tests/fixtures/categoryi18n.json',
        './tests/fixtures/dataset.json',
        './tests/fixtures/dataseti18n.json',
        './tests/fixtures/datasetrevision.json',
        './tests/fixtures/datastream.json',
        './tests/fixtures/datastreami18n.json',
        './tests/fixtures/datastreamrevision.json',
        './tests/fixtures/tag.json',
        './tests/fixtures/visualization.json',
        './tests/fixtures/visualizationi18n.json',
        './tests/fixtures/visualizationrevision.json',
    ]


    def setUp(self):
        call_command('loaddata', *self.fixtures)

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
        resp = self.client.post('/home/update_list', data={ 'order': 1, 'category_filters': 'Finanzas', 'type':'vz,'}, follow=True, SERVER_NAME="opencity.site.demo.junar.com")
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
        self.assertEqual(models.Account.objects.get(pk=1).get_preference('account.dataset.show'), True)
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

    def test_rest_datastream_coverage(self):
        # Basic path
        resp = self.client.get('/rest/datastreams/61453/data.json?page=0&rp=50&sortname=&sortorder=asc&query=', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # Basic path
        resp = self.client.get('/rest/datastreams/61453/data.grid?page=0&rp=50&sortname=&sortorder=asc&query=', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

    def test_rest_visualization_coverage(self):
        # Basic path
        resp = self.client.get('/rest/charts/5608/data.json', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        # maps
        resp = self.client.get('/rest/maps/5608/data.json', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

    def test_branded_coverage(self):
        # Basic path
        resp = self.client.get('/branded/css/viewDataStream.view/1.css', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/js/viewDataStream.embed/1.js', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/css/search.search/1.css', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/css/chart_manager.embed/1.css', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/js/loadHome.load/1.js', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/css/manageDeveloper.filter/1.css', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/css/chart_manager.view/1.css', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/js/viewDashboards.view/1.js', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/css/manageDatasets.view/1.css', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/branded/css/asdfasf/1.css', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp.status_code, 404)

        resp2 = self.client.get('/branded/newcss/manageDatasets.view/1.css', follow=True, SERVER_NAME="microsites.dev:8080")
        self.assertEqual(resp2.status_code, 200)

        resp2 = self.client.get('/branded/newcss/manageDatasets.view/1.css', follow=True, SERVER_NAME="junarprueba.site.staging.junar.com")
        self.assertEqual(resp2.status_code, 200)
