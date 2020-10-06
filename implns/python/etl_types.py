from typing import Callable, List, Dict, Any

class EtlExpression(object):
    def __init__(self):
        assert False

    def native(self) -> Any:
        pass

    def __str__(self) -> str:
        return self.readable_str()

    def readable_str(self):
        pass

    def unreadable_str(self):
        return self.readable_str()

class EtlString(EtlExpression):
    def __init__(
        self, input_value: str, is_already_encoded: bool = False, keyword: bool = False
    ) -> None:
        # print("STR: " + input_value)
        if is_already_encoded:
            self._value = input_value
        if keyword:
            self._value = "\u029e" + input_value
        else:
            self._value = input_value

    def readable_str(self) -> str:
        if self.is_keyword():
            return ":" + self._value[1:]
        else:
            val = self._value

            val = val.replace("\\", "\\\\")  # escape backslashes
            val = val.replace("\n", "\\n")  # escape newlines
            val = val.replace('"', '\\"')  # escape quotes
            val = '"' + val + '"'  # add surrounding quotes
            return val

    def unreadable_str(self) -> str:
        if self.is_keyword():
            return ":" + self._value[1:]
        else:
            return self._value

    def native(self) -> Any:
        return self._value

    def is_keyword(self) -> bool:
        return len(self._value) > 1 and self._value[0] == "\u029e"


class EtlList(EtlExpression):
    def __init__(self, values: List[EtlExpression])  -> None :
        for x in values:
            assert isinstance(x,EtlExpression)
        self._values = values

    def readable_str(self) -> str:
        return "[" + " ".join(map(lambda x: x.readable_str(), self._values)) + "]"

    def unreadable_str(self) -> str:
        return "[" + " ".join(map(lambda x: x.unreadable_str(), self._values)) + "]"

    def native(self) -> List[EtlExpression]:
        return self._values


class EtlSymbol(EtlExpression):
    def __init__(self, value: str) -> None:
        assert type(value) is str

        self._value = str(value)

    def readable_str(self) -> str:
        return str(self._value)

    def eval(self, environment) -> EtlExpression:
        # print("Evaluating: " + repr(self))
        return environment.get(self)

    def native(self) -> str:
        return self._value


class EtlException(Exception, EtlExpression):
    def __init__(self, value: EtlExpression) -> None:
        self._value = value

    def readable_str(self) -> str:
        return str(self._value)

    def native(self) -> EtlExpression:
        return self._value


class EtlIndexError(EtlException):
    def __init__(self, index: int) -> None:
        super().__init__(EtlString("Index out of bounds: " + str(index)))


class EtlSyntaxException(EtlException):
    def __init__(self, message) -> None:
        super().__init__(EtlString(message))


class EtlUnknownTypeException(EtlException):
    def __init__(self, message) -> None:
        super().__init__(EtlString(message))


class EtlInvalidArgumentException(EtlException):
    def __init__(self, arg: EtlExpression, reason: str) -> None:
        super().__init__(
            EtlString(arg.readable_str() + ": invalid argument: " + reason)
        )


class EtlUnknownSymbolException(EtlException):
    def __init__(self, func: str) -> None:
        super().__init__(EtlString("'" + func + "' not found"))
        self.func = func


class EtlNotImplementedException(EtlException):
    def __init__(self, func: str) -> None:
        super().__init__(EtlString("not implemented: " + func))


class EtlFunctionCompiled(EtlExpression):
    def __init__(
        self, native_function: Callable[[List[EtlExpression]], EtlExpression]
    ) -> None:
        self._native_function = native_function
        self._is_macro = False

    def readable_str(self):
        return "#<macro>" if self._is_macro else "#<function>"

    def native(self) -> Callable[[List[EtlExpression]], EtlExpression]:
        return self._native_function

    def call(self, args: List[EtlExpression]) -> EtlExpression:
        # print("CALL: " + str([str(arg) for arg in args]))
        return self._native_function(args)

    def is_macro(self) -> bool:
        return self._is_macro

    def make_macro(self) -> None:
        self._is_macro = True


class EtlFunctionRaw(EtlExpression):
    def __init__(
        self,
        fn: Callable[[List[EtlExpression]], EtlExpression],
        ast: EtlExpression,
        params: EtlList,
        env,
    ) -> None:
        self._ast = ast
        self._params = params
        self._env = env
        self._native_function = fn
        self._is_macro = False

    def readable_str(self):
        return "#<macro>" if self._is_macro else "#<function>"

    def ast(self) -> EtlExpression:
        return self._ast

    def params(self) -> EtlList:
        return self._params

    def env(self):
        return self._env

    def native(self) -> Callable[[List[EtlExpression]], EtlExpression]:
        return self._native_function

    def call(self, args: List[EtlExpression]) -> EtlExpression:
        return self._native_function(args)

    def is_macro(self) -> bool:
        return self._is_macro

    def make_macro(self) -> None:
        self._is_macro = True


class EtlInt(EtlExpression):
    def __init__(self, value: int) -> None:
        assert type(value) is int
        self._value = value

    def readable_str(self) -> str:
        return str(self._value)

    def native(self) -> int:
        return self._value


class EtlVector(EtlExpression):
    def __init__(self, values: List[EtlExpression]) -> None:
        self._values = values

    def readable_str(self) -> str:
        return "(" + " ".join(map(lambda x: x.readable_str(), self._values)) + ")"

    def unreadable_str(self) -> str:
        return "(" + " ".join(map(lambda x: x.unreadable_str(), self._values)) + ")"

    def native(self) -> List[EtlExpression]:
        return self._values


class EtlHash_map(EtlExpression):
    def __init__(self, values: Dict[str, EtlExpression]) -> None:
        self._dict = values.copy()

    def readable_str(self) -> str:
        result_list: List[str] = []
        for x in self._dict:
            result_list.append(EtlString(x).readable_str())
            result_list.append(self._dict[x].readable_str())
        return "{" + " ".join(result_list) + "}"

    def unreadable_str(self) -> str:
        result_list: List[str] = []
        for x in self._dict:
            result_list.append(EtlString(x, is_already_encoded=True).unreadable_str())
            result_list.append(self._dict[x].unreadable_str())
        return "{" + " ".join(result_list) + "}"

    def native(self) -> Dict[str, EtlExpression]:
        return self._dict


class EtlNil(EtlExpression):
    def __init__(self) -> None:
        pass

    def readable_str(self) -> str:
        return "nil"

    def eval(self, environment) -> EtlExpression:
        return self

    def native(self) -> None:
        return None


class EtlBoolean(EtlExpression):
    def __init__(self, value: bool) -> None:
        self._value = value

    def readable_str(self) -> str:
        if self._value:
            return "true"
        return "false"

    def native(self) -> bool:
        return self._value


class EtlAtom(EtlExpression):
    def __init__(self, value: EtlExpression) -> None:
        self._value = value

    def native(self) -> EtlExpression:
        return self._value

    def readable_str(self) -> str:
        return "(atom " + str(self._value) + ")"

    def reset(self, value: EtlExpression) -> None:
        self._value = value
