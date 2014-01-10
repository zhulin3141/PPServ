import module
from module.module_factory import *

for mod in ModuleFactory.get_module_list():
    if not mod.is_install():
        print mod.uninstall_service()
