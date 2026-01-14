# 4-Takt-Motor State Diagram

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Ansaugen

    Ansaugen: 1. Takt - Einlass
    Ansaugen: Kolben OT → UT
    Ansaugen: Einlassventil offen
    Ansaugen: Auslassventil geschlossen
    Ansaugen: Gemisch wird angesaugt

    Verdichten: 2. Takt - Kompression
    Verdichten: Kolben UT → OT
    Verdichten: Einlassventil geschlossen
    Verdichten: Auslassventil geschlossen
    Verdichten: Gemisch wird komprimiert

    Arbeiten: 3. Takt - Verbrennung
    Arbeiten: Kolben OT → UT
    Arbeiten: Einlassventil geschlossen
    Arbeiten: Auslassventil geschlossen
    Arbeiten: Zündkerze zündet
    Arbeiten: Energie wird erzeugt

    Ausstossen: 4. Takt - Auslass
    Ausstossen: Kolben UT → OT
    Ausstossen: Einlassventil geschlossen
    Ausstossen: Auslassventil offen
    Ausstossen: Abgase werden ausgestoßen

    Ansaugen --> Verdichten: Kolben erreicht UT
    Verdichten --> Arbeiten: Zündung bei OT
    Arbeiten --> Ausstossen: Kolben erreicht UT
    Ausstossen --> Ansaugen: Zyklus wiederholt
```

## Gefundene Fehler:

1. **Fehlende Mermaid-Code-Block-Wrapper**: Der Code muss in ` ```mermaid ` eingeschlossen sein
2. **Syntax-Problem**: Mehrfache Beschreibungen mit `:` für denselben State-Namen funktionieren nicht direkt in Mermaid
3. **Lösung**: Verwendung von verschachtelten States mit internen Beschreibungen

Das Diagramm zeigt nun die 4 Takte eines Verbrennungsmotors im zyklischen Ablauf.
