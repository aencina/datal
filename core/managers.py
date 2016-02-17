import re
import types
import logging
from django.db import models, connection
from django.conf import settings
from django.core.paginator import InvalidPage
from django.core.urlresolvers import reverse
from core.utils import slugify
from core import helpers, choices

logger = logging.getLogger(__name__)


class ThresholdManager(models.Manager):

    def get_limit_by_code_and_account_id(self, code, account_id):

        try:
            return super(ThresholdManager, self).values('limit').get( account = account_id, name = code)['limit']
        except self.model.DoesNotExist:
            return super(ThresholdManager, self).values('limit').get( account_level__account = account_id, name = code)['limit']


class AccountLevelManager(models.Manager):
    def get_by_code(self, code):
        return super(AccountLevelManager, self).get(code = code)



class PreferenceManager(models.Manager):

    def get_value_by_account_id_and_key(self, account_id, key):
        return super(PreferenceManager, self).values('value').get( account = account_id, key = key )['value']

    def get_account_id_by_known_key_and_value(self, known_key, known_value):
        return super(PreferenceManager, self).values('account_id').get(value = known_value, key = known_key)['account_id']


class DataStreamManager(models.Manager):
    def get_top(self, account_id, limit = 5):
        """ Return the Top DSs Ids. """

        sql = """   SELECT `ao_datastreams`.`id`
                       , COUNT(`ao_datastreams`.`id`) AS `total`
                    FROM `ao_users`
                    INNER JOIN `ao_datastreams` ON (`ao_datastreams`.`user_id` = `ao_users`.`id`)
                    INNER JOIN `ao_datastream_hits` ON (`ao_datastreams`.`id` = `ao_datastream_hits`.`datastream_id`)
                    WHERE account_id = %s
                    GROUP BY `ao_datastreams`.`id`
                    ORDER BY `total` DESC
                    LIMIT %s"""
        params = [account_id, limit]

        cursor = connection.cursor()
        cursor.execute(sql, params)

        top_datastreams = []
        for datastream_id, total in cursor.fetchall():
            top_datastreams.append(datastream_id)

        return top_datastreams

    def get_last(self, account_id, limit = 5):
        """ Return the last DSs Ids. """

        sql = """   SELECT  MAX(`ao_datastream_revisions`.`id`) AS `datastream_revision_id`,
                        `ao_datastream_revisions`.`datastream_id`
                    FROM `ao_datastream_revisions`
                    INNER JOIN `ao_datastreams` ON (`ao_datastreams`.`id` = `ao_datastream_revisions`.`datastream_id`)
                    INNER JOIN `ao_users` ON (`ao_users`.`id` = `ao_datastreams`.`user_id`)
                    WHERE `ao_datastream_revisions`.`status` = %s AND `ao_users`.`account_id` = %s
                    GROUP BY `ao_datastream_revisions`.`datastream_id`
                    ORDER BY `ao_datastream_revisions`.`created_at` DESC
                    LIMIT %s"""

        params = [choices.StatusChoices.PUBLISHED, account_id, limit]

        cursor = connection.cursor()
        cursor.execute(sql, params)

        last_datastreams = []
        for datastream_revision_id, datastream_id in cursor.fetchall():
            last_datastreams.append(datastream_id)

        return last_datastreams


class CategoryManager(models.Manager):
    def get_for_home(self, language, account_ids = None, limit = None):
        cursor = connection.cursor()

        sql = """SELECT `ao_categories`.`id`,
                 `ao_categories_i18n`.`name`
          FROM `ao_categories_i18n`
          , `ao_categories` """

        sql += """ WHERE language = %s"""
        sql += """ AND `ao_categories_i18n`.`category_id` = `ao_categories`.`id`"""

        accounts_filter = account_ids
        if type(account_ids) != types.ListType:
            accounts_filter = [account_ids]

        sql += """ AND ("""
        op = """"""
        for account_id in accounts_filter:
            sql += op + """ `ao_categories`.`account_id` = %s"""
            op = """ OR """

        sql += """)"""

        sql += """ GROUP BY name
          ORDER BY name ASC"""

        if limit:
            sql += """ LIMIT %s""" % limit

        params = [language]

        for account_id in accounts_filter:
            params.append(account_id)

        cursor.execute(sql, params)
        row = cursor.fetchone()

        categories = []
        while row:
            categories += [{'id': row[0], 'name': row[1]}]
            row = cursor.fetchone()

        return categories

    def get_for_transparency(self, account):
        """ get categories for transparency microsite on selected account """
        categs = account.get_preference('account.transparency.categories').split()
        from core.models import Category
        categories_id = Category.objects.values("id", "categoryi18n__id", "categoryi18n__name").filter(id__in = categs)

        categories = []
        for category in categories_id:
            categories +=  [{ 'id': category["id"], 'name': category["categoryi18n__name"]}]

        return categories


class UserPassTicketsManager(models.Manager):
    pass


class VisualizationManager(models.Manager):
    def get_top(self, account_id, limit = 5):

        sql = """   SELECT `ao_visualizations`.`id`
                           , COUNT(`ao_visualizations`.`id`) AS `total`
                    FROM `ao_users`
                    INNER JOIN `ao_visualizations` ON (`ao_visualizations`.`user_id` = `ao_users`.`id`)
                    INNER JOIN `ao_visualization_hits` ON (`ao_visualizations`.`id` = `ao_visualization_hits`.`visualization_id`)
                    WHERE account_id = %s
                    GROUP BY `ao_visualizations`.`id`
                    ORDER BY `total` DESC
                    LIMIT %s"""
        params = [account_id, limit]

        cursor = connection.cursor()
        cursor.execute(sql, params)

        top_visualizations = []
        for visualization_id, total in cursor.fetchall():
            top_visualizations.append(visualization_id)

        return top_visualizations

    def get_last(self, account_id, limit = 5):
        """ Return the last VZs Ids. """

        sql = """   SELECT  MAX(`ao_visualizations_revisions`.`id`) AS `visualization_revision_id`,
                        `ao_visualizations_revisions`.`visualization_id`
                    FROM `ao_visualizations_revisions`
                    INNER JOIN `ao_visualizations` ON (`ao_visualizations`.`id` = `ao_visualizations_revisions`.`visualization_id`)
                    INNER JOIN `ao_users` ON (`ao_users`.`id` = `ao_visualizations`.`user_id`)
                    WHERE `ao_visualizations_revisions`.`status` = %s AND `ao_users`.`account_id` = %s
                    GROUP BY `ao_visualizations_revisions`.`visualization_id`
                    ORDER BY `ao_visualizations_revisions`.`created_at` DESC
                    LIMIT %s"""

        params = [choices.StatusChoices.PUBLISHED, account_id, limit]

        cursor = connection.cursor()
        cursor.execute(sql, params)

        last_visualizations = []
        for visualization_revision_id, visualization_id in cursor.fetchall():
            last_visualizations.append(visualization_id)

        return last_visualizations


class DataStreamParameterManager(models.Manager):

    def queryByDataStreamRevisionId(self, p_revision_id, p_language=settings.LANGUAGE_CODE[0:2]):
        parameter_id = 0
        parameter_position = 1
        parameter_name = 2
        parameter_description = 3

        l_parameter_cursor = connection.cursor()

        l_parameter_cursor.execute("""
                                    SELECT id
                                    , coalesce(position, 0)
                                    , name
                                    , description
                                    FROM ao_datastream_parameters
                                    WHERE datastream_revision_id = %s
                                    ORDER BY position
                                    """, [p_revision_id])

        l_parameters_rows = l_parameter_cursor.fetchall().__iter__()
        l_parameter_row = helpers.next(l_parameters_rows, None)

        l_parameters = []
        while l_parameter_row != None:

            l_parameter_id                      = l_parameter_row[parameter_id]
            l_parameter_name                    = l_parameter_row[parameter_name]
            l_parameter_description             = l_parameter_row[parameter_description]

            l_parameter = dict(parameter_id=l_parameter_id
                                , parameter_name=l_parameter_name
                                , parameter_description=l_parameter_description
                                , parameter_value=None)

            l_parameters.append(l_parameter)
            l_parameter_row = helpers.next(l_parameters_rows, None)

        return l_parameters


class DataSetManager(models.Manager):

    def getEndPointById(self, p_id):
        dataset_revision_id   = 0
        dataset_end_point     = 1

        l_dataset_cursor  = connection.cursor()

        l_dataset_cursor.execute("""SELECT id
                                    , end_point
                                    FROM ao_dataset_revisions
                                    WHERE dataset_id = %s
                                    ORDER BY id DESC
                                    """, [p_id])

        l_datasets_rows    = l_dataset_cursor.fetchall().__iter__()
        l_dataset_row      = helpers.next(l_datasets_rows, None)

        l_dataset_revision_id = l_dataset_row[dataset_revision_id]
        l_dataset_end_point   = l_dataset_row[dataset_end_point]

        return l_dataset_end_point, l_dataset_end_point.startswith('file://')


class DataStreamRevisionManager(models.Manager):
    def get_guids_with_cache(self):
        sql = """SELECT
              aodr.datastream_rev_id,
              adr.dataset_rev_id,
              aod.guid
            FROM
              ao_datastreams aod
            INNER JOIN (
            SELECT
              datastream_id, dataset_id, MAX(id) AS datastream_rev_id, status
            FROM
              ao_datastream_revisions
            WHERE
              status = %s GROUP BY datastream_id, status)
            AS aodr ON aod.id = aodr.datastream_id
            INNER JOIN (
            SELECT
              dataset_id, MAX(id) AS dataset_rev_id, status
            FROM
              ao_dataset_revisions
            WHERE
              status = %s AND
              impl_details LIKE '%%useCache="true"%%'
            GROUP BY
              dataset_id, status)
            AS adr ON aodr.dataset_id = adr.dataset_id"""

        params = [choices.StatusChoices.PUBLISHED, choices.StatusChoices.PUBLISHED]
        cursor = connection.cursor()
        cursor.execute(sql, params)

        last_guids = []
        for guid in cursor.fetchall():
            last_guids.append(guid)

        return last_guids


class ObjectGrantManager(models.Manager):

    def get_collaborators(self, object_id, object_type):

        sql = """SELECT `ao_users`.`nick`,
                        `ao_users`.`email`,
                        `ao_user_roles`.`code`
                 FROM `ao_user_object_grants`
                 INNER JOIN `ao_user_grants` ON (`ao_user_object_grants`.`grant_id` = `ao_user_grants`.`id`)
                 INNER JOIN `ao_users` ON (`ao_user_grants`.`user_id` = `ao_users`.`id`)
                 INNER JOIN `ao_user_roles` ON (`ao_user_grants`.`role_id` = `ao_user_roles`.`id`)
                 WHERE `ao_user_object_grants`.`type` = %s AND `ao_user_object_grants`.`"""+object_type+"""_id` = %s
                 ORDER BY `ao_user_object_grants`.`created_at` DESC"""

        params = [object_type, object_id]
        cursor = connection.cursor()
        cursor.execute(sql, params)

        collaborators = []
        for nick, email, role_code in cursor.fetchall():
            collaborators.append({'email': email, 'role': role_code, 'nick': nick})
        return collaborators

    def get_available_users(self, object_id, object_type, account_id):

        sql = """SELECT `ao_users`.`id`,
                        `ao_users`.`nick`,
                        `ao_users`.`email`
                 FROM `ao_users`
                 INNER JOIN `ao_user_role_roles` ON (`ao_users`.`id` = `ao_user_role_roles`.`user_id`)
                 INNER JOIN `ao_user_roles` ON (`ao_user_role_roles`.`role_id` = `ao_user_roles`.`id`)
                 WHERE `ao_users`.`account_id` = %s AND `ao_user_roles`.`code` IN ('ao-member')
                 AND `ao_users`.`id` NOT IN (
                    SELECT `ao_user_grants`.`user_id`
                    FROM `ao_user_grants`
                    INNER JOIN `ao_user_object_grants` ON (`ao_user_object_grants`.`grant_id` = `ao_user_grants`.`id`)
                    WHERE `ao_user_object_grants`.`type` = %s AND `ao_user_object_grants`.`"""+object_type+"""_id` = %s
                )"""

        params = [account_id, object_type, object_id]
        cursor = connection.cursor()
        cursor.execute(sql, params)

        available_users = []
        for user_id, nick, email in cursor.fetchall():
            available_users.append({'user_id': user_id, 'email': email, 'nick': nick})

        return available_users

    def has_privilege_on_object(self, object_id, object_type, user_id, privilege_code):

        sql = """SELECT 1
                 FROM `ao_user_object_grants`
                 INNER JOIN `ao_user_grants` ug0 ON (`ao_user_object_grants`.`grant_id` = ug0.`id`)
                 INNER JOIN `ao_user_roles` ON (ug0.`role_id` = `ao_user_roles`.`id`)
                 INNER JOIN `ao_user_grants` ug1 ON (`ao_user_roles`.`id` = ug1.`role_id`)
                 INNER JOIN `ao_user_privileges` ON (ug1.`privilege_id` = `ao_user_privileges`.`id`)
                 WHERE `ao_user_object_grants`.`type` = %s AND `ao_user_object_grants`.`"""+object_type+"""_id` = %s
                 AND ug0.`user_id` = %s AND `ao_user_privileges`.`code` = %s"""

        params = [object_type, object_id, user_id, privilege_code]
        cursor = connection.cursor()
        cursor.execute(sql, params)
        return bool(cursor.fetchall())
