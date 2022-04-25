# DLang
DL's Language 

AST类图:

```mermaid
classDiagram
	class BasicASTNode{
		type : ASTNodeType
		visit()
	}
	BasicASTNode <|-- RootASTNode
	class RootASTNode{
		fns : list[FunctionASTNode]
		main : FunctionASTNode
		merge()
		visit()
	}
	RootASTNode --> FunctionASTNode
	
    BasicASTNode <|-- FunctionASTNode
	class FunctionASTNode{
        name: string;
        returnType: ValueType | VoidType;
        haveReturn: boolean;
        args: ArgDefineListASTNode;
        statements: StatementASTNode[]
        getArgsType()
        visit(context: Context): NodeVisitorReturn
	}
	
	FunctionASTNode --> StatementASTNode
	StatementListASTNode --> StatementASTNode
	
	BasicASTNode <|-- StatementListASTNode
	class StatementListASTNode{
        statements: StatementASTNode[] = [];
        createContext: boolean;
        haveReturn: boolean = false;
        merge(other: StatementListASTNode)
        visit(context: Context): NodeVisitorReturn
	}
	BasicASTNode <|-- IfStatementASTNode
	class IfStatementASTNode{
        condition: ValueASTNode;
        body: StatementASTNode;
        elseBody?: StatementASTNode;
        haveReturn()
        visit(context: Context): NodeVisitorReturn
	}
	IfStatementASTNode --> ValueASTNode
	IfStatementASTNode --> StatementASTNode
	IfStatementASTNode --> NodeVisitorReturn
	BasicASTNode <|-- WhileStatementASTNode
	
	class WhileStatementASTNode{
        condition: ValueASTNode;
        body: StatementASTNode;
        visit(context: Context): NodeVisitorReturn
	}
	WhileStatementASTNode --> ValueASTNode
	WhileStatementASTNode --> StatementASTNode
	WhileStatementASTNode --> NodeVisitorReturn
	
	BasicASTNode <|-- ForStatementASTNode
	class ForStatementASTNode{
        init: DefineListASTNode | UnitOPASTNode[];
        condition: ValueASTNode;
        update: UnitOPASTNode[];
        body: StatementASTNode;
        visit(context: Context): NodeVisitorReturn 
	}
	ForStatementASTNode --> DefineListASTNode
	ForStatementASTNode --> UnitOPASTNode
	ForStatementASTNode --> ValueASTNode
	ForStatementASTNode --> StatementASTNode
	ForStatementASTNode --> NodeVisitorReturn
	
	BasicASTNode  <|-- DefineListASTNode
	class DefineListASTNode{
        defs: DefineASTNode[] = [];
        isConst: boolean = false;
        merge(other: DefineListASTNode)
        visit(context: Context): NodeVisitorReturn
	}
	DefineListASTNode --> DefineASTNode
	DefineListASTNode --> NodeVisitorReturn
	BasicASTNode  <|-- DefineASTNode
	class DefineASTNode{
        dst: Variable;
        src?: ValueASTNode;
        visit(context: Context): NodeVisitorReturn
	}
	DefineListASTNode --> NodeVisitorReturn
	DefineListASTNode --> Variable
	DefineListASTNode --> ValueASTNode
	
	BasicASTNode <|-- ArgDefineListASTNode
	class ArgDefineListASTNode{
    	defs: Variable[] = [];
        merge(other: ArgDefineListASTNode)
        visit(context: Context): NodeVisitorReturn
	}
	ArgDefineListASTNode --> Variable
	ArgDefineListASTNode --> ArgDefineListASTNode
	ArgDefineListASTNode --> NodeVisitorReturn
	BasicASTNode <|-- LeafASTNode
	class LeafASTNode{
		dst: Variable | Literal;
		visit(context: Context): NodeVisitorReturn
	}
	LeafASTNode --> NodeVisitorReturn
	LeafASTNode --> Variable
	LeafASTNode --> Literal
	
	BasicASTNode <|-- BinOPASTNode
	class BinOPASTNode{
        dst: Variable;
        x: ValueASTNode;
        y: ValueASTNode;
        visit(context: Context): NodeVisitorReturn
	}
	BinOPASTNode --> ValueASTNode
	BinOPASTNode --> Variable
	BinOPASTNode --> NodeVisitorReturn
	
	BasicASTNode <|-- UnitOPASTNode
	class UnitOPASTNode{
        dst: Variable;
        src: ValueASTNode;
        visit(context: Context): NodeVisitorReturn
	}
	UnitOPASTNode --> NodeVisitorReturn
	UnitOPASTNode --> ValueASTNode
	UnitOPASTNode --> Variable
	
	BasicASTNode <|-- FunctionCallASTNode
	class FunctionCallASTNode{
        name: string;
        args: FunctionCallArgListASTNode;
        visit(context: Context): NodeVisitorReturn
	}
	FunctionCallASTNode --> NodeVisitorReturn
	FunctionCallASTNode --> FunctionCallArgListASTNode
	
	BasicASTNode <|-- FunctionCallArgListASTNode
	class FunctionCallArgListASTNode{
        args: ValueASTNode[] = [];
        types: ValueType[] = [];
        merge(other: FunctionCallArgListASTNode)
        length()
        checkType(realArgs: ValueType[])
        visit(context: Context): NodeVisitorReturn
	}
	FunctionCallArgListASTNode --> ValueASTNode
	FunctionCallArgListASTNode --> NodeVisitorReturn
	BasicASTNode <|-- FunctionReturnASTNode
	class FunctionReturnASTNode{
		src?: ValueASTNode;
		visit(context: Context): NodeVisitorReturn
	}
	FunctionReturnASTNode --> FunctionReturnCode

```

如何实现将函数作为变量？

1. 在函数（甲）内部定义函数（乙）

2. 返回定义的函数（乙）

3. 声明变量丙等于调用甲的返回值

4. 需要把丙注册到函数池

   如何实现这个在函数内部的注册功能？

   如果这个函数存在外部引用，意味着需要将这些外部引用转化为全局变量





