from autobean_refactor.models.raw_models import plugin
from . import internal


class Plugin(plugin.Plugin):
    name = internal.required_string_property(plugin.Plugin.raw_name)
    config = internal.optional_escaped_string_property(plugin.Plugin.raw_config)
