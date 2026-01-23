# Bilder per E-Mail verwalten

Du kannst Bilder jetzt ganz einfach per E-Mail hinzufügen, bearbeiten oder löschen.

## Grundsätzliche Konzepte

Jedes Bild benötigt zwei Dateien:
1. **Die Bilddatei** (z.B. `2025-1.jpg`)
2. **Die Informationsdatei** (z.B. `2025-1.ini`)

Beide Dateien MÜSSEN exakt den gleichen Namen haben, nur die Endung ist unterschiedlich.

### Dateinamen-Format

**WICHTIG:** Alle Dateien müssen nach diesem Schema benannt sein:
```
JAHR-NAME.ENDUNG
```

**Richtige Beispiele:**
- `2025-1.jpg` und `2025-1.ini`
- `2024-blumenwiese.jpg` und `2024-blumenwiese.ini`
- `2023-12.png` und `2023-12.ini`

**Falsche Beispiele:**
- ❌ `bild1.jpg` (fehlt Jahr)
- ❌ `25-1.jpg` (Jahr nicht 4-stellig)
- ❌ `2025_1.jpg` (Unterstrich statt Bindestrich)
- ❌ `2025-1.docx` (falscher Dateityp)

### Die .ini Datei

Die `.ini` Datei enthält Informationen zum Bild:
```ini
[Metadata]
Title=2023-1
Year=2023
Material=Acryl, Kohle und Tusche auf Papier
Format=50 x 70 cm
Status=Verkauft
```

Alles **nach** dem `=` Zeichen kannst du ändern.  
Alles **vor** dem `=` Zeichen MUSS so bleiben.

---

## Neues Bild hochladen oder Bild bearbeiten

### Schritt 1: E-Mail vorbereiten

1. Erstelle eine neue E-Mail an: **bilder@example.net**
2. Lass den Betreff leer (oder schreib irgendetwas rein, außer "DELETE")

### Schritt 2: Authentifizierung

**In der ersten Zeile** der E-Mail schreibst du:
```
AUTH: DeinPasswort
```

Ersetze `DeinPasswort` durch das Passwort, das du von mir bekommen hast.

**WICHTIG:**
- Nach `AUTH:` muss ein Leerzeichen kommen
- Das Passwort muss exakt stimmen (Groß-/Kleinschreibung beachten)
- Das muss in der **ersten Zeile** stehen

### Schritt 3: Dateien benennen

Bevor du Dateien anhängst, müssen sie richtig benannt sein:

**Windows:**
1. Öffne den Ordner mit deinen Bildern
2. Rechtsklick auf die Datei → **Umbenennen**
3. Gib den neuen Namen ein (z.B. `2025-1.jpg`)
4. Drücke Enter
5. Wiederhole das für die `.ini` Datei

**Mac:**
1. Öffne den Ordner mit deinen Bildern
2. Klicke einmal auf die Datei
3. Drücke Enter
4. Gib den neuen Namen ein (z.B. `2025-1.jpg`)
5. Drücke Enter
6. Wiederhole das für die `.ini` Datei

### Schritt 4: Dateien anhängen

1. Klicke auf das **Büroklammer-Symbol** (Anhang hinzufügen)
2. Wähle **beide** Dateien aus:
   - Das Bild (z.B. `2025-1.jpg`)
   - Die `.ini` Datei (z.B. `2025-1.ini`)

### Schritt 5: E-Mail senden

Sende die E-Mail ab.

### Beispiel einer fertigen E-Mail:
```
An: bilder@example.net
Betreff: (leer oder beliebig)

E-Mail-Text:
AUTH: MeinGeheimesPasswort123

Anhänge:
📎 2025-1.jpg
📎 2025-1.ini
```

### Fertig

Die Website wird **innerhalb einer Stunde** automatisch aktualisiert.

Du bekommst eine Bestätigungs-E-Mail mit den Ergebnissen.

---

## Bild löschen

### Schritt 1: E-Mail vorbereiten

1. Erstelle eine neue E-Mail an: **bilder@example.net**
2. Schreibe in den **Betreff**: `DELETE`

### Schritt 2: Authentifizierung und Dateinamen

In die E-Mail schreibst du:
```
AUTH: DeinPasswort
2025-5.jpg
2025-5.ini
```

**Erste Zeile:** Dein Authentifizierungs-Passwort  
**Weitere Zeilen:** Die Dateinamen, die gelöscht werden sollen (jeder Name in eine eigene Zeile)

### Schritt 3: E-Mail senden

Sende die E-Mail ab.

### Beispiel einer Lösch-E-Mail:
```
An: bilder@example.net
Betreff: DELETE

E-Mail-Text:
AUTH: MeinGeheimesPasswort123
2025-5.jpg
2025-5.ini
2024-12.jpg
2024-12.ini
```

### Fertig

Die Bilder werden gelöscht und die Website wird automatisch aktualisiert.

Du bekommst eine Bestätigungs-E-Mail mit den Ergebnissen.

---

## Häufige Fehler und Lösungen

### "Authentifizierung fehlgeschlagen"

**Lösung:**
- Überprüfe, ob die erste Zeile exakt so aussieht: `AUTH: DeinPasswort`
- Nach `AUTH:` muss ein Leerzeichen kommen
- Das Passwort muss exakt stimmen (achte auf Groß-/Kleinschreibung)

### "Keine Dateien gefunden"

**Lösung:**
- Hast du die Dateien wirklich angehängt? (Büroklammer-Symbol)
- Sind die Dateinamen richtig? (müssen mit 4-stelliger Jahreszahl beginnen)
- Hast du sowohl `.jpg` als auch `.ini` Datei angehängt?

### "Datei nicht gefunden" beim Löschen

**Lösung:**
- Überprüfe die Schreibweise (Tippfehler?)
- Schau auf der Website nach dem exakten Dateinamen
- Achte auf Groß-/Kleinschreibung

### "Datei abgelehnt"

**Lösung:**
- Dateiname muss mit 4-stelliger Jahreszahl beginnen (z.B. `2025`)
- Nach dem Jahr muss ein Bindestrich `-` kommen
- Erlaubte Endungen: `.jpg`, `.jpeg`, `.png`, `.ini`
- Benenne die Datei um und sende die E-Mail erneut

---

## Wichtige Hinweise

- **Geduld:** Die Website wird nicht sofort aktualisiert, sondern innerhalb einer Stunde
- **Bestätigung:** Du bekommst immer eine Bestätigungs-E-Mail zurück
- **Fehler:** Wenn etwas nicht funktioniert, bekommst du eine E-Mail mit detaillierten Anweisungen
- **Beide Dateien:** Vergiss nicht, sowohl das Bild als auch die `.ini` Datei zu handhaben

Bei Problemen: Ruf mich an oder schreib mir bei Signal.