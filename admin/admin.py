from django.contrib import admin
from django.forms import Textarea
from django.core import urlresolvers
from core.models import *
from django.contrib.contenttypes.models import ContentType
import logging
logger = logging.getLogger(__name__)

class ContentTypeAdmin(admin.ModelAdmin):
    list_display= ("app_label", "model", "name")
admin.site.register(ContentType, ContentTypeAdmin)

class UserAdmin(admin.ModelAdmin):
    fields = ('name', 'nick', 'email', 'password', 'country', 'ocupation', 'language', 'roles', 'account')
    list_display = ('id', 'name', 'nick', 'account', 'language', 'created_at')
    list_filter = ('account','language')
    search_fields = ('name', 'nick')
    list_per_page = 25

admin.site.register(User, UserAdmin)


class ThresholdAdmin(admin.ModelAdmin):
    fields = ('name', 'account_level', 'account', 'description', 'limit')
    list_display = ('name', 'limit', 'account_level', 'account')
    search_fields = ('name', 'account_level')
    list_per_page = 25

admin.site.register(Threshold, ThresholdAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name', )
    list_per_page = 25

admin.site.register(Tag, TagAdmin)


class GrantAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'privilege')
    search_fields = ('privilege',)
    list_filter = ('user', 'role')
    list_per_page = 25

admin.site.register(Grant, GrantAdmin)


class SettingAdmin(admin.ModelAdmin):
    fields = ('key', 'description', 'value')
    list_display = ('key', 'description', 'value')
    search_fields = ('key','description', 'value')
    list_per_page = 100

admin.site.register(Setting, SettingAdmin)


class RoleAdmin(admin.ModelAdmin):
    fields = ('name', 'code', 'description')
    list_display = ('name', 'code', 'description', 'created_at')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(Role, RoleAdmin)


class PrivilegeAdmin(admin.ModelAdmin):
    fields = ('name', 'code', 'description')
    list_display = ('name', 'code', 'description', 'created_at')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(Privilege, PrivilegeAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'auth_key', 'created_at', 'expires_at', 'valid', 'type')
    search_fields = ('name','user', 'type')
    list_per_page = 25

admin.site.register(Application, ApplicationAdmin)


class AccountLevelAdmin(admin.ModelAdmin):
    fields = ('name', 'code', 'description')
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(AccountLevel, AccountLevelAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'status')
    search_fields = ('name', 'level', 'status')
    list_per_page = 25

admin.site.register(Account, AccountAdmin)


class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('key',"goto_account",  'value')
    list_filter = ('account',)
    list_per_page = 25
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={"rows": 80, "cols": 220}), },
    }

    def goto_account(self, obj):
        ct = ContentType.objects.get_for_model(obj.account.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[obj.account.id])
        return u"<a href='%s'>%s</a>" % (link, obj.account)
    goto_account.allow_tags=True
    goto_account.short_description='Account'

admin.site.register(Preference, PreferenceAdmin)


class DataStreamAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'guid', "goto_last_revision", "goto_last_published_revision")
    list_filter = ('user',)
    list_per_page = 25
    fields = ['guid', 'user', "goto_last_revision", "goto_last_published_revision"]
    readonly_fields= ('user', "goto_last_revision", "goto_last_published_revision" )

    def goto_last_revision(self, obj):
        model = obj.last_revision

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_last_revision.allow_tags=True
    goto_last_revision.short_description='Last Rev'

    def goto_last_published_revision(self, obj):
        model = obj.last_published_revision

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_last_published_revision.allow_tags=True
    goto_last_published_revision.short_description='Last Published Rev'


admin.site.register(DataStream, DataStreamAdmin)


class DataStreamRevisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'goto_dataset','goto_datastream', 'user', 'category', 'status','created_at')
    list_filter = ('datastream', 'user')
    list_per_page = 25
    fields =['goto_dataset','goto_datastream','category','user','data_source','select_statement','status','meta_text','rdf_template']
    readonly_fields= ('user', 'goto_dataset', 'goto_datastream','status')

    def goto_dataset(self, obj):
        model = obj.dataset

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_dataset.allow_tags=True
    goto_dataset.short_description='Dataset'

    def goto_datastream(self, obj):
        model = obj.datastream

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_datastream.allow_tags=True
    goto_datastream.short_description='Datastream'



admin.site.register(DataStreamRevision, DataStreamRevisionAdmin)


class DatastreamI18nAdmin(admin.ModelAdmin):
    list_display = ('id','goto_datastream_revision', 'title')
    search_fields = ('title',)
    list_per_page = 25

    def goto_datastream_revision(self, obj):
        model = obj.datastream_revision

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_datastream_revision.allow_tags=True
    goto_datastream_revision.short_description='Datastream Rev'



admin.site.register(DatastreamI18n, DatastreamI18nAdmin)


class VisualizationI18nAdmin(admin.ModelAdmin):
    list_display = ('id', 'goto_visualization_revision', 'title')
    search_fields = ('title',)
    list_per_page = 25

    def goto_visualization_revision(self, obj):
        model = obj.visualization_revision

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_visualization_revision.allow_tags=True
    goto_visualization_revision.short_description='Visualization Rev'

admin.site.register(VisualizationI18n, VisualizationI18nAdmin)


class DataStreamParameterAdmin(admin.ModelAdmin):
    list_display = ('datastream_revision', 'name')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(DataStreamParameter, DataStreamParameterAdmin)


class VisualizationParameterAdmin(admin.ModelAdmin):
    list_display = ('revision', 'name')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(VisualizationParameter, VisualizationParameterAdmin)


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'is_dead','guid','created_at', 'goto_last_revision', 'goto_last_published_revision')
    search_fields = ('user', 'type')
    list_per_page = 25
    fields = ["type", "is_dead", "guid", 'user', 'goto_last_revision', 'goto_last_published_revision']
    readonly_fields= ('user', 'goto_last_revision', 'goto_last_published_revision')

    def goto_last_revision(self, obj):
        model = obj.last_revision

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_last_revision.allow_tags=True
    goto_last_revision.short_description='Last Rev'

    def goto_last_published_revision(self, obj):
        model = obj.last_published_revision

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_last_published_revision.allow_tags=True
    goto_last_published_revision.short_description='Last Published Rev'


admin.site.register(Dataset, DatasetAdmin)


class DatasetRevisionAdmin(admin.ModelAdmin):
    list_display = ('id','goto_dataset', 'user', 'category', 'status')
    search_fields = ('user', 'dataset', 'category')
    list_per_page = 25
    fields = ["goto_dataset", "user", "category", 'end_point', 'filename','impl_details', 'impl_type', 'status', 'size']
    readonly_fields= ('user', 'goto_dataset','end_point', 'filename', 'status','size')

    def goto_dataset(self, obj):
        model = obj.dataset

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_dataset.allow_tags=True
    goto_dataset.short_description='Dataset'



admin.site.register(DatasetRevision, DatasetRevisionAdmin)


class DatasetI18nAdmin(admin.ModelAdmin):
    list_display = ('dataset_revision', 'title')
    search_fields = ('dataset_revision', 'title')
    list_per_page = 25

admin.site.register(DatasetI18n, DatasetI18nAdmin)


class VisualizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'guid', 'goto_datastream', 'user', 'goto_last_revision', 'goto_last_published_revision')
    search_fields = ('datastream', 'user')
    list_per_page = 25
    fields = ['goto_datastream', 'user', 'datastream', 'goto_last_revision', 'goto_last_published_revision']
    readonly_fields= ('goto_datastream', 'user', 'datastream', 'goto_last_revision', 'goto_last_published_revision')

    def goto_last_revision(self, obj):
        model = obj.last_revision

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_last_revision.allow_tags=True
    goto_last_revision.short_description='Last Rev'

    def goto_last_published_revision(self, obj):
        model = obj.last_published_revision

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_last_published_revision.allow_tags=True
    goto_last_published_revision.short_description='Last Published Rev'

    def goto_datastream(self, obj):
        model = obj.datastream

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_datastream.allow_tags=True
    goto_datastream.short_description='Datastream'



admin.site.register(Visualization, VisualizationAdmin)


class VisualizationRevisionAdmin(admin.ModelAdmin):
    list_display = ('goto_visualization', 'user', 'status', 'goto_datastream')
    search_fields = ('visualization', 'user')
    list_per_page = 25
    #fields = ['user','lib','impl_details','meta_text','status','parameters',]
    fields = ['goto_visualization','user','goto_datastream','lib','impl_details','meta_text','status','parameters',]
    readonly_fields= ('goto_visualization','user','goto_datastream','status')

    def goto_visualization(self, obj):
        model = obj.visualization

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_visualization.allow_tags=True
    goto_visualization.short_description='Visualization'

    def goto_datastream(self, obj):
        model = obj.datastream

        if not model:
            return ""
        ct = ContentType.objects.get_for_model(model.__class__)
        link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
        return u"<a href='%s'>%s</a>" % (link, model)
    goto_datastream.allow_tags=True
    goto_datastream.short_description='Datastream'
admin.site.register(VisualizationRevision, VisualizationRevisionAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 25

admin.site.register(Category, CategoryAdmin)


class CategoryI18nAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    search_fields = ('category', 'name')
    list_per_page = 25

admin.site.register(CategoryI18n, CategoryI18nAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'url')
    list_per_page = 25

admin.site.register(Source, SourceAdmin)

class DataStreamHitsAdmin(admin.ModelAdmin):
    list_display = ('datastream', 'created_at', 'channel_type')
    search_fields = ('datastream', 'created_at')
    list_per_page = 25

admin.site.register(DataStreamHits, DataStreamHitsAdmin)

class VisualizationHitsAdmin(admin.ModelAdmin):
    list_display = ('visualization', 'created_at', 'channel_type')
    search_fields = ('visualization', 'created_at')
    list_per_page = 25

admin.site.register(VisualizationHits, VisualizationHitsAdmin)


class DataStreamCommentAdmin(admin.ModelAdmin):
    list_display = ('datastream', 'user')
    search_fields = ('datastream', 'user')
    list_per_page = 25

admin.site.register(DataStreamComment, DataStreamCommentAdmin)

try:
    # Esto no deberia estar aca, hay que pasarlo a los plugins
    from plugins.dashboards.models import Dashboard, DashboardI18n, DashboardRevision, DashboardWidget

    # Dashboard
    class DashboardAdmin(admin.ModelAdmin):
        list_display = ('id','user','guid', 'goto_last_revision', 'goto_last_published_revision')
        search_fields = ('guid',)
        list_per_page = 25
        readonly_fields= ('goto_last_revision', 'goto_last_published_revision')

        def goto_last_revision(self, obj):
            model = obj.last_revision
    
            if not model:
                return ""
            ct = ContentType.objects.get_for_model(model.__class__)
            link=urlresolvers.reverse("%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
            return u"<a href='%s'>%s</a>" % (link, model)
        goto_last_revision.allow_tags=True
        goto_last_revision.short_description='Last Rev'
    
        def goto_last_published_revision(self, obj):
            model = obj.last_published_revision
    
            if not model:
                return ""
            #ct = ContentType.objects.get_for_model(model.__class__)
            #link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
            #return u"<a href='%s'>%s</a>" % (link, model)
        goto_last_published_revision.allow_tags=True
        goto_last_published_revision.short_description='Last Published Rev'


    admin.site.register(Dashboard, DashboardAdmin)


    # DashboardI18n
    class DashboardI18nAdmin(admin.ModelAdmin):
        list_display = ('id','goto_dashboard_revision', 'language', 'title', 'created_at')
        search_fields = ('dashboard_revision',)
        list_filter = ('language',)
        list_per_page = 25
        readonly_fields= ('goto_dashboard_revision',)
 
        def goto_dashboard_revision(self, obj):
            model = obj.dashboard_revision
    
            if not model:
                return ""
            ct = ContentType.objects.get_for_model(model.__class__)
            link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
            return u"<a href='%s'>%s</a>" % (link, model)
        goto_dashboard_revision.allow_tags=True
        goto_dashboard_revision.short_description='Dashboard Rev'



    admin.site.register(DashboardI18n, DashboardI18nAdmin)

    
    # DashboardRevision
    class DashboardRevisionAdmin(admin.ModelAdmin):
        list_display = ('id','goto_dashboard', 'user', 'category', 'status', 'created_at')
        search_fields = ('dashboard',)
        list_filter = ('user','status','dashboard',)
        list_per_page = 25
        readonly_fields= ("goto_dashboard",)        
 
        def goto_dashboard(self, obj):
            model = obj.dashboard
    
            if not model:
                return ""
            ct = ContentType.objects.get_for_model(model.__class__)
            link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
            return u"<a href='%s'>%s</a>" % (link, model)
        goto_dashboard.allow_tags=True
        goto_dashboard.short_description='Dashboard'


    admin.site.register(DashboardRevision, DashboardRevisionAdmin)


    # DashboardWidget
    class DashboardWidgetAdmin(admin.ModelAdmin):
        list_display = ('id','order', 'goto_dashboard_revision', 'goto_datastream', 'goto_visualization')
        search_fields = ('dashboard_revision',)
        list_filter = ('dashboard_revision',)
        list_per_page = 25
        readonly_fields= ('goto_dashboard_revision', 'goto_datastream', 'goto_visualization')
 
        def goto_dashboard_revision(self, obj):
            model = obj.dashboard_revision
    
            if not model:
                return ""
            ct = ContentType.objects.get_for_model(model.__class__)
            link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
            return u"<a href='%s'>%s</a>" % (link, model)
        goto_dashboard_revision.allow_tags=True
        goto_dashboard_revision.short_description='Dashboard Rev'

        def goto_datastream(self, obj):
            model = obj.datastream
    
            if not model:
                return ""
            ct = ContentType.objects.get_for_model(model.__class__)
            link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
            return u"<a href='%s'>%s</a>" % (link, model)
        goto_datastream.allow_tags=True
        goto_datastream.short_description='Datastream'

        def goto_visualization(self, obj):
            model = obj.visualization
    
            if not model:
                return ""
            ct = ContentType.objects.get_for_model(model.__class__)
            link=urlresolvers.reverse("admin:%s_%s_change" %(ct.app_label, ct.model), args=[model.id])
            return u"<a href='%s'>%s</a>" % (link, model)
        goto_visualization.allow_tags=True
        goto_visualization.short_description='Visualization'
    admin.site.register(DashboardWidget, DashboardWidgetAdmin)
except Exception as e:
    import sys, traceback
    logger.error("\n".join(traceback.format_exception(*sys.exc_info())))
