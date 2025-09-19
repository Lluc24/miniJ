# Introduction

This project was developed as part of the [GEI-LP](https://www.fib.upc.edu/en/studies/bachelors-degrees/bachelor-degree-informatics-engineering/curriculum/syllabus/LP) course (2024–2025 Q2) at Universitat Politècnica de Catalunya. miniJ is an interpreter of the language G, a simplified version of J (derived from APL), implemented using Python, ANTLR, and NumPy.

Through this work, I learned to:
- Understand the different phases of compilation, in particular lexical, syntactic, and semantic analysis.
- Use tools for building lexical and syntactic analyzers, such as ANTLR.
- Differentiate between the design of a compiler and an interpreter.

The project was evaluated by Professor `Edelmira Pasarella` and received the maximum grade (10/10).

The original project assignment can be found in this repository: [gebakx/lp-mini-j](https://github.com/gebakx/lp-mini-j) (in Catalan). The submission delivered for evaluation is the file `entrega.zip` included in this repository.

The following README text corresponds to the original project documentation written in Catalan.

## Estructura del projecte
Els fitxers que es poden trobar al projecte són els següents:
- `README.md`: Documentació del projecte.
- `Makefile`: Per generar els fitxers necessaris per a l'execució de l'intèrpret.
- `g.g4`: Fitxer de gramàtica ANTLR per al llenguatge G.
- `g.py`: Controlador principal del sistema. És el punt d'entrada del programa que executa l'intèrpret.
- `visitor.py`: Visitador per a l'arbre de sintaxi abstracte (AST) generat per ANTLR.
- `motor_g.py`: Motor d'execució encarregat d'encapsular la lògica operacional del llenguatge G.
- Els fitxers de prova:
    - Pels operadors aritmètics: `aritmetics.j` junt amb `aritmetics.out`.
    - Pels operadors booleans i relacionals: `booleans-i-relacionals.j` junt amb `booleans-i-relacionals.out`.
    - Per les funcions i variables: `funcions-i-variables.j` junt amb `funcions-i-variables.out`.
    - Els exemples proporcionats per l'enunciat: `exemples.j` junt amb `exemples.out`.
    - Pels errors sintàctics i lèxics: `errors-sintactics-i-lexics.j` junt amb `errors-sintactics-i-lexics.out`.
    - Pels errors semàntics: `errors-semantics.j` junt amb `errors-semantics.out`.

## Instal·lació

En aquesta pràctica s'ha utilitzat Python 3.10.9. Per instal·lar les dependències, cal crear i activar un entorn
virtual:

```bash
python -m venv env
source env/bin/activate 
```

Un cop activat l'entorn virtual, cal instal·lar les dependències:
```bash
pip install numpy antlr4-tools 
antlr4

pip install antlr4-python3-runtime
```

El Makefile permet generar els fitxers necessaris per a l'execució de l'intèrpret:
```bash
make
```

Finalment, per executar l'intèrpret, cal executar el fitxer `g.py` passant-li com a paràmetre el fitxer de codi G que es
vol interpretar. Utilitzarem el fitxer que conté els exemples proporcionats per l'enunciat per mostrar el funcionament:
```bash
python g.py exemples.j
```

## Funcionament del codi i decisions de disseny
En aquest apartat es documenta el funcionament del codi, les característiques principals i les decisions de
disseny preses. A més, els fitxers `g.py`, `visitor.py` i `motor_g.py` estan documentats seguint l'estil de docstrings
de Python, per tal de facilitar la comprensió del codi.

A l'hora de dissenyar l'intèrpret, s'ha decidit desacoblar la lògica interna de l'intèrpret (estructures de dades i
operacions) del visitador en dos fitxers separats: `visitor.py` i `motor_g.py`. A més de millorar la flexibilitat i 
mantenibilitat del codi, també obre les portes a utilitzar una llibreria diferent de Numpy per a les operacions i
representació de les dades.

Tots els errors es capturen i es mostren per pantalla per tal d'informar a l'usuari, tant els lèxics, sintàctics com
semàntics. Això evita que el programa s'aturi de forma inesperada.

### Gramàtica `g.g4`
Per tal de facilitar la comprensió de la gramàtica, afegim una breu descripció d'alt nivell de les regles:
1. El punt d'entrada de la gramàtica són les expressions genèriques `gen`. Corresponen a les sentències (línies de
codi) del llenguatge G.
2. Les expressions `expr` engloben totes les operacions amb llistes que es poden realitzar al llenguatge G. Tenen una
estructura recursiva i utilitzen associativitat a la dreta, ja que en G les expressions s'avaluen de dreta a esquerra.
3. Les funcions `func` representen les funcions definides per l'usuari. Suporta la composició de funcions.
4. Els operadors binaris `operBin` i unaris `operUn` s'han representat com a regles i no com a tokens, per tal que
l'analitzador sintàctic descendent LL(k) pugui tractar-los segons el context.

### Controlador `g.py`
El fitxer `g.py` és el punt d'entrada del programa. S'encarrega de fer l'anàlisi lèxica i sintàctica del codi G. En cas
de detectar errors sintàctics o lèxics, els mostra per pantalla junt amb l'estructura de l'AST i finalitza l'execució.
Si no hi ha errors, delega a `visitor.py` l'anàlisi semàntica de l'AST. Notar que es construeix l'AST sobre tot el
fitxer passat com a paràmetre. Això és diferent que analitzar línia a línia. Fixem-nos que si una línia té un error
lèxic o sintàctic, l'analitzador no continuarà:

```bash
echo "1 2 3 $ 1 2 3   NB. Error lexic" > prova.j
echo "1 2 3 + 1 2 3   NB. L'error anterior impedeix que s'analitzi" >> prova.j
python g.py prova.j
```

Tanmateix, això facilita que el visitador sigui l'encarregat d'emmagatzemar les variables i funcions definides en línies 
anteriors, fent-les disponibles per a les línies següents.

```bash
echo "x =: 1 2 3 4" > prova.j
echo "x * 2   NB. Resultat: 2 4 6 8" >> prova.j
python g.py prova.j
```

### Visitador `visitor.py`
El fitxer `visitor.py` implementa el patró de disseny visitador per a l'AST generat per ANTLR. Els errors es tracten en
el mètode `visitGenExpr` encarregat de visitar la regla `gen`. Això permet que els errors semàntics es tractin de forma
independent entre dues línies (a diferència dels lèxics i sintàctics). Per exemple:

```bash
echo "1 2 3 + 1 2   NB. Error semantic (length error)" > prova.j
echo "5 * 5         NB. L'error anterior no impedeix que s'analitzi" >> prova.j
python g.py prova.j
```

S'ha decidit utilitzar l'estructura de dades del diccionari com a taula de símbols per emmagatzemar les variables i
funcions definides (que estan en taules diferents). A diferència de la declaració de variables, la qual avalua les 
expressions que se li assignen, les funcions simplement guarden l'arbre AST corresponent a l'expressió. Això simplifica
el codi, fent que quan el paràmetre de la funció estigui disponible s'avaluï tot junt de la mateixa forma que les altres
expressions. També introdueix l'avaluació mandrosa en el nostre intèrpret!

```bash
echo "f =: (1 2 3 + 4 5) * ]   NB. Per ara no hi ha error" > prova.j
echo "5 ^ 3                    NB. Resultat: 125" >> prova.j
echo "f 5                      NB. Error semantic (length error)" >> prova.j
python g.py prova.j
```

L'altra estructura de dades important és la pila, la qual s'encarrega d'emmagatzemar els operands. Quan s'avalua un
operador, es desempilen els operands necessaris, s'aplica l'operador i es torna a apilar el resultat. Això implica que
l'avaluació d'una expressió sempre guarda el resultat al damunt de la pila. També, quan les funcions són avaluades,
agafen el paràmetre necessari de la pila. Notar que, a diferència de la convenció, el primer operand és el de dalt de
la pila i el segon operand és el de sota. Això és degut a la naturalesa de l'avaluació de dreta a esquerra i de les
funcions que contenen el primer operand:

```bash
echo "f =: 0 = ]     NB. Per ara no s'avalua" > prova.j
echo "f 1 2          NB. Primer s'empila 1 2, i quedara sota de 0 en la pila" >> prova.j
python g.py prova.j
```
S'ha decidit utilitzar una pila en comptes de funcions de Python per senzillesa i escalabilitat del codi. La pila permet
implementar operands i funcions amb múltiples valors de forma senzilla i eficient.

### Motor d'execució `motor_g.py`
El fitxer `motor_g.py` és el motor d'execució encarregat d'encapsular la lògica operacional del llenguatge G. Utilitza
els vectors de Numpy per representar les llistes i efectuar les operacions. A més, s'encarrega de verificar els errors
semàntics que hi puguin haver, com ara errors de longitud o tipus de dades.

Abans d'apilar les llistes llegides, la classe `visitor.py` utilitza el mètode `codifica_llista` de 
`motor_g.py` per convertir-les en vectors. El mateix quan necessita imprimir-les per pantalla en codificació de J,
utilitzant el mètode `descodifica_llista`.

També, quan necessita aplicar un operador, la classe `visitor.py` demana la funció corresponent a `motor_g.py`,
passant-li la codificació en string de l'operador. La classe `motor_g.py` s'encarrega de buscar la funció de numpy
corresponent mitjançant dos diccionaris: un per operacions unàries i un altre per binàries.

Per fer comprovació d'errors semàntics, un dels mètodes utilitzats és la clausura de funcions: pels operadors binaris en
els quals cal comprovar que la llargada de les llistes operands sigui correcta, donat que `motor_g.py` no sap els
paràmetres, retorna una funció amb clausura que comprovarà les llargades quan s'invoqui.

```python
def _comprovacio_llargada(self, func):
    """
    Retorna la funció passada com a paràmetre afegint comprovació de llargades.
    Utilitza clausura de funcions.
    """
    def aplicacio_segura(x, y):
        if np.size(x) == np.size(y) or np.size(x) == 1 or np.size(y) == 1:
            return func(x, y)
        else:
            raise ValueError("length error")
    return aplicacio_segura
```

## Jocs de prova
Els fitxers `aritmetics.j`, `booleans-i-relacionals.j`, `funcions-i-variables.j`, `exemple.j`, 
`errors-sintactics-i-lexics.j` i `errors-semantics.j` corresponen a jocs de prova que verifiquen el correcte
funcionament de l'intèrpret. Venen acompanyats dels respectius fitxers de sortida `.out`. Per executar un joc de prova,
com per exemple `aritmetics.j`, pot fer-se de la següent forma:

```bash
python g.py aritmetics.j > aritmetics.tmp
diff aritmetics.out aritmetics.tmp
rm aritmetics.tmp
```

També es poden executar tots alhora. Per fer-ho, cal verificar que no hi hagi altres fitxers `.j`, com el `prova.j`
creat anteriorment per veure el funcionament de l'intèrpret. En cas de ser-hi, cal esborrar-lo amb `rm prova.j`. A
continuació, el següent script executa tots els jocs de prova (es pot copiar i enganxar directament a la consola):

```bash
for fitxer_test in *.j
do
    nom_test=$(basename "$fitxer_test" .j)
	sortida_esperada="${nom_test}.out"
	sortida_obtinguda="${nom_test}.tmp"
	python g.py "$fitxer_test" > "$sortida_obtinguda"
	echo "Diferencies entre $sortida_esperada i $sortida_obtinguda:"
	diff "$sortida_esperada" "$sortida_obtinguda"
	rm "$sortida_obtinguda"
done
```

