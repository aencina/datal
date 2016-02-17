# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from core.http import get_domain_with_protocol
from core.v8.factories import AbstractCommandFactory
from core.exceptions import DatasetTableNotFoundException
import urllib
import logging

logger = logging.getLogger(__name__)

class SelectStatementBuilder(object):
    def build(self, table_id):
        return '<selectStatement><Select><Column>*</Column></Select><From><Table>%s</Table></From><Where/></selectStatement>' % (table_id or 'table0')


class DataSourceBuilder(object):
    def build(self, table_id, dataset_revision_id, app):

        data = {'pId': dataset_revision_id, 'pLimit': 50}
        command = AbstractCommandFactory(app).create("load", "dt", [data])
        result = command.run()
        if not result:
            # TODO: correct handling
            raise Exception('Wrong engine answer')

        soup = BeautifulSoup(result[0])
        table = soup.find(attrs={'tableid': 'table%d' % table_id or 'table0'})
        try:
            if not table:
                raise DatasetTableNotFoundException(table_id) 
            number_of_columns = len(table.findAll('tr')[0].findAll())
        except:
            logger.error("DataSourceBuilder ERROR --> %s" % result[0])
            raise

        impl_details_xml = '<dataSource><DataStructure><Field id="%s"><type></type><format><languaje></languaje><country></country><style></style></format><Table>' % (table_id or 'table0')
        for i in range(number_of_columns):
            impl_details_xml = impl_details_xml + '<Field id="column%d"><alias></alias><type></type><format><languaje></languaje><country></country><style></style></format></Field>' % i
        impl_details_xml = impl_details_xml + '</Table></Field></DataStructure></dataSource>'
        return impl_details_xml

