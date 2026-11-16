import pyblish.api

from ayon_core.lib import UILabelDef
from ayon_core.pipeline.publish import AYONPyblishPluginMixin
from ayon_maya.api import plugin


class ValidateOptionalHeader(plugin.MayaInstancePlugin, AYONPyblishPluginMixin):
    """Section title shown when the instance has optional validators."""

    label = "Optional Validators"
    order = pyblish.api.ValidatorOrder - 0.01
    families = ["*"]

    def process(self, instance):
        pass

    @classmethod
    def get_attr_defs_for_instance(cls, create_context, instance):
        for plugin_cls in create_context.plugins_with_defs:
            if plugin_cls is cls or not getattr(plugin_cls, "enabled", True):
                continue
            if not getattr(plugin_cls, "optional", False):
                continue
            if plugin_cls.order >= pyblish.api.ExtractorOrder:
                continue
            if not plugin_cls.instance_matches_plugin_families(instance):
                continue
            return [UILabelDef("<b>Optional Validators</b>")]
        return []
