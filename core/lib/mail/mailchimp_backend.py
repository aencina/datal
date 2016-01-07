"""
Python library for send mailchimp campaigns
Mandrill is the 'transactional tool' (few and personalizated emails)
"""
import mailchimp
import mandrill
import logging

from core.lib.mail.mail import MailService
from django.conf import settings


class MailchimpMailService(MailService):

    def _get_mandrill(self):
        """ get the mandrill object """
        return mandrill.Mandrill(settings.MANDRILL['api_key'])

    def _get_mailchimp(self):
        """ get the mailchip object """
        try:
            m = mailchimp.Mailchimp(settings.MAILCHIMP['api_key'])
        except Exception, e:
            logger = logging.getLogger(__name__)
            logger.error('MailChimp error (%s) (%s)' % ( str(e), repr(e) ) )
            m = None
        return m
            
    def send_welcome_mail(self, user, link, company): 
        """ Notify new admin """
        ma = self._get_mandrill()
    
        avars = [
            {'name':'FNAME', 'content': user.name},
            {'name': 'ADMINNAME', 'content': user.nick},
            {'name': 'COMPANY', 'content': company},
            {'name': 'LINK', 'content': link},
            {'name':'TWITTER:PROFILEURL', 'content': settings.TWITTER_PROFILE_URL},
            {'name':'FACEBOOK:PROFILEURL', 'content': settings.FACEBOOK_PROFILE_URL},
            {'name':'LIST:COMPANY', 'content': settings.MAIL_LIST['LIST_COMPANY']},
            {'name':'LIST:DESCRIPTION', 'content': settings.MAIL_LIST['LIST_DESCRIPTION']},
            {'name':'UNSUB', 'content': settings.MAIL_LIST['LIST_UNSUBSCRIBE']},
            {'name':'UPDATE_PROFILE', 'content': settings.MAIL_LIST['LIST_UPDATE_PROFILE']}
        ]

        to = [{'email': user.email}]

        if user.language == "es":
            tmpl = settings.MAIL_LIST['WELCOME_TEMPLATE_ES']
            sbj = 'Nueva cuenta en '+ APPLICATION_DETAILS['name']
        else:
            tmpl = settings.MAIL_LIST['WELCOME_TEMPLATE_EN']
            sbj = 'New '+ APPLICATION_DETAILS['name'] +' account'

        message = {'subject':sbj, 'to': to,
                   'from_name': company,
                   'from_email':APPLICATION_DETAILS['mail'],
                   'merge': True,
                   'merge_vars': [{'rcpt': user.email,'vars': avars }]
        }
    
        result = ma.messages.send_template(template_name=tmpl, template_content=[], message=message, async=False,
                                           ip_pool='Main Pool')
        if result[0]["reject_reason"] == None:
            return True
        else:
            logger = logging.getLogger(__name__)
            logger.error("Failed to send email (%s)" % result[0]["reject_reason"])
            return False    

    def list_subscribe(self, user, language='es', extradata={}):
        """ add new workspace user to our mail list """
        logger = logging.getLogger(__name__)
        
        list_id = settings.MAILCHIMP['lists']['workspace_users_list'][language]['id']
        email = user.email
    
        try:
            fname  = user.name.split(' ')[0]
            lname  = ' '.join(user.name.split(' ')[1:])
        except:
            fname  = user.name
            lname  = ''
    
        user_type="Workspace"
        mergetags = {'FNAME': fname, 'LNAME': lname, 'MMERGE7': user_type, 'MMERGE6':extradata["country"],
                     'MMERGE3': extradata["company"]}
    
        # add to list
        m=self._get_mailchimp()
        if not m:
            return False
            
        try:
            m.lists.subscribe(list_id, {'email':email}, mergetags)
            return True
        except mailchimp.ListAlreadySubscribedError:
            return True
        except mailchimp.ListMergeFieldRequiredError, e:
            logger.error('You forget some mandatory fiedls: %s - %s - %s' % (str(e), repr(e), str(mergetags)))
            return False
        except mailchimp.Error, e:
            logger.error('An error occurred: %s - %s - %s' % (e.__class__, e, str(mergetags) ) )
            return False
    
        return True
