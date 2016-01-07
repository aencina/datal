from abc import ABCMeta, abstractmethod

from django.conf import settings
from core.exceptions import MailServiceNotFoundException
import importlib

class MailService():
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def send_welcome_mail(self, user, link, company):
        """ Para usuarios nuevos del sistema """
        pass

    @abstractmethod
    def list_subscribe(self, user, language='es', extradata={}):
        """ Suscribir a la lista de usuarios del sistema"""
        pass

mail_service = None
class_name = settings.EMAIL_SERVICE.split('.')[-1]
module_name = settings.EMAIL_SERVICE.split('.{}'.format(class_name))[0]
mail_service = getattr(importlib.import_module(module_name), class_name)
