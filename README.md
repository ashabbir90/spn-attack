# spn-attack

Projektmitglieder: Ayesha Shabbir und Leonard König

**Inhaltsverzeichnis**

[ToC]

## Verwendung

Dieses Projekt enthält vier Skripte, welche alle separat ausgeführt werden können, solange sie sich im gleichen Ordner befinden. Für die Ausführung der Skripte muss eine `python`-Umgebung installiert sein, welche die Packete `numpy`, `colorama`, `time` und `random` enthält.

Zum Testen der Linearen Angriffe muss die Datei [`Linear_Attack.py`](Linear_Attack.py) ausgeführt werden. Durch editieren der Variable `Attack` können einzele Angriffe ausgewählt werden. Bsp.:
- `Attacks = [1]`: Nur der von [Stinson (2018)](#quelle) beschriebene Beispielangriff wird ausgeführt.
- `Attacks = [1,2,3,4]`: Alle implementierten Angriff werden der Reihe nach ausgeführt (Achtung: Die Angriffe 3-4 können längere Laufzeiten haben [ca. 2-3 min je Angriff])

Zum Testen des Differenziellen Angriffs muss die Datei [`Differential_Attack.py`](Differential_Attack.py) ausgeführt werden.

## Skripte

- [`Basic_SPN.py`](Basic_SPN.py)
  - Implementierung grundlegender Funktionen des Substitutions-Permutations-Netzwerks (Schlüsselgenerierung, S-Box, Bit-Permutation und Verschlüsselung)
- [`Linear_Attack.py`](Linear_Attack.py)
  - Implementierung 4 linearer Angriffe (inklusive des Angriffs aus [Stinson (2018)](#quelle))
  - Berechnung von $`N_L(a,b)`$ sowie der linearen Approximationstabelle
  - Invertierung der S-Box
- [`Differential_Attack.py`](Differential_Attack.py)
  - Implemenierung des diffenenziellen Angriffs aus [Stinson (2018)](#quelle)
  - Berechnung der Menge $`\Delta(x')`$ bestehend aus den geordneten Paaren $`(x,x^*)`$ wobei $`x'=x\oplus x^*`$
  - Berechnung von $`N_D(a',b')`$ sowie der Differenz-Verteilungstabelle
  - Berechnung von $`R_p(a',b')`$ (nur für 4-Bit Zahlen)
- [`Console_Outputs.py`](Console_Outputs.py)
  - Funktionen zur Formatierung der Ausgaben in der Konsole

## Bilder
### Graphische Darstellungen der implementierten Angriffe

![](images/networks/linear_attack_1_overview.png)
![](images/networks/linear_attack_2_overview.png)
![](images/networks/linear_attack_3_overview.png)
![](images/networks/linear_attack_4_overview.png)
![](images/networks/differential_attack_overview.png)

### Berechnung des Bias $`\epsilon`$ für die Linearen Angriffe

- `linear_attack_1`
  
  ![linear_attack_1_math.png](images/math/linear_attack_1_math.png)

- `linear_attack_2`
  
  ![linear_attack_2_math.png](images/math/linear_attack_2_math.png)

- `linear_attack_3`
  
  ![linear_attack_3_math.png](images/math/linear_attack_3_math.png)

- `linear_attack_4`
  
  ![linear_attack_4_math.png](images/math/linear_attack_4_math.png)

## Quelle

Stinson, D.R.; Paterson, M.B.: Cryptography - Theory and Practice, CRC Press 2018
