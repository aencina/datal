# -*- coding: utf-8 -*-
"""
Wrappers para sftp y s3  
Si quiere agregar el suyo extienda la clase datastore e implemente los metodos abstractos. Luego definalo en core/settings.py, instancielo 
y asignelo a la variable active
"""
import logging
import sftp

from django.conf import settings

from abc import ABCMeta, abstractmethod
from uuid import uuid4 as UUID
from paramiko.client import SSHClient, AutoAddPolicy

from core.exceptions import *

logger = logging.getLogger(__name__)


class datastore:
    """ save and recovery files from another services"""
    def create(self, bucket_name, data, account_id, user_id):
        pass

    def build_url(self, bucket_name, key, response_headers=None, force_http=False):
        pass

    def update_s3_file(self, request, generated_name):
        pass

    def save_to_s3(self, bucket_name, keyname, data):
        pass


class Datastore:
    """ Clase abstracta de la cual todos los tipos de datastore deben heredar """
    __metaclass__ = ABCMeta

    @abstractmethod 
    def create(self, account_id, user_id, bucket_name, file_data):
        pass

    @abstractmethod 
    def build_url(self, **kwargs):
        pass

    @abstractmethod     
    def update(self, bucket_name, end_point, file_data):
        pass


class s3(Datastore):
    """ Crea y actualiza archivos en S3"""

    def __init__(self):
        self.connection = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)

    def build_url(self, **kwargs):
        pass

    def create(self, bucket_name, file_data, account_id, user_id):
        """
        Crea un archivo en S3 dentro de un bucket. La ruta hacia el archivo se genera dando vuelta los ids de la
        cuenta y el usuario. El nombre del archivo con UUID
        """
        logger = logging.getLogger(__name__)
        logger.info(bucket_name)
        #try:
        end_point = "%s/%s/%d" %(str(account_id)[::-1], str(user_id)[::-1], UUID())
        self._save(bucket_name, end_point, file_data)

        logger.error('S3 saved to: %s ' % end_point)

        return end_point
        #except Exception, e:
        #    logger.error('S3CreateException: %s IN %s [%s, %s, %s]' % (str(e), end_point, account_id, user_id,
        #                                                               bucket_name))
        #    raise S3CreateException(e)

    def upload(self, bucket_name, uuid, file_data, account_id):
        """
        Crea un archivo en S3 dentro de un bucket. La ruta hacia el archivo se genera dando vuelta los ids de la
        cuenta y el usuario. El nombre del archivo con UUID
        """
        logger = logging.getLogger(__name__)
        if not uuid: uuid = UUID() # pueden pasarme un nombre de archivo especial
        
        #try:
        end_point = "%s/%s" % (str(account_id), uuid)
        try:
            self._save(bucket_name, end_point, file_data)
            logger.info('S3 saved to: %s ' % end_point)
        except Exception, e:
            logger.error('Error saving to S3: %s :: %s, %s,%s,%s,%s' % (str(e), end_point, bucket_name, uuid, file_data, account_id))
            raise
            
        return end_point
        
        
    def generate_url(self, bucket_name, **kwargs):
        """ Genera una url para poder acceder a un archivo desde afuera """
        key = kwargs['key']
        response_headers = kwargs.get('response_headers', None)
        force_http = kwargs.get('force_http', True)

        return self.connection.generate_url(300, 'GET', bucket_name, key, response_headers = response_headers,
                                            force_http=force_http)
    
    def update(self, bucket_name, file_name, file_data):
        """ Actualiza un archivo en S3. El nombre del archivo se encuentra precedido por la ruta hacia el mismo."""        
        try:
            self._save(bucket_name, file_name, file_data)
        except Exception, e:
            raise S3UpdateException(e)

    def _save(self, bucket_name, end_point, File):
        k = Key(self.connection.get_bucket(bucket_name))
        k.key = end_point
        k.set_contents_from_file(File)
        
        
class datastore_sftp(datastore):
    """ collect of independent functions, not really a Class """
    def __init__(self):
        # Remote path for saving all resources
        self.base_folder = settings.SFTP_DATASTORE_REMOTEBASEFOLDER
        # Local base folder for saving temporary files before upload
        self.tmp_folder = settings.SFTP_DATASTORE_LOCALTMPFOLDER
        # url for donwloading resources
        self.public_base_url = settings.SFTP_BASE_URL
        self.buckets = []
        self.connection = None
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh_client.load_system_host_keys()
        self.sftp = None

    def connect(self):
        """ don't use at INIT because it hangs all application"""
        logger = logging.getLogger(__name__)
        logger.error('Connecting SFTP %s:%s (%s, %s)' %(
            settings.SFTP_DATASTORE_HOSTNAME,
            settings.SFTP_DATASTORE_PORT,
            settings.SFTP_DATASTORE_USER,
            settings.SFTP_DATASTORE_PASSWORD)
        )

        # TODO: Remove
        con = sftp.Connection(
            host=settings.SFTP_DATASTORE_HOSTNAME,
            port=settings.SFTP_DATASTORE_PORT,
            username=settings.SFTP_DATASTORE_USER,
            password=settings.SFTP_DATASTORE_PASSWORD,
            log=True
        )
        self.connection = con
        #

        self.ssh_client.connect(
            settings.SFTP_DATASTORE_HOSTNAME,
            port=settings.SFTP_DATASTORE_PORT,
            username=settings.SFTP_DATASTORE_USER,
            password=settings.SFTP_DATASTORE_PASSWORD
        )
        self.sftp = self.ssh_client.open_sftp()

        # list all buckets (folders)
        try:
            self.buckets = self.sftp.listdir(path=self.base_folder)
            logger.error('Buckets: %s' %str(self.buckets))
        except Exception, e:
            logger.error('Error Connecting SFTP %s' % str(e))
            self.sftp.close()

    def create(self, bucket_name, data, account_id, user_id):
        """ upload data (file) to the bueck_name folder, Return a key for identify this file
        data is a file_name
        """
        # We save as buket_name / account_id / user_id / UUID
        folder = "%s/%s" % (str(account_id)[::-1], str(user_id)[::-1])
        uuid = str(UUID())
        key = "%s/%s" % (folder, uuid)
        final_remote_folder = '%s/%s/%s' % (self.base_folder, bucket_name, folder)
        self.save_checking_path(uploaded_file=data, folder=final_remote_folder, file_name=uuid)
        return key

    def upload(self, bucket_name, file_name, file_data, account_id):
        """ update file for existing resource """
        logger.info(file_name)
        remote_path = "%s/%s/%s/" % (self.base_folder, bucket_name, str(account_id))
        remote_file = "%s/%s" % (remote_path, file_name)
        self.connect()
        self.ssh_client.exec_command('mkdir -p %s' % remote_path)
        logger.info(remote_path)
        logger.info(remote_file)
        self.sftp.putfo(file_data, remotepath=remote_file)
        
    def save_checking_path(self, uploaded_file, folder, file_name):
        """ ensure path and save """
        self.connect()
        self.ssh_client.exec_command('mkdir -p %s' % folder)
        final_path = '%s/%s' % (folder, file_name)
        try:
            self.sftp.putfo(uploaded_file, remotepath=final_path)
        except IOError, e:
            logger.error('Error saving file to SFTP %s' % str(e))
            raise e

    def build_url(self, bucket_name, key, response_headers=None, force_http=True):
        """ return an URL for downloading resource
        S3 allows expire seconds if it's a private resource, we don't #TODO """
        return '%s/%s/%s' % (self.public_base_url, bucket_name, key)

    def update_s3_file(self, request, generated_name):
        """ update file for existing resource """
        self.connect()
        data = request.FILES['Filedata']
        final_remote_folder = "%s/%s/%s" % (self.base_folder, request.bucket_name, generated_name)
        self.connection.put(data.temporary_file_path(), remotepath = final_remote_folder)

    def save_to_s3(self, bucket_name, keyname, data):
        """ save file to server, like 'create' function """
        self.connect()
        import os
        file_name = os.path.basename(keyname)
        folder_name = os.path.dirname(keyname)
        final_remote_folder = '%s/%s/%s' % (self.base_folder, bucket_name, folder_name)
        #save uploaded file (if file is small DJANGO save it in memory, not at temporary folder)
        logger.info('Saving uploaded at %s (%s - %s)' % (data.temporary_file_path(),final_remote_folder, file_name ))
        self.save_checking_path(local_path=data.temporary_file_path(), folder=final_remote_folder, file_name=file_name)

active_datastore = None
if settings.USE_DATASTORE == 's3':
    # imports for S3
    from boto.s3.connection import S3Connection
    from boto.s3.key import Key

    active_datastore = s3()

elif settings.USE_DATASTORE == 'sftp':
    active_datastore = datastore_sftp()
else:
    raise DatastoreNotFoundException()
