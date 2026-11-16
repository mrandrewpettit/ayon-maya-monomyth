import pyblish.api

from ayon_core.lib import UILabelDef
from ayon_maya.api import plugin

class ValidateOptionalHeader(plugin.MayaInstancePlugin):
    label = "Optinoal Validators"
    order = pyblish.api.ValidatorOrder - 0.01
    families = ["model"]

    def process(self, instance):
        pass

    @classmethod
    def get_attr_defs_for_instance(cls, create_context, instance):
        return [UILabelDef("Optional Validators")]