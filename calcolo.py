# calcolo.py

import math

# --- Costanti Normative (Valori 2024, da aggiornare per il 2025 appena disponibili) ---
# L'INPS aggiorna questi valori ogni anno. Usiamo quelli del 2024 come stima plausibile.
IMPORTO_RIFERIMENTO_MENSILE = 1425.21
MASSIMALE_MENSILE = 1550.42
COEFFICIENTE_SETTIMANALE = 4.33

def calcola_naspi(retribuzione_media_mensile: float, settimane_contributive: int):
    """
    Calcola l'importo mensile lordo e la durata della NASpI.

    Args:
        retribuzione_media_mensile (float): La retribuzione media lorda mensile imponibile.
        settimane_contributive (int): Il numero di settimane di contribuzione negli ultimi 4 anni.

    Returns:
        dict: Un dizionario contenente 'importo_mensile', 'durata_mesi', 'requisiti_soddisfatti' e 'messaggio_errore'.
    """
    
    # Requisito minimo: almeno 13 settimane di contribuzione
    if settimane_contributive < 13:
        return {
            "requisiti_soddisfatti": False,
            "messaggio_errore": "Requisito non soddisfatto: sono necessarie almeno 13 settimane di contribuzione negli ultimi 4 anni."
        }

    # Calcolo della retribuzione di riferimento
    retribuzione_riferimento = retribuzione_media_mensile

    # Calcolo dell'importo mensile dell'indennità
    importo_mensile = 0.0
    if retribuzione_riferimento <= IMPORTO_RIFERIMENTO_MENSILE:
        importo_mensile = retribuzione_riferimento * 0.75
    else:
        importo_mensile = (IMPORTO_RIFERIMENTO_MENSILE * 0.75) + \
                          ((retribuzione_riferimento - IMPORTO_RIFERIMENTO_MENSILE) * 0.25)
    
    # Applicazione del massimale
    importo_mensile_lordo = min(importo_mensile, MASSIMALE_MENSILE)

    # Calcolo della durata in settimane e mesi
    durata_settimane = math.floor(settimane_contributive / 2)
    
    # La durata massima è di 24 mesi (104 settimane)
    durata_settimane = min(durata_settimane, 104) 
    
    durata_mesi = round(durata_settimane / COEFFICIENTE_SETTIMANALE, 1)

    return {
        "importo_mensile_lordo": round(importo_mensile_lordo, 2),
        "durata_mesi": durata_mesi,
        "durata_settimane": durata_settimane,
        "requisiti_soddisfatti": True,
        "messaggio_errore": None
    }

def calcola_piano_decalage(importo_iniziale: float, durata_mesi: float, over_55: bool):
    """
    Calcola il piano di ammortamento mensile con la riduzione (décalage).

    Args:
        importo_iniziale (float): L'importo lordo mensile della NASpI.
        durata_mesi (float): La durata totale in mesi.
        over_55 (bool): Se il beneficiario ha più di 55 anni.

    Returns:
        list: Una lista di importi mensili lordi dopo l'applicazione del décalage.
    """
    piano = []
    importo_corrente = importo_iniziale
    
    # Il décalage inizia dal 6° mese (indice 5) o dall'8° (indice 7) per gli over 55
    mese_inizio_decalage = 8 if over_55 else 6
    
    for mese in range(1, int(durata_mesi) + 1):
        if mese >= mese_inizio_decalage:
            importo_corrente *= 0.97  # Riduzione del 3%
        piano.append(round(importo_corrente, 2))
        
    return piano
