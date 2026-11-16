import pyblish.api

from ayon_maya.api import plugin

_USD_MODEL_CREATOR_IDENTIFIER = "io.ayon.creators.maya.mayausd.model"


class CollectMayaUsdStripGrp(plugin.MayaInstancePlugin):
    """Enable the export chaser that strips ``_GRP`` from USD prim names."""

    order = pyblish.api.CollectorOrder
    label = "Maya USD Export Chaser: Strip GRP"
    families = ["mayaUsd"]

    def process(self, instance):
        if (
            instance.data.get("creator_identifier")
            != _USD_MODEL_CREATOR_IDENTIFIER
        ):
            return

        self.log.debug("Enabling USD strip GRP chaser")
        instance.data.setdefault("chaser", []).append("AYON_stripGrp")
