from xml.dom.minicompat import NodeList
from tac import *
from type import *
class CallStackRecord:
    def __init__(self,name,pc,sp) -> None:
        self.name = name
        self.pc = pc
        self.sp = sp

def vm(code:list[ThreeAddressCode],globalFns:dict[str,GlobalFunction],args:list[LiteralCode]):
    varStk = []
    callStk:list[CallStackRecord] = []
    globalVar = [None]
    pc = 0
    sp = 0
    fnName = '__ENTRY__'
    def allocateStack(cnt):
        while cnt > 0:
            cnt -= 1
            varStk.append(None)
    def releaseStack(cnt):
        while cnt > 0:
            cnt-=1
            varStk.pop()
    def getValue(pos:Union[VariableCode,LiteralCode]):
        nonlocal fnName, sp, pc
        if hasattr(pos,'address'):
            val = varStk[sp + pos.address]
            if val == None:
                raise(Error('visit undefined memory'))
            return val
        elif hasattr(pos,globalAddress):
            val = globalVar[pos.globalAddress]
            if val == None:
                raise(Error('visit undefined memory'))
            return val
        else:
            return pos.value
    def setValue(pos:VariableCode,val):
        nonlocal fnName, sp, pc
        if hasattr(pos,'address'):
            address = sp + pos.address
            if address < 0 or address >= len(varStk):
                raise('visit out of stack range')
            varStk[address] = val
        else:
            address = pos.globalAddress
            if address < 0 or address >= len(globalVar):
                raise(Error('visit out of global memory range'))
            varStk[address] = val
    def TAC_nop(code):
        pass

    def TAC_functionCall(code:ThreeAddressCode):
        nonlocal fnName, sp, pc
        name = code.name
        if name in globalFns:
            fnObj = globalFns[name]
            if hasattr(fnObj,'address'):
                callStk.append(CallStackRecord(name=fnName,sp=sp,pc=pc))
                fnName = name
                sp = len(varStk)
                pc = fnObj.address - 1
                allocateStack(fnObj.memCount)
            else:
                args = varStk[-len(fnObj.args):]
                varStk = varStk[:-len(fnObj.args)]
                value = fnObj.fn(*args)
                globalVar[0] = value
        else:
            raise(Error(f'function "{name}" is not defined'))

    def TAC_functionReturn(code: ThreeAddressCode):
        nonlocal fnName, sp, pc
        returnCode = code
        name = returnCode.name
        if returnCode.src is not None:
            globalVar[0] = getValue(returnCode.src)
        fnObj = globalFns[name]
        releaseStack(fnObj.memCount + len(fnObj.args))
        if len(callStk) == 0:
            raise(Error('call stack is empty'))
        record = callStk.pop()
        fnName = record.name
        pc = record.pc
        sp = record.sp
    
    def TAC_pushStack(code: ThreeAddressCode):
        value = getValue(code.src)
        varStk.append(value)
    
    def TAC_goto(code: ThreeAddressCode):
        nonlocal fnName, sp, pc
        pc += code.offset

    def TAC_ifGoto(code: ThreeAddressCode):
        value = getValue(code.src)
        fg = value
        if type(value) == int:
            if value == 0:
                fg = False
        elif type(value) == str:
            if len(value) == 0:
                fg = False
        elif type(value) == bool:
            if not value:
                fg = False
        if fg == code.target:
            pc += code.offset

    def TAC_Assign(code: ThreeAddressCode):
        value = getValue(code.src)
        setValue(code.dst,value)
    
    def TAC_not(code: ThreeAddressCode):
        value = getValue(code.src)
        if type(value) == bool:
            setValue(code.dst,not value)
        elif type(value) == int:
            setValue(code.dst,value==0)
        elif type(value) == str:
            setValue(code.dst,len(value) == 0)
        else:
            setValue(code.dst,not value)
    
    def TAC_and(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x and y)
    
    def TAC_or(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x or y)

    def TAC_equal(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x == y)

    def TAC_notEqual(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x != y)
        
    def TAC_LE(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x <= y)

    def TAC_LT(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x < y)

    def TAC_GE(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x >= y)

    def TAC_GT(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x > y)

    def TAC_Neg(code: ThreeAddressCode):
        val = getValue(code.src)
        setValue(code.dst,-val)

    def TAC_plus(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x + y)

    def TAC_minus(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x - y)

    def TAC_mul(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x * y)

    def TAC_div(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        val = x//y if code.x.type == numberType and code.y.type == numberType else x/y
        setValue(code.dst,val)
    
    def TAC_mod(code: ThreeAddressCode):
        x = getValue(code.x)
        y = getValue(code.y)
        setValue(code.dst,x % y)
    
    action = {
        ThreeAddressCodeType.NOP: TAC_nop,
        ThreeAddressCodeType.FunctionCall:TAC_functionCall,
        ThreeAddressCodeType.FunctionReturn:TAC_functionReturn,
        ThreeAddressCodeType.PushStack:TAC_pushStack,
        ThreeAddressCodeType.Goto:TAC_goto,
        ThreeAddressCodeType.IfGoto:TAC_ifGoto,
        ThreeAddressCodeType.Assign:TAC_Assign,
        ThreeAddressCodeType.Not:TAC_not,
        ThreeAddressCodeType.And:TAC_and,
        ThreeAddressCodeType.Or:TAC_or,
        ThreeAddressCodeType.Equal:TAC_equal,
        ThreeAddressCodeType.NotEqual:TAC_notEqual,
        ThreeAddressCodeType.LessOrEqual:TAC_LE,
        ThreeAddressCodeType.LessThan:TAC_LT,
        ThreeAddressCodeType.MoreOrEqual:TAC_GE,
        ThreeAddressCodeType.MoreThan:TAC_GT,
        ThreeAddressCodeType.Negative:TAC_Neg,
        ThreeAddressCodeType.Plus:TAC_plus,
        ThreeAddressCodeType.Minus:TAC_minus,
        ThreeAddressCodeType.Mul:TAC_mul,
        ThreeAddressCodeType.Div:TAC_div,
        ThreeAddressCodeType.Mod:TAC_mod,
    }

    for arg in args:
        varStk.append(arg.value)
    sp = len(varStk)
    while pc < len(code):
        action[code[pc].type](code[pc])
        if len(callStk) == 0:
            return
        pc+=1