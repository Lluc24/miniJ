grammar g;
root : (gen? '\n')* EOF ;

gen : expr                                   # genExpr
    | VAR '=:' expr                          # genAssign
    | VAR '=:' func                          # genFunc
    ;

expr : <assoc=right> expr operBin expr       # exprOperBin
     | operUn expr                           # exprOperUn
     | '(' expr ')'                          # exprPar
     | NUM+                                  # exprLlista
     | VAR                                   # exprVar
     ;

func : func '@:' func                        # funcComp
     | expr operBin ']'                      # funcOperBin
     | operUn                                # funcOperUn
     | '(' func ')'                          # funcPar
     ;

operBin : ('+' | '-' | '*' | '%' | '^' | '|' | '>' | '<' | '>=' | '<=' | '=' | '<>' | ',' | '#' | '{')('~')? ;
operUn  : (']' | '#' | 'i.' | operBin ':' | operBin '/' | VAR) ;

VAR  : ([a-z] | [A-Z])([a-z] | [A-Z] | [0-9] | '_')* ;
NUM : '_'?[0-9]+ ;

COM : 'NB.' ~[\n]* -> skip ;
WS  : [ \t\r]+ -> skip ;

LEXICAL_ERROR : . ;
