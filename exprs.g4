// Gramatica per expressions senzilles
grammar exprs;
root : (gen? '\n')* EOF             // l'etiqueta ja es root
     ;

gen : expr                                   # genExpr
    ;

expr : <assoc=right> expr operBinari expr    # binOperExpr
     | list                                  # listExpr
     ;
list : list NUM                              # buildList
     | NUM                                   # baseList
     ;


operBinari : ('+' | '-' | '*' | '/' | '%' | '^')
           ;
NUM : '_'?[0-9]+ ;
WS  : [ \t\r]+ -> skip ;
