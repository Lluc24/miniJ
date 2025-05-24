// Gramatica per expressions senzilles
grammar exprs;
root : (gen? '\n')* EOF             // l'etiqueta ja es root
     ;

gen : expr                                   # genExpr
    | VAR '=:' expr                          # genAssign
    | VAR '=:' func                          # genFunc
    ;

expr : <assoc=right> expr binaryOper expr    # binOperExpr
     | unaryOper expr                        # unOperExpr
     | '(' expr ')'                          # parExpr
     | NUM+                                  # listExpr
     | VAR                                   # varExpr
     ;

func : func '@:' func                        # compFunc
     | expr binaryOper ']'                   # binaryFunc
     | unaryOper                             # unaryFunc
     ;

binaryOper : ('+' | '-' | '*' | '%' | '^' | '|' | '>' | '<' | '>=' | '<=' | '=' | '<>' | ',' | '#' | '{')('~')? ;
unaryOper  : (']' | '#' | 'i.' | binaryOper ':' | binaryOper '/' | VAR) ;

VAR  : ([a-z] | [A-Z])([a-z] | [A-Z] | [0-9] | '_')* ;
NUM : '_'?[0-9]+ ;

COM : 'NB.' ~[\r\n]* -> skip ;
WS  : [ \t\r]+ -> skip ;
