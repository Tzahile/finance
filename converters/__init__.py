import pkgutil
from os.path import dirname
from importlib import import_module


pwd = dirname(__file__)
for (_, name, _) in pkgutil.iter_modules([pwd]):
    if name.endswith("_converter"):
        import_module("." + name, package=__name__)
