// Gramatica per expressions senzilles
grammar exprs;
root : (gen? '\n')* EOF             // l'etiqueta ja es root
     ;

gen : expr                                   # genExpr
    | VAR ':=' expr                          # genAssign
    ;

expr : <assoc=right> expr operBinari expr    # binOperExpr
     | '(' expr ')'                          # parExpr
     | NUM+                                  # listExpr
     | VAR                                   # varExpr
     ;


operBinari : ('+' | '-' | '*' | '/' | '%' | '^' | '|');

VAR  : '_'?([a-z] | [A-Z])([a-z] | [A-Z] | [0-9] | '_')* ;
NUM : '_'?[0-9]+ ;
COMMENT : 'NB.'~('\n') -> skip;
WS  : [ \t\r]+ -> skip ;
