# calcolo.py

import math

# --- Costanti Normative (Valori 2024, da aggiornare per il 2025 appena disponibili) ---
IMPORTO_RIFERIMENTO_MENSILE = 1425.21
MASSIMALE_MENSILE = 1550.42
COEFFICIENTE_SETTIMANALE = 4.33

def calcola_retribuzione_riferimento(lista_ral: list, settimane_contributive: int):
    """
    Calcola la retribuzione mensile di riferimento partendo dalle RAL e dalle settimane.
    Formula: (Totale Retribuzioni 4 anni / Totale Settimane Contributive) * 4,33
    """
    if settimane_contributive == 0:
        return 0.0
        
    totale_retribuzioni = sum(lista_ral)
    retribuzione_settimanale_media = totale_retribuzioni / settimane_contributive
    retribuzione_mensile_riferimento = retribuzione_settimanale_media * COEFFICIENTE_SETTIMANALE
    return retribuzione_mensile_riferimento

def calcola_naspi(lista_ral: list, settimane_contributive: int):
    """
    Calcola l'importo mensile lordo e la durata della NASpI.

    Args:
        lista_ral (list): Lista delle 4 retribuzioni annue lorde.
        settimane_contributive (int): Il numero di settimane di contribuzione negli ultimi 4 anni.

    Returns:
        dict: Un dizionario contenente tutti i risultati del calcolo.
    """
    
    if settimane_contributive < 13:
        return {
            "requisiti_soddisfatti": False,
            "messaggio_errore": "Requisito non soddisfatto: sono necessarie almeno 13 settimane di contribuzione negli ultimi 4 anni."
        }

    # 1. Calcola la retribuzione mensile di riferimento
    retribuzione_riferimento = calcola_retribuzione_riferimento(lista_ral, settimane_contributive)

    # 2. Calcolo dell'importo mensile dell'indennità
    importo_mensile = 0.0
    if retribuzione_riferimento <= IMPORTO_RIFERIMENTO_MENSILE:
        importo_mensile = retribuzione_riferimento * 0.75
    else:
        importo_mensile = (IMPORTO_RIFERIMENTO_MENSILE * 0.75) + \
                          ((retribuzione_riferimento - IMPORTO_RIFERIMENTO_MENSILE) * 0.25)
    
    # 3. Applicazione del massimale
    importo_mensile_lordo = min(importo_mensile, MASSIMALE_MENSILE)

    # 4. Calcolo della durata
    durata_settimane = math.floor(settimane_contributive / 2)
    durata_settimane = min(durata_settimane, 104) # Max 24 mesi
    durata_mesi = round(durata_settimane / COEFFICIENTE_SETTIMANALE, 1)

    return {
        "retribuzione_riferimento_calcolata": round(retribuzione_riferimento, 2),
        "importo_mensile_lordo": round(importo_mensile_lordo, 2),
        "durata_mesi": durata_mesi,
        "durata_settimane": durata_settimane,
        "requisiti_soddisfatti": True,
        "messaggio_errore": None
    }

def calcola_piano_decalage(importo_iniziale: float, durata_mesi: float, over_55: bool):
    """
    Calcola il piano di ammortamento mensile con la riduzione (décalage).
    (Questa funzione rimane invariata)
    """
    piano = []
    importo_corrente = importo_iniziale
    mese_inizio_decalage = 8 if over_55 else 6
    
    for mese in range(1, int(durata_mesi) + 1):
        if mese >= mese_inizio_decalage:
            importo_corrente *= 0.97
        piano.append(round(importo_corrente, 2))
        
    return piano
