# Grundsätzliche Konzepte:
Jedes Bild benötigt eine zusätzliche Datei, die Informationen zu dem Bild enthält. Das sind zum Beispiel Format, Größe und Name des Bildes.
Die Datei MUSS genauso heißen, wie die Bilddatei, aber statt auf __.png__ oder __.jpg__ zu enden, muss sie auf __.ini__ enden. 
Beispiel:
![image](docs/Pasted image 20240515144008.png)
Die Datei hat folgenden Inhalt:
```ini
[Metadata]
Title=2023-1
Year=2023
Material=Acryl, Kohle und Tusche auf Papier
Format=50 x 70 cm
Status=Verkauft
```
Alles hinter dem `=` Zeichen sind Informationen, die du verändern kannst, alles davor muss so bleiben, wie es ist.

Am besten kopierst du einfach eine der bereits vorhandenen __.ini__ Dateien und benennst sie um. Umbenennen kannst du mit Rechtsklick auf die Datei und dann auf __Umbenennen__ klicken ![image](docs/Pasted image 20240515144341.png)
Die Datei muss genauso heißen, wie die Bilddatei, das ist wichtig.

So, nun zum Ablauf, wenn du ein neues Bild hochladen möchtest:
# Neues Bild hochladen
1. Sourcetree starten. Hat folgendes Logo: ![image](docs/Pasted image 20240515140701.png)
2. Es erscheint dieses Fenster. Nicht überwältigt sein, du musst da nur ein bisschen rumklicken :D:![image](docs/Pasted image 20240515142915.png)
3. Einmal oben links auf Pull ![image](docs/Pasted image 20240515142943.png) klicken um eventuelle Änderungen von der Webseite auf dein PC zu kopieren.
4. Nochmal auf Pull klicken im neuen Dialog: ![image](docs/Pasted image 20240515143041.png)
5. Auf ![image](docs/Pasted image 20240515143117.png) oben rechts in der Leiste klicken. Dann öffnet sich ein Ordner, wo die Webseite drin ist: ![image](docs/Pasted image 20240515143245.png)
6. In den Ordner `static/images/kunstwerke` navigieren: ![image](docs/Pasted image 20240515143352.png)
7. Jetzt kannst du die neuen Bilder in die jeweiligen Ordner kopieren. Zum Beispiel ein neues Bild __DSC1000.jpg__ dass du 2024 gemalt hast (Du kannst für jedes neue Jahr auch neue Ordner erstellen, die als namen das Jahr haben):
	1. Öffne den Ordner 2024
	2. Kopiere das Bild in den Ordner
	3. Kopiere eine der vorhandenen __.ini__ Dateien in den Ordner und benenne sie wie das Bild. Heißt das Bild __DSC1000.jpg__ muss die __.ini__ Datei __DSC1000.ini__ heißen
	4. Bearbeite die __.ini__ Datei und passe die Informationen für Format, Titel und so weiter an.
9. Nun musst du die Änderungen wieder von deinem PC auf die Webseite hochladen
10. Öffne wieder Sourcetree und klicke auf ![image](docs/Pasted image 20240515144958.png)  ![image](docs/Pasted image 20240515144943.png)
11. Klicke im neuen Fenster auf ![image](docs/Pasted image 20240515145052.png) ![image](docs/Pasted image 20240515145121.png)
12. Schreib in das unterste Feld, was du gemacht hast, z.B.: "Neues Bild in 2024 hinzugefügt" ![image](docs/Pasted image 20240515145422.png)
13. Klicke auf ![image](docs/Pasted image 20240515145147.png) ![image](docs/Pasted image 20240515145248.png)
14. Klicke auf ![image](docs/Pasted image 20240515145454.png) ![image](docs/Pasted image 20240515145524.png)
15. Klicke auf ![image](docs/Pasted image 20240515145548.png) ![image](docs/Pasted image 20240515145615.png)
# Fertig 
Kannst alles schließen, es dauert ein paar Minuten, bis die Änderungen sichtbar sind, da die Webseite neu gebaut wird. Maximal 10 Minuten.