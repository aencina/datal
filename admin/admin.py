from django.contrib import admin
from django.forms import Textarea
from core.models import *


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
    list_display = ('account', 'key', 'value')
    list_filter = ('account',)
    list_per_page = 25
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={"rows": 80, "cols": 220}), },
    }

admin.site.register(Preference, PreferenceAdmin)


class DataStreamAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'guid')
    list_filter = ('user',)
    list_per_page = 25

admin.site.register(DataStream, DataStreamAdmin)


class DataStreamRevisionAdmin(admin.ModelAdmin):
    list_display = ('id','datastream', 'user', 'category', 'status','created_at')
    list_filter = ('datastream', 'user')
    list_per_page = 25

admin.site.register(DataStreamRevision, DataStreamRevisionAdmin)


class DatastreamI18nAdmin(admin.ModelAdmin):
    list_display = ('id','datastream_revision', 'title')
    search_fields = ('title',)
    list_per_page = 25

admin.site.register(DatastreamI18n, DatastreamI18nAdmin)


class VisualizationI18nAdmin(admin.ModelAdmin):
    list_display = ('visualization_revision', 'title')
    search_fields = ('title',)
    list_per_page = 25

admin.site.register(VisualizationI18n, VisualizationI18nAdmin)


class DataStreamParameterAdmin(admin.ModelAdmin):
    list_display = ('datastream_revision', 'name')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(DataStreamParameter, DataStreamParameterAdmin)


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'is_dead','guid','created_at')
    search_fields = ('user', 'type')
    list_per_page = 25

admin.site.register(Dataset, DatasetAdmin)


class DatasetRevisionAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'user', 'category', 'status')
    search_fields = ('user', 'dataset', 'category')
    list_per_page = 25

admin.site.register(DatasetRevision, DatasetRevisionAdmin)


class DatasetI18nAdmin(admin.ModelAdmin):
    list_display = ('dataset_revision', 'title')
    search_fields = ('dataset_revision', 'title')
    list_per_page = 25

admin.site.register(DatasetI18n, DatasetI18nAdmin)


class VisualizationAdmin(admin.ModelAdmin):
    list_display = ('datastream', 'user')
    search_fields = ('datastream', 'user')
    list_per_page = 25

admin.site.register(Visualization, VisualizationAdmin)


class VisualizationRevisionAdmin(admin.ModelAdmin):
    list_display = ('visualization', 'user', 'status')
    search_fields = ('visualization', 'user')
    list_per_page = 25

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
        list_display = ('id','guid', 'last_revision', 'last_published_revision')
        search_fields = ('guid',)
        list_per_page = 25

    admin.site.register(Dashboard, DashboardAdmin)


    # DashboardI18n
    class DashboardI18nAdmin(admin.ModelAdmin):
        list_display = ('id','dashboard_revision', 'language', 'title', 'created_at')
        search_fields = ('dashboard_revision',)
        list_filter = ('language',)
        list_per_page = 25


    admin.site.register(DashboardI18n, DashboardI18nAdmin)


    # DashboardRevision
    class DashboardRevisionAdmin(admin.ModelAdmin):
        list_display = ('id','dashboard', 'user', 'category', 'status', 'created_at')
        search_fields = ('dashboard',)
        list_filter = ('user','status','dashboard',)
        list_per_page = 25
    admin.site.register(DashboardRevision, DashboardRevisionAdmin)


    # DashboardWidget
    class DashboardWidgetAdmin(admin.ModelAdmin):
        list_display = ('id','order', 'dashboard_revision', 'datastream', 'visualization')
        search_fields = ('dashboard_revision',)
        list_filter = ('dashboard_revision',)
        list_per_page = 25
    admin.site.register(DashboardWidget, DashboardWidgetAdmin)
except:
    pass
