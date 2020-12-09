import typing
import sys
import os

DEFAULT_METHOD_RESOLUTION_ORDER = (
    "dunder_main_directory",
    "user_config_directory",
    "system_config_directory",
)

DEFAULT_FOLDER_METHOD = "user_config_directory"

OptionalStrTuple = typing.Optional[typing.Tuple[str]]

class PathFinder:
    def __init__(self,
                 config_directory_name: str = "python_autosettings",
                 default_folder_method: typing.Optional[str] = None,
                 method_resolution_order: OptionalStrTuple = None):
        if default_folder_method is None:
            default_folder_method = DEFAULT_FOLDER_METHOD
        if method_resolution_order is None:
            method_resolution_order = DEFAULT_METHOD_RESOLUTION_ORDER
        self._ensure_callable_attribute_exists(default_folder_method)
        self._validate_mro(method_resolution_order)
        # The following attributes are "private" to discourage users from
        # modifying them after the constructor is called. @property methods
        # are provided to grant read-only access
        self._method_resolution_order = method_resolution_order
        self._default_folder_method = default_folder_method
        self._config_directory_name = config_directory_name

    def _ensure_callable_attribute_exists(self, attribute_name: str):
        if not hasattr(self, attribute_name):
            raise self._get_attribute_error(attribute_name)
        elif not callable(getattr(self, attribute_name)):
            raise self._get_not_callable_error(attribute_name)

    def _get_attribute_error(self, attribute_name: str):
        template = "'{}' object has not attribute '{}'"
        classname = self.__class__.__name__
        message = template.format(classname, attribute_name)
        return AttributeError(message)

    def _get_not_callable_error(self, attribute_name: str):
        template = "'{}' is not a callable member of the '{}' class"
        classname = self.__class__.__name__
        message = template.format(attribute_name, classname)
        return TypeError(message)

    def _validate_mro(self, mro: typing.Tuple[str]):
        for method in mro:
            self._ensure_callable_attribute_exists(method)

    @property
    def default_folder_method(self):
        return self._default_folder_method

    @property
    def method_resolution_order(self):
        return self._method_resolution_order

    @property
    def config_directory_name(self):
        return self._config_directory_name

    def absolute_config_filepath(self, filename: str):
        """Returns the absolute path of the configuration file based on:
            - the filename parameter
            - self.config_directory_name
            - PathFinder.RESOLUTION_ORDER
            - PathFinder.DEFAULT_DIRECTORY
        """
        for method_name in self.method_resolution_order:
            filepath = self._get_full_filepath(method_name, filename)
            if os.path.isfile(filepath):
                return filepath
        return self._get_full_filepath(self.default_folder_method, filename)

    def _get_full_filepath(self, method_name: str, filename: str):
        method = getattr(self, method_name)
        return os.path.join(method(), filename)

    def user_config_directory(self) -> str:
        """Returns $HOME/.config on linux and %AppData%\Roaming on Windows."""
        user_dir = os.path.abspath(os.path.expanduser('~'))
        if sys.platform.startswith('linux'):
            return os.path.join(user_dir, '.config', self.config_directory_name)
        else: # pragma: no cover
            raise self._not_implemented_in_system("user_config_directory")

    def _not_implemented_in_system(self, method_name: str): # pragma: no cover
        template = "method '{}' not implimented for system: {}"
        return NotImplementedError(template.format(method_name, sys.platform))

    def system_config_directory(self) -> str:
        """Returns /etc on linux and %AppData%\Roaming on Windows."""
        if sys.platform.startswith('linux'):
            return os.path.join('/etc', self.config_directory_name)
        else: # pragma: no cover
            raise self._not_implemented_in_system("system_config_directory")

    def dunder_main_directory(self) -> str:
        """Returns the absolute path of the directory containing the python
        script evoked directly by the interpreter (where __main__ is).
        """
        return os.path.abspath(os.path.dirname(sys.argv[0]))



class AutoSettings:
    def __init__(self,
                 filename: str,
                 config_directory_name: typing.Optional[str] = None,
                 pathfinder: typing.Optional[PathFinder] = None,
                 autosave: bool = True):
        self.filename = filename
        self.pathfinder = pathfinder
        pass

    def __getitem__(self):
        pass

    def get(self, key: str, default: str):
        pass

    def __setitem__(self):
        pass



