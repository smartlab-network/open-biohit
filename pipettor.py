from typing import Dict, Tuple, Type, Callable

import System
from System.Data import DataTable
from InstrumentLib import InstrumentCls, ControlCls

CLR_TYPES: Dict[str, Tuple[Type, Type]] = {
    "System.String": (String, str),
    "Single": (Single, float),
    "Boolean": (Boolean, bool),
    "System.Object": (Object, object),
    "Int32": (Int32, int),
    "System.Data.DataTable": (DataTable, DataTable)
}


class Pipettor:
    __instrument: InstrumentCls

    def __init__(self) -> None:
        self.__instrument = InstrumentCls()

        for name in dir(self.__instrument):
            attr = getattr(self.__instrument, name)
            if attr.__class__.__name__ == "MethodBinding":
                print(name)
                if name.startswith(("add_", "remove_")):  # event handlers
                    print("Skipping", name)
                    continue
                try:
                    setattr(self, name, ClrMethod(attr))
                except NotImplementedError as ex:
                    print(ex)

    def __del__(self):
        self.__instrument.Dispose()


class ClrMethod:
    overloads: Dict[Tuple[Type, ...], Callable[[...], bool]]
    __wrapped_func: Callable

    def __init__(self, wrapped_func: Callable) -> None:
        self.__wrapped_func = wrapped_func
        self.overloads = {}
        raw_overloads = str(self.__wrapped_func.Overloads).splitlines(keepends=False)
        for line in raw_overloads:
            ret_type, rest = line.split(maxsplit=1)
            raw_param_types = rest[:-1].split("(")[1]
            if "ByRef" in raw_param_types:
                raise NotImplementedError("ref types not implemented")
            param_types = []
            for raw_param_type in raw_param_types.split(", "):
                if raw_param_type != "":  # not empty
                    param_types.append(CLR_TYPES[raw_param_type][1])
            if param_types:
                self.overloads[tuple(param_types)] = eval(f"self._ClrMethod__wrapped_func.Overloads[{raw_param_types}]")
            else:
                self.overloads[()] = self.__wrapped_func

    def __call__(self, *args, **kwargs):
        n_args = len(args) + len(kwargs)
        possible_overloads = {}
        for signature, method in self.overloads.items():
            if len(signature) == n_args:
                return possible_overloads.popitem()[1](*args, **kwargs)
        raise NotImplementedError("Method with this signature does not exist or multiple signatures exist")