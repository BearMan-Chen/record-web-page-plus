from enum import Enum, unique, auto


@unique
class MyEnumPY(Enum):
    @property
    def name_(self):
        return self._replace_name.lower()

    @property
    def __route_name(self) -> str:
        return self._replace_name.lower().replace("_", "-")

    def route_args(self, *args: str) -> str:
        return f"""/{self.__route_name}/<{">/<".join(_.name_ if type(_) is EnumRouteAttribute else _ for _ in args)}>""" if len(args) else self.route

    @property
    def route(self) -> str:
        return self._value_.lower().replace("_", "-") if isinstance(self._value_, str) else f"/{self.__route_name}"

    @property
    def _replace_name(self) -> str:
        return self._name_.split("__")[0]

    def __str__(self) -> str:
        return self.name_


@unique
class MyEnumJS(MyEnumPY):
    @property
    def name_(self):
        return "".join(_.capitalize() if idx else _.lower() for idx, _ in enumerate(self._replace_name.split("_")))


@unique
class EnumRouteAttribute(MyEnumPY):
    FILE_NAME = auto()
    DATE_TIME = auto()
    FOLDER_PATH = auto()
