# Interpret programovacího jazyka BASIC
BASIC (Beginner's All-purpose Symbolic Instruction Code) je interpretovaný programovací jazyk s naivním (popř. imperativním) paradigmatem. Díky své jednoduché syntaxi byl v minulosti používaný pro výuku programování a tvorbu jednoduchých aplikací.
## Spuštění interpretu
Ke spuštění interpretu je nutné mít na počítači nainstalovaný Python.<br>
Pokud chcete spustit soubor s kódem BASIC, zadejte:
```
python basic.py "adresa_souboru"
```
Adresa souboru může být absolutní i relativní k aktuálnímu adresáři.
### Textové rozhraní interpretu
Pokud chcete spustit textové rozhraní programu v příkazovém řádku, zadejte:
```
python basic.py
```
K ovládání textového rozhraní slouží příkazy:
- RUN – spustí interpretaci aktuálního programu
- LIST – postupně vypíše na konzoli všechny řádky zdrojového kódu
- END – ukončí textové rozhraní programu
- CLS – vymaže obsah příkazového řádku
- NEW – otevře nový program
- DEL _číslo řádku_ – smaže řádek
- OPEN _název souboru_ – otevře soubor ze složky "Programy BASIC"
- SAVE – uloží změny do otevřeného souboru
- SAVE _název souboru_ – uloží zdrojový kód do konkrétního souboru ze složky "Programy BASIC"
## Ukázky programů v jazyce BASIC
Ve složce "Programy BASIC" se nachází ukázky kódu, které můžete spustit pomocí tohoto interpretu. Slouží k demonstraci škály využití mého interpretu. Zároveň je můžete využít pro inspiraci k vlastním projektům. Předtím bych však doporučil si důkladněji nastudovat syntaxi této verze jazyka BASIC, kterou jsem podrobně popsal ve své seminární práci.
### Binary search
Binary search je algoritmus pro vyhledávání čísel v seřazeném seznamu. Pro předvedení je seznam ve zdrojovém kódu již definovaný. Po spuštění kódu vás program požádá o uživatelský vstup. Pokud zadáte číslo, které se v seznamu nachází, program vrátí pozici onoho čísla v seznamu. Nutno dodat, že indexy prvků v seznamu se číslují od nuly. Pokud zadáte číslo, které v seznamu není program vás o tom informuje, podobně jako při zadání neplatného vstupu.
### Výpočet faktoriálu
Tento program vrátí faktoriál zadaného čísla neboli součin těch přirozených čísel, která jsou menší nebo rovna zadanému číslu.
### Fibonacciho posloupnost
Program vypíše prvních 50 Fibonacciho čísel. Posloupnost začíná čísly 0 a 1, hodnoty dalších členů jsou vždy rovny součtu dvou předchozích.
### Prvočísla
Tento program vypíše prvních 10000 prvočísel, tedy přirozených čísel, která jsou beze zbytku dělitelná číslem 1 a sebou samými (kromě samotnho čísla 1). Algoritmus funguje na principu Eratosthenova síta.
