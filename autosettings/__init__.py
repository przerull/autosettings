import typing

DEFAULT_MRO = (
    "dunder_main_directory",
    "user_config_directory",
    "system_config_directory",
)

class PathFinder:
    def __init__(self,
                 config_directory_name: str = "python_autosettings",
                 default_folder_method: str = "user_config_directory",
                 method_resolution_order: typing.Tuple[str] = DEFAULT_MRO):
        self._validate_default_folder_method(default_folder_method)
        self._validate_mro(method_resolution_order)
        self.method_resolution_order = method_resolution_order
        self.default_folder_method = default_folder_method
        self.config_directory_name = config_directory_name

    def _validate_default_folder_method(self, default_folder_method: str):
        if not hasattr(self, default_folder_method):
            raise AttributeError() #TODO get decent error message
        elif not callable(getattr(self, default_folder_method)):
            raise TypeError() #TODO get decent error message

    def _validate_mro(self, mro: typing.Tuple[str]):
        for method in mro:
            if not hasattr(self, method):
                raise AttributeError() #TODO get decent error message
            elif not callable(getattr(self, method)):
                raise TypeError() #TODO get decent error message

    def absolute_config_filepath(self, filename: str):
        """Returns the absolute path of the configuration file based on:
            - the filename parameter
            - self.config_directory_name
            - PathFinder.RESOLUTION_ORDER
            - PathFinder.DEFAULT_DIRECTORY
        """
        pass

    def user_config_directory() -> str:
        """Returns $HOME/.config on linux and %AppData%\Roaming on Windows."""
        pass

    def system_config_directory() -> str:
        """Returns /etc on linux and %AppData%\Roaming on Windows."""
        pass

    def dunder_main_directory() -> str:
        """Returns the absolute path of the directory containing the python
        script evoked directly by the interpreter (where __main__ is).
        """
        pass



class AutoSettings:
    def __init__(self,
                 filename: str,
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



