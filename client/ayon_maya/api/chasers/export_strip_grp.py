import logging

import mayaUsd.lib as mayaUsdLib
from pxr import Sdf


def log_errors(fn):
    """Decorator to log errors on error"""

    def wrap(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            logging.error(exc, exc_info=True)
            raise

    return wrap


class StripGrpExportChaser(mayaUsdLib.ExportChaser):
    """Rename exported prims that end with ``_GRP`` by removing that suffix."""

    name = "AYON_stripGrp"
    suffix = "_GRP"

    def __init__(self, factoryContext, *args, **kwargs):
        super().__init__(factoryContext, *args, **kwargs)
        self.log = logging.getLogger(self.__class__.__name__)
        self.stage = factoryContext.GetStage()

    @log_errors
    def PostExport(self):
        layer = self.stage.GetRootLayer()
        paths = []

        def collect(path):
            if not path.IsPrimPath():
                return
            spec = layer.GetPrimAtPath(path)
            if spec and spec.name.endswith(self.suffix):
                paths.append(path)

        layer.Traverse("/", collect)

        edit = Sdf.BatchNamespaceEdit()
        for path in reversed(paths):
            new_name = path.name[: -len(self.suffix)]
            if not new_name:
                continue
            self.log.debug("Renaming prim %s to %s", path, new_name)
            edit.Add(path, path.ReplaceName(new_name))

        layer.Apply(edit)
        return True
