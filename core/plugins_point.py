from djangoplugins.point import PluginPoint


class DatalPluginPoint(PluginPoint):
    """
    Documentation, that describes how plugins can implement this plugin
    point.

    """
    pass


    @classmethod
    def get_active_with_att(cls, att):
        return map(lambda x: getattr(x, att), filter(lambda x: x.is_active() and hasattr(x, att), cls.get_plugins()))

