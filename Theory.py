NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Base de Dados de Acordes e Escalas (Intervalos e Nomes)
CHORD_DATA = {
    "maior": {0: "Tônica", 4: "3ª Maior", 7: "5ª Justa"},
    "menor": {0: "Tônica", 3: "3ª Menor", 7: "5ª Justa"},
    "7":     {0: "Tônica", 4: "3ª Maior", 7: "5ª Justa", 10: "7ª Menor"},
    "maj7":  {0: "Tônica", 4: "3ª Maior", 7: "5ª Justa", 11: "7ª Maior"},
    "m7":    {0: "Tônica", 3: "3ª Menor", 7: "5ª Justa", 10: "7ª Menor"},
    "m7b5":  {0: "Tônica", 3: "3ª Menor", 6: "5ª Diminuta", 10: "7ª Menor"},
    "dim":   {0: "Tônica", 3: "3ª Menor", 6: "5ª Diminuta", 9: "7ª Diminuta"},
    "9":     {0: "T", 4: "3M", 7: "5J", 10: "7m", 14: "9ª"},
    "maj9":  {0: "T", 4: "3M", 7: "5J", 11: "7M", 14: "9ª"},
    "m9":    {0: "T", 3: "3m", 7: "5J", 10: "7m", 14: "9ª"}
}

# Estrutura do Campo Harmônico Maior (Graus e tipos de acordes)
HARMONIC_FIELD_TYPES = ["maj7", "m7", "m7", "maj7", "7", "m7", "m7b5"]
MAJOR_SCALE_STEPS = [0, 2, 4, 5, 7, 9, 11] # Intervalos da escala maior

def get_harmonic_field(root):
    """Retorna os graus do campo harmônico maior para a tonalidade."""
    root = root.upper().replace("DB", "C#").replace("EB", "D#").replace("GB", "F#").replace("AB", "G#").replace("BB", "A#")
    if root not in NOTES: return None
    
    root_idx = NOTES.index(root)
    field = []
    for i, step in enumerate(MAJOR_SCALE_STEPS):
        note = NOTES[(root_idx + step) % 12]
        chord_type = HARMONIC_FIELD_TYPES[i]
        field.append(f"{i+1}º Grau: {note} {chord_type}")
    return field

def get_chord_details(root, chord_type):
    """Retorna o detalhamento teórico das notas de um acorde (nome real e intervalo)."""
    root = root.upper().replace("DB", "C#").replace("EB", "D#").replace("GB", "F#").replace("AB", "G#").replace("BB", "A#")
    if root not in NOTES: return None
    root_idx = NOTES.index(root)
    intervals = CHORD_DATA.get(chord_type.lower())
    if not intervals: return None
    return {NOTES[(root_idx + s) % 12]: label for s, label in intervals.items()}

def get_chord_notes(root, chord_type):
    """Retorna a lista de notas reais de um acorde."""
    root = root.upper().replace("DB", "C#").replace("EB", "D#").replace("GB", "F#").replace("AB", "G#").replace("BB", "A#")
    if root not in NOTES: return []
    
    root_idx = NOTES.index(root)
    intervals = CHORD_DATA.get(chord_type.lower())
    if not intervals: return []
    
    # intervals agora é um dicionário, ex: {0: "T", 4: "3M", ...}
    return [NOTES[(root_idx + s) % 12] for s in intervals.keys()]
