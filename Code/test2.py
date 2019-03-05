global addon
addon = "test"
import importlib
mod = importlib.import_module('Addons.{0}'.format(addon))

