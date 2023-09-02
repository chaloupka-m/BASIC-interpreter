# Interpret vlastní verze programovacího jazyka BASIC
BASIC (Beginner's All-purpose Symbolic Instruction Code) je interpretovaný programovací jazyk s imperativním paradigmatem. Díky své jednoduché syntaxi byl v minulosti používaný pro výuku programování a tvorbu jednoduchých aplikací.
## Spuštění interpretu
Ke spuštění interpretu je nutné mít na počítači nainstalovaný Python.
Pokud chcete spustit soubor s kódem BASIC, zadejte:
```
python basic.py "adresa_souboru"
```
### Textové rozhraní programu
Pokud chcete spustit textové rozhraní programu v příkazové řádce, zadejte:
```
python basic.py
```
K ovládání textového rozhraní slouží příkazy:
- RUN - spustí interpretaci aktuálního programu
- LIST - vypíše na konzoli zdrojový kód
- END - ukončí textové rozhraní programu
- CLS - vymaže obsah příkazového řádku
- NEW - vytvoří nový program
- DEL _Line number_ - smaže řádek
- OPEN _Filename_ - otevře soubor s kódem BASIC
- SAVE - uloží změny do otevřeného souboru
- SAVE _Filename_ - uloží zdrojový kód do souboru
## Syntaxe jazyka BASIC
- BASIC není senzitivní na velikost písmen.
- Není třeba deklarovat proměnné.
- Neinicializované proměnné jsou rovny 0.
- Názvy proměnných mohou obsahovat písmena bez diakritiky, číslice a symbol '_', mohou mít libovolnou délku, nesmí ovšem začínat číslicí.
- Datovými typy jsou zde Integer, Float, String a Array.
- Před každým příkazem je nutné napsat číslo řádku, které musí být nezáporné celé číslo.
- Pokud zvolíte číslo řádku, které již existuje, původní příkaz bude nahrazen novým.
- Při interpretaci kódu se příkazy provádí v pořadí čísel řádků.
### Příkazy (Statements)
#### PRINT _Expression_
Vypíše hodnotu výrazu na konzoli.
```
10 PRINT 1 + 2 * 3
```
Na místo parametru lze zadat i více výrazů oddělených středníkem:
```
10 PRINT "1 + 2 = "; 1 + 2
```
#### INPUT _Expression_; _Identifier_
Vypíše hodnotu výrazu na konzoli a vyžádá si uživatelský vstup, který uloží do proměnné.
```
10 INPUT "Zadejte své jméno: "; NAME
```
#### REM _Comment_
Komentář je používán pro snazší orientaci v kódu, interpret komentář ignoruje.
```
10 REM Toto je komentář
```
#### END
Ukončí program
```
10 END
20 REM Tento řádek už nebude vykonán
```
#### LET _Identifier_ = _Expression_
Inicializuje proměnnou (uloží hodnotu výrazu do proměnné).
```
10 LET NUMBER = 5
```
#### GOTO _Line number_
Přeskočí program na určenou řádku kódu.
```
10 GOTO 30
20 REM Tento řádek bude přeskočen
30 REM Program pokračuje zde
```
#### GOSUB _Line number_, RETURN
Zahájí tzv. subrutinu. Program přeskočí na určenou řádku kódu, pokračuje řádek po řádce až k příkazu RETURN, který subrutinu ukončí a program pokračuje dále za příkazem GOSUB.
```
10 GOSUB 1000
20 REM Krok 3
30 END
1000 REM Krok 1
1010 REM Krok 2
1020 RETURN
```
#### IF _Expression_ THEN _Statement_ ELSEIF _Expression_ THEN _Statement_ ELSE _Statement_
Příkaz IF kontroluje podmínku. Pokud je podmínka pravdivá, provede následující příkaz, pokud ne, pokračuje dalšími podmínkami ELSEIF (může jich být i více). Není-li žádná z podmínek pravdivá, program pokračuje příkazem ELSE.
```
10 IF X < 0 THEN PRINT "X je záporné číslo" ELSEIF X = 0 THEN PRINT "X je nula" ELSE PRINT "X je kladné číslo"
```
Příkazy ELSEIF a ELSE nejsou povinné a lze je kompletně vynechat nebo použít jen jeden z nich:
```
10 IF X = 1 THEN PRINT "X je rovno 1"
20 IF Y = 0 THEN PRINT "Y je nula" ELSE PRINT "Y je nenulové číslo"
30 IF Z = 0 THEN PRINT "Z je nula" ELSEIF Z = 1 THEN PRINT "Z je rovno 1"
```
Místo příkazů lze zadat v podmínce i čísla řádků, program je bude brát jako příkazy GOTO.
Tento zápis:
```
10 IF X = 0 50
```
je ekvivalentní zápisu:
```
10 IF X = 0 GOTO 50
```
#### FOR _Identifier_ = _Expression_ TO _Expression_ STEP _Expression_, NEXT _Identifier_
Uloží hodnotu prvního výrazu do proměnné. Následující příkazy se budou provádět v cyklu. Na konci každého cyklu definovaného příkazem NEXT s identickým názvem proměnné se hodnota proměnné navýší o hodnotu výrazu STEP, pokud hodnota proměnné nepřesáhne hodnotu výrazu TO. V tom případě se cyklus ukončí. Výraz STEP lze v programu vynechat, v takovém případě se hodnota výrazu nastaví na 1.
```
10 REM Program, který vypíše hodnoty od 0 do 10
20 FOR I = 0 TO 10
30 PRINT I
30 NEXT I
```
#### CLS
Vymaže grafický výstup.
```
10 PRINT "Tento řádek se vypíše na konzoli, ale bude vzápětí smazán"
20 CLS
30 PRINT "Tento řádek bude na konzoli vidět po skončení programu"
```
#### PAUSE _Duration_
Pozastaví program na určitý počet milisekund.
```
10 PRINT "Další řádek se na konzoli vypíše za 5 sekund..."
20 PAUSE 5000
30 PRINT "Tento řádek se na konzoli vypsal po 5 sekundách"
```
#### ARRAY _Identifier_
Deklaruje proměnnou jako dynamické pole. Velikost pole se může za běhu programu měnit. K jeho hodnotám se přistupuje pomocí indexu od 0. Hodnoty mohou být kteréhokoli datového typu: Integer, Float a String. Zvláštním případem obsažených hodnot jsou další pole, poté se jedná o vícedimenzionální pole, která jsou v této verzi BASICu také podporovaná.
```
10 ARRAY A
20 LET A[0] = 5
30 LET A[1] = 3.14
40 LET A[2] = "Textový řetězec"
50 PRINT "5 * 3.14 = "; A[0] * A[1]

60 ARRAY B
70 LET B[0] = 5
80 LET B[1] = A
90 PRINT "5 * 3.14 = "; B[1][0] * B[1][1]
```
### Výrazy (Expressions)
#### Aritmetické operace
Symboly pro aritmetické operace: sčítání '+', odčítání '-', násobení '*', dělení '/', umocňování '**' a modulo '%'
#### Relační operace
Symboly pro relační operace: rovná se '=', nerovná se '<>', větší než '>', menší než '<', větší nebo rovno '>=' a menší nebo rovno '<='
#### Logické operace
Klíčová slova pro logické operace: konjunkce 'AND' a disjunkce 'OR'
### Funkce (Functions)
- Podporované číselné funkce:
    - RAND(X) - vrátí náhodné číslo od 0 do výše hodnoty argumentu
    - ABS(X) - vrátí absolutní hodnotu argumentu
    - SGN(X) - pokud je argument menší než 0, vrátí -1, pokud je roven 0, vrátí 0, jinak vrátí 1
    - ROUND(X) - vrátí zaokrouhlenou hodnotu argumentu na jednotky
    - FLOOR(X) - vrátí hodnotu argumentu zaokrouhlenou dolů na nejbližší nižší celé číslo.
    - EXP(X) - vrátí přirozenou exponenciální hodnotu e<sup>x</sup> argumentu
    - LOG(X) - vrátí přirozený logaritmus argumentu
    - SQR(X) - vrátí druhou odmocninu z argumentu
    - Goniometrické funkce:
        - SIN(X)
        - COS(X)
        - TAN(X)
    - Cyklometrické funkce
        - ASIN(X)
        - ACOS(X)
        - ATAN(X)
- Textové funkce
    - UPPERCASE(_String_) - vrátí původní textový řetězec převedený na velká písmena
    - LOWERCASE(_String_) - vrátí původní textový řetězec převedený na malá písmena
    - Funkce pro práci s textovými řetězci i s poli
        - LEN(_String_/_Array_) - vrátí délku textového řetězce/pole
        - LEFT(_String_/_Array_, _Integer n_) - vrátí 'n' znaků (prvků v poli) zleva
        - RIGHT(_String_/_Array_, _Integer n_) - vrátí 'n' znaků (prvků v poli) zprava
        - MID(_String_/_Array_, _Integer start_, _Integer n_) - vrátí 'n' znaků (prvků v poli) od pozice 'start'