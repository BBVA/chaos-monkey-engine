'''
ModulesStore
Handle the dynamic load of modules outside the main package.

'''
import logging
import sys
import inspect
from os import listdir
from os.path import isfile, join, splitext, isdir


class ModulesStore:
    """
    Load and store modules from outside the app package
    """
    modules = []

    def __init__(self, klass):
        self.klass = klass
        self.modules = []
        self.log = logging.getLogger('%s.%s' % (__name__, klass.__name__))

    def load(self, path):
        """
        Loads all modules found in a given path.
        It adds the path to the sys.path and import all modules found

        :param path: path for lookup modules
        """

        self._validate_path(path)

        sys.path.insert(0, path)

        module_names = self._get_module_names(path)
        try:
            for name in module_names:
                self.log.debug('added module %s', name)
                module = __import__(name)
                self.modules.append(module)
        except ImportError:
            self.log.debug('error importing module %s', name)
            raise ValueError('Unable to import %s' % name)

    def set_modules(self, modules):
        self.modules = modules

    def get_modules(self):
        return self.modules

    def list(self):
        """
        List all loaded modules names. It will return a list withe the
        __name__ of each module
        :return:
        """
        module_names = []
        for module in self.get_modules():
            module_name = getattr(module, '__name__')
            for name, data in inspect.getmembers(module):
                if inspect.isclass(data) and self._has_klass_ancestor(data):
                    module_names.append(module_name + ':' + name)

        return module_names

    def add(self, module):
        self.modules.append(module)

    def remove(self, module_name):
        for module in self.modules:
            if module_name == getattr(module, '__name__'):
                self.modules.remove(module)

    def get(self, ref):
        """
        Given a str reference of a class in a module (eg. ModuleName.ClassName)
        return the class so it can be instantiated

        The module with the class must be loaded first using load or add method.

        :param ref: str representation of a class in a module
        :return: class ready for instantation
        """
        return self._ref_to_obj(ref)

    def _has_klass_ancestor(self, cls):
        if hasattr(cls, '__bases__') and self.klass in cls.__bases__:
            return True
        return False

    @staticmethod
    def _validate_path(path):
        '''
        Check for a valid path
        '''
        if not isdir(path):
            raise ValueError('invalid path ' + path)

    @staticmethod
    def _get_module_names(path):
        '''Inspect a path and return all file names without extension'''
        names = []
        for f in listdir(path):
            if isfile(join(path, f)):
                names.append(splitext(f)[0])
        return names

    def _ref_to_obj(self, ref):
        """
        Return the object pointed to by ``ref``.
        :type ref: str
        """
        if not isinstance(ref, str):
            raise TypeError('References must be strings')
        if ':' not in ref:
            raise ValueError('Invalid reference')

        module_name, class_name = ref.split(':', 1)
        for module in self.modules:
            attr_name = getattr(module, '__name__')
            if attr_name == module_name:
                try:
                    self.log.debug(attr_name + ' found on module store!')
                    return getattr(module, class_name)
                except Exception:
                    raise ModuleLookupError('Error resolving reference %s: not found in modules' % ref)


class ModuleLookupError(Exception):
    """
    Represent a Module lookup error when a module is not found by its ref
    """

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

    def __str__(self):
        return '%s' % self.message
