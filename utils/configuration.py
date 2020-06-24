import yaml


class Borg:
    _shared_state = {}

    def __init__(self) -> None:
        self.__dict__ = self._shared_state


class Configurations(Borg):
    _first_initialization = True

    def __init__(self) -> None:
        Borg.__init__(self)
        if Configurations._first_initialization:
            self._load_file()
            Configurations._first_initialization = False

    def _load_file(self) -> None:
        with open("settings.yaml") as yaml_file:
            config = yaml.safe_load(yaml_file)

        self.__dict__.update(config)
