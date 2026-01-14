# Otto-Zyklus SysML v2 Modell - Dokumentation

## Übersicht

Diese SysML v2 Modelldatei beschreibt einen **Ottomotor** (Viertakt-Benzinmotor) mit allen wesentlichen mechanischen Komponenten und seinem Verhaltensmodell. Das Modell kombiniert strukturelle Definitionen mit einem detaillierten Zustandsmodell des Otto-Zyklus.

## Hauptkomponenten

### 1. Enumerationen

Das Modell definiert drei wichtige Enumerationstypen:

- **Kraftstoffart**: Verschiedene Benzinarten (Benzin, SuperBenzin, E10, E85)
- **Ventilzustand**: Zustand eines Ventils (offen, geschlossen)
- **KolbenPosition**: Totpunkte des Kolbens (OT = Oberer Totpunkt, UT = Unterer Totpunkt)

### 2. Signal-Definitionen

Signale für Zustandsübergänge im Otto-Zyklus:
- `KolbenErreichtUT`: Signal wenn Kolben unteren Totpunkt erreicht
- `KolbenErreichtOT`: Signal wenn Kolben oberen Totpunkt erreicht
- `ZuendungSignal`: Signal für Zündungsauslösung
- `ZyklusWiederholen`: Signal für Zykluswiederholung

### 3. Action-Definitionen

Das Modell definiert verschiedene Aktionen für Motoraktivitäten:

- **Ventilsteuerung**: `EinlassventilOeffnen`, `EinlassventilSchliessen`, `AuslassventilOeffnen`, `AuslassventilSchliessen`
- **Gemischverarbeitung**: `GemischAnsaugen`, `GemischVerdichten`, `GemischZuenden`
- **Energieerzeugung**: `EnergieErzeugen` (erzeugt Kolbenkraft und Drehmoment)
- **Abgasverarbeitung**: `AbgaseAusstossen`
- **Kolbenbewegung**: `KolbenBewegen` (zwischen Totpunkten)

## Der Otto-Zyklus (Viertakt-Zyklus)

Das Herzstück des Modells ist die Zustandsdefinition `OttoZyklus`, die den klassischen Viertakt-Prozess beschreibt:

### 1. Takt: Ansaugen (Intake Stroke)
- **Kolbenbewegung**: OT → UT (nach unten)
- **Ventilstellung**: Einlassventil offen, Auslassventil geschlossen
- **Prozess**: Frisches Kraftstoff-Luft-Gemisch wird angesaugt
- **Entry-Aktion**: Einlassventil öffnen, Auslassventil schließen
- **Do-Aktion**: Kolben bewegen, Gemisch ansaugen
- **Exit-Aktion**: Einlassventil schließen
- **Übergang**: Bei Erreichen von UT → Verdichten

### 2. Takt: Verdichten (Compression Stroke)
- **Kolbenbewegung**: UT → OT (nach oben)
- **Ventilstellung**: Beide Ventile geschlossen
- **Prozess**: Gemisch wird auf ca. 1/10 seines Volumens komprimiert
- **Do-Aktion**: Kolben bewegen, Gemisch verdichten
- **Übergang**: Bei Zündungssignal → Arbeiten

### 3. Takt: Arbeiten (Power Stroke)
- **Kolbenbewegung**: OT → UT (nach unten)
- **Ventilstellung**: Beide Ventile geschlossen
- **Prozess**: Zündung und Verbrennung erzeugen Energie
- **Entry-Aktion**: Gemisch zünden
- **Do-Aktion**: Energie erzeugen, Kolben bewegen
- **Übergang**: Bei Erreichen von UT → Ausstoßen

### 4. Takt: Ausstoßen (Exhaust Stroke)
- **Kolbenbewegung**: UT → OT (nach oben)
- **Ventilstellung**: Auslassventil offen, Einlassventil geschlossen
- **Prozess**: Verbrennungsgase werden ausgestoßen
- **Entry-Aktion**: Auslassventil öffnen
- **Do-Aktion**: Kolben bewegen, Abgase ausstoßen
- **Exit-Aktion**: Auslassventil schließen
- **Übergang**: Bei Zykluswiederholung → Ansaugen (Zyklus beginnt von vorne)

### Kompakte Version

Das Modell enthält auch eine vereinfachte Darstellung `OttoZyklusKompakt` mit Shorthand-Notation für schnellere Übersichten.

## Mechanische Komponenten

### Zylinder
- Enthält: Kolben, Ventile (1-2 Einlass, 1-2 Auslass), Zündkerze
- Attribute: Masse, Bohrung, Hub, Hubraum, Verdichtungsverhältnis (8:1 bis 14:1)
- Verhaltensmodell: Exhibiert den `OttoZyklus`

### Kolben
- Bewegt sich im Zylinder auf und ab
- Attribute: Masse, Durchmesser, Höhe, Position, Kolbenbolzendurchmesser
- Referenz: Verbunden mit Pleuelstange

### Pleuelstange
- Verbindet Kolben mit Kurbelwelle
- Wandelt lineare Bewegung in Rotation um
- Attribute: Masse, Länge, Durchmesser der Lager (kleines/großes Auge)

### Kurbelwelle
- Wandelt oszillierende Kolbenbewegung in Drehbewegung
- Attribute: Masse, Länge, Hubradius, Drehzahl, Drehmoment, verschiedene Durchmesser

### Ventile (Einlass & Auslass)
- Steuern Gas-Ein- und Auslass
- Attribute: Masse, Teller-/Schaftdurchmesser, Hub, Zustand

### Zündkerze
- Erzeugt Funken zur Gemischentzündung
- Attribute: Masse, Gewinde, Elektrodenabstand, Wärmewert

## Motor-Betriebszustände

Neben dem Otto-Zyklus definiert das Modell übergeordnete Betriebszustände:

1. **Aus**: Motor ist ausgeschaltet
2. **Anlassen**: Motor wird gestartet (mit Starter)
3. **Laufend**: Normalbetrieb (Otto-Zyklen laufen in allen Zylindern)
4. **Abstellen**: Motor wird abgestellt

Übergänge erfolgen über Signale wie `StarterSignal`, `MotorLaeuft`, `StopSignal` mit Guards (z.B. Kraftstoff vorhanden).

## Hauptdefinition: Ottomotor

Die zentrale `part def Ottomotor` vereint alle Komponenten:

- **Attribute**: Masse, Gesamthubraum, Nennleistung, max. Drehmoment, max. Drehzahl, Zylinderanzahl, Kraftstoffart
- **Komponenten**:
  - 4-12 Zylinder (typische Konfigurationen)
  - 1 Kurbelwelle
  - 4-12 Pleuelstangen (eine pro Zylinder)
- **Verhalten**: Exhibiert `MotorBetriebszustaende`

### Hierarchie der Zustandsmaschinen

Das Modell verwendet eine zweistufige Hierarchie:
1. **Motor-Ebene**: `MotorBetriebszustaende` (aus → anlassen → laufend → abstellen)
2. **Zylinder-Ebene**: `OttoZyklus` pro Zylinder (ansaugen → verdichten → arbeiten → ausstoßen)

## Beispielinstanz: 4-Zylinder Motor

Das Modell enthält eine konkrete Instanz `vierZylinderMotor` mit realistischen Werten:

- **Masse**: 120 kg
- **Hubraum**: 1.998 L
- **Leistung**: 110 kW
- **Drehmoment**: 200 Nm
- **Zylinderanzahl**: 4
- **Kraftstoff**: SuperBenzin
- **Zylinderkonfiguration**:
  - Bohrung: 86 mm
  - Hub: 86 mm (Quadratmotor)
  - Verdichtungsverhältnis: 10.5:1
  - 2 Einlass- und 2 Auslassventile pro Zylinder
- **Kolben**: 0.35 kg pro Stück
- **Kurbelwelle**: 18 kg, Hubradius 43 mm
- **Pleuelstangen**: 0.55 kg, Länge 144 mm

## Verwendete SysML v2 Konzepte

Das Modell demonstriert fortgeschrittene SysML v2 Features:

1. **State Definitions**: Detaillierte Zustandsmaschinen mit Entry/Do/Exit-Aktionen
2. **Transitions**: Explizite Übergänge mit Accept-Events und Guards
3. **Part Definitions**: Strukturelle Komponentendefinitionen
4. **Action Definitions**: Verhaltensbausteine
5. **Attribute Typing**: ISQ/SI-Einheiten für physikalische Größen
6. **Exhibit States**: Zuordnung von Verhaltensmodellen zu Komponenten
7. **Redefinition**: Spezialisierung von Definitionen in Instanzen
8. **Enumerations**: Typsichere Aufzählungen
9. **Item Definitions**: Signal-/Event-Definitionen

## Physikalische Größen

Das Modell verwendet standardisierte Einheiten aus ISQ (International System of Quantities) und SI:
- Länge (length): mm, m
- Volumen (volume): L
- Masse (mass): kg
- Kraft (force): N
- Drehmoment (torque): Nm
- Leistung (power): kW
- Druck (pressure)
- Drehzahl (rotationalFrequency)

## Dokumentationsstil

Jede Definition enthält `doc`-Kommentare in deutscher Sprache, die den Zweck und die Funktionsweise erklären. Das Modell ist lehrreich aufgebaut und eignet sich gut für Ausbildungszwecke im Bereich Motorentechnik und Systems Engineering.
