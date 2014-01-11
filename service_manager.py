from comm import *
from conf import *
from module.module import *
from module.module_factory import *
from globals import *

class ServiceManager():

    def install_service(self):
        '''安装所有的服务'''
        for mod in self.get_module_list():
            if not mod.is_install():
                mod.install_service()
                logger.info(Lang().get('not_install_service') % (mod.module_name))

    def uninstall_service(self):
        '''卸载所有的服务'''
        for mod in self.get_module_list():
            if mod.is_install():
                logger.info(mod.uninstall_service())

    def start_service(self, service_list=None):
        '''启动服务'''
        for mod in self.get_module_list(service_list):
            logger.info(mod.start_service())

    def stop_service(self, service_list=None):
        '''停止服务'''
        for mod in self.get_module_list(service_list):
            logger.info(mod.stop_service())

    def get_module_list(self, service_list=None):
        list = []
        if service_list is None:
            service_list = Conf().get('module')
        for module_name in service_list:
            list.append(ModuleFactory.factory(module_name))
        return list
