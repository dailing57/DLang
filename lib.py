from cmath import isnan
from math import ceil, floor, sqrt
from random import randint
from type import *


class DArray:
    def __init__(self, name, value, father=None) -> None:
        self.name = name
        self.value: list = value
        self.father = father


arrs: dict[str, DArray] = {}

Input: list[str] = []
pos = 0


def nextNumber():
    global pos
    val = int(Input[pos])
    pos += 1
    if not isnan(val):
        return val
    else:
        raise(Error('Input Error, expects a Number'))


def nextFloat():
    global pos
    val = float(Input[pos])
    pos += 1
    if not isnan(val):
        return val
    else:
        raise(Error('Input Error, expects a Float'))


def nextString():
    global pos
    res = Input[pos]
    pos += 1
    return res


def nextBool():
    global pos
    val = Input[pos]
    pos += 1
    if val == true:
        return True
    if val == false:
        return False
    else:
        raise(Error('Input Error, expects a Bool'))


def output(text):
    print(text)


def arrayNew(name):
    fa = arrs[name] if name in arrs else None
    arrs[name] = DArray(name, [], fa)


def arrayAssign(name, len):
    if name not in arrs:
        raise(Error(f'Array "{name}" is not defined'))
    arr = arrs[name]
    arr.value = [0 for i in range(len)]


def arrayLen(name):
    if name not in arrs:
        raise(Error(f'Array "{name}" is not defined'))
    return len(arrs[name].value)


def arrayPush(name, x):
    if name not in arrs:
        raise(Error(f'Array "{name}" is not defined'))
    arr = arrs[name]
    arr.value.append(x)
    return len(arr.value)


def arrayPop(name):
    if name not in arrs:
        raise(Error(f'Array "{name}" is not defined'))
    return arrs[name].value.pop()


def arrayGet(name, i):
    if name not in arrs:
        raise(Error(f'Array "{name}" is not defined'))
    arr = arrs[name]
    if i < 0 or i >= len(arr.value):
        raise(Error('Array "{arr.name}" visit out of bound'))
    return arr.value[i]


def arraySet(name, i, x):
    if name not in arrs:
        raise(Error(f'Array "{name}" is not defined'))
    arr = arrs[name]
    if i < 0 or i >= len(arr.value):
        raise(Error('Array "{arr.name}" visit out of bound'))
    arr.value[i] = x


def arrayClear(name):
    if name not in arrs:
        raise(Error(f'Array "{name}" is not defined'))
    arrs[name].value = []


def arrayDelete(name):
    if name not in arrs:
        raise(Error(f'Array "{name}" is not defined'))
    arr = arrs[name]
    if arr.father is not None:
        arrs[name] = arr.father
    else:
        arrs.pop(name)


def stringGet(s, i):
    if i < 0 or i >= len(s):
        raise(Error('visit undefined memory'))
    return s[i]


IOLib: list[BuiltinFunction] = [
    BuiltinFunction(
        name=Lib_In + DoubleColon + Lib_hasNext,
        args=[],
        type=boolType,
        fn=(lambda: pos < len(Input))
    ),
    BuiltinFunction(
        name=Lib_In + DoubleColon + Lib_nextNumber,
        args=[],
        type=numberType,
        fn=nextNumber
    ),
    BuiltinFunction(
        name=Lib_In + DoubleColon + Lib_nextFloat,
        args=[],
        type=floatType,
        fn=nextFloat
    ),
    BuiltinFunction(
        name=Lib_In + DoubleColon + Lib_nextString,
        args=[],
        type=stringType,
        fn=nextString
    ),
    BuiltinFunction(
        name=Lib_In + DoubleColon + Lib_nextBool,
        args=[],
        type=boolType,
        fn=nextBool
    ),
    BuiltinFunction(
        name=Lib_Out,
        args=[stringType],
        type=voidType,
        fn=output
    ),
]
ArrayLib: list[BuiltinFunction] = [
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_new,
        args=[stringType],
        type=voidType,
        fn=arrayNew
    ),
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_assign,
        args=[stringType, numberType],
        type=voidType,
        fn=arrayAssign
    ),
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_length,
        args=[stringType],
        type=numberType,
        fn=arrayLen
    ),
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_push,
        args=[stringType],
        type=numberType,
        fn=arrayPush
    ),
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_pop,
        args=[stringType],
        type=numberType,
        fn=arrayPop
    ),
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_get,
        args=[stringType, numberType],
        type=numberType,
        fn=arrayGet
    ),
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_set,
        args=[stringType, numberType, numberType],
        type=voidType,
        fn=arraySet
    ),
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_clear,
        args=[stringType],
        type=voidType,
        fn=arrayClear
    ),
    BuiltinFunction(
        name=Lib_Array + DoubleColon + Lib_Delete,
        args=[stringType],
        type=voidType,
        fn=arrayDelete
    ),
]

StringLib: list[BuiltinFunction] = [
    BuiltinFunction(
        name=Lib_String + DoubleColon + Lib_length,
        args=[stringType],
        type=numberType,
        fn=(lambda s: len(s))
    ),
    BuiltinFunction(
        name=Lib_String + DoubleColon + Lib_get,
        args=[stringType, numberType],
        type=stringType,
        fn=stringGet
    ),
    BuiltinFunction(
        name=Lib_String + DoubleColon + Lib_to_number,
        args=[stringType],
        type=numberType,
        fn=(lambda s:int(s))
    ),
    BuiltinFunction(
        name=Lib_String + DoubleColon + Lib_to_float,
        args=[stringType],
        type=floatType,
        fn=(lambda s:float(s))
    ),
]

NumberLib: list[BuiltinFunction] = [
    BuiltinFunction(
        name=Lib_Number + DoubleColon + Lib_to_string,
        args=[numberType],
        type=stringType,
        fn=(lambda s:str(s))
    ),
    BuiltinFunction(
        name=Lib_Number + DoubleColon + Lib_max,
        args=[numberType, numberType],
        type=numberType,
        fn=(lambda a, b:max(a, b))
    ),
    BuiltinFunction(
        name=Lib_Number + DoubleColon + Lib_min,
        args=[numberType, numberType],
        type=numberType,
        fn=(lambda a, b:min(a, b))
    ),
    BuiltinFunction(
        name=Lib_Number + DoubleColon + Lib_abs,
        args=[numberType],
        type=numberType,
        fn=(lambda a, b:abs(a, b))
    ),
    BuiltinFunction(
        name=Lib_Number + DoubleColon + Lib_rand,
        args=[numberType, numberType],
        type=numberType,
        fn=(lambda l, r:randint(l, r))
    ),
]

FloatLib: list[BuiltinFunction] = [
    BuiltinFunction(
        name=Lib_Float + DoubleColon + Lib_to_string,
        args=[floatType],
        type=stringType,
        fn=(lambda a:str(a))
    ),
    BuiltinFunction(
        name=Lib_Float + DoubleColon + Lib_floor,
        args=[floatType],
        type=numberType,
        fn=(lambda a:floor(a))
    ),
    BuiltinFunction(
        name=Lib_Float + DoubleColon + Lib_round,
        args=[floatType],
        type=numberType,
        fn=(lambda a:round(a))
    ),
    BuiltinFunction(
        name=Lib_Float + DoubleColon + Lib_ceil,
        args=[floatType],
        type=numberType,
        fn=(lambda a:ceil(a))
    ),
    BuiltinFunction(
        name=Lib_Float + DoubleColon + Lib_max,
        args=[floatType, floatType],
        type=floatType,
        fn=(lambda a, b:max(a, b))
    ),
    BuiltinFunction(
        name=Lib_Float + DoubleColon + Lib_min,
        args=[floatType, floatType],
        type=floatType,
        fn=(lambda a, b:min(a, b))
    ),
    BuiltinFunction(
        name=Lib_Float + DoubleColon + Lib_abs,
        args=[floatType],
        type=floatType,
        fn=(lambda a:abs(a))
    ),
    BuiltinFunction(
        name=Lib_Float + DoubleColon + Lib_sqrt,
        args=[floatType],
        type=floatType,
        fn=(lambda a:sqrt(a))
    ),
]


def initInputHook(inp):
    global arrs, Input, pos
    arrs.clear()
    Input = inp if inp is not None else []
    pos = 0


beforeRunHooks = [initInputHook]


def clearHook(*arg):
    global arrs, Input, pos
    Input = []
    arrs.clear()
    pos = 0


afterRunHooks = [clearHook]
