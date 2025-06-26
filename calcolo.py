# calcolo.py

import math

# --- Costanti Normative (Valori 2024, da aggiornare per il 2025 appena disponibili) ---
IMPORTO_RIFERIMENTO_MENSILE = 1425.21
MASSIMALE_MENSILE = 1550.42
COEFFICIENTE_SETTIMANALE = 4.33
GIORNI_PER_MESE_COMMERCIALE = 30

def calcola_naspi(lista_ral: list, settimane_contributive: int):
    """
    Calcola l'importo mensile lordo e la durata della NASpI.
    Restituisce anche la durata totale in giorni per il calcolo del décalage.
    """
    
    if settimane_contributive < 13:
        return {
            "requisiti_soddisfatti": False,
            "messaggio_errore": "Requisito non soddisfatto: sono necessarie almeno 13 settimane di contribuzione negli ultimi 4 anni."
        }

    retribuzione_riferimento = calcola_retribuzione_riferimento(lista_ral, settimane_contributive)

    importo_mensile = 0.0
    if retribuzione_riferimento <= IMPORTO_RIFERIMENTO_MENSILE:
        importo_mensile = retribuzione_riferimento * 0.75
    else:
        importo_mensile = (IMPORTO_RIFERIMENTO_MENSILE * 0.75) + \
                          ((retribuzione_riferimento - IMPORTO_RIFERIMENTO_MENSILE) * 0.25)
    
    importo_mensile_lordo = min(importo_mensile, MASSIMALE_MENSILE)

    durata_settimane = math.floor(settimane_contributive / 2)
    durata_settimane = min(durata_settimane, 104)
    
    # --- MODIFICA ---
    # Calcoliamo e restituiamo sia la durata in mesi (per stima) sia quella in giorni (per calcolo preciso)
    durata_mesi_stimata = round(durata_settimane / COEFFICIENTE_SETTIMANALE, 1)
    giorni_totali_diritto = durata_settimane * 7

    return {
        "retribuzione_riferimento_calcolata": round(retribuzione_riferimento, 2),
        "importo_mensile_lordo": round(importo_mensile_lordo, 2),
        "durata_mesi": durata_mesi_stimata, # Mantenuto per la metrica UI
        "durata_settimane": durata_settimane,
        "giorni_totali_diritto": giorni_totali_diritto, # Nuovo, per il calcolo preciso
        "requisiti_soddisfatti": True,
        "messaggio_errore": None
    }

def calcola_retribuzione_riferimento(lista_ral: list, settimane_contributive: int):
    """Calcola la retribuzione mensile di riferimento. (Invariata)"""
    if settimane_contributive == 0:
        return 0.0
    totale_retribuzioni = sum(lista_ral)
    retribuzione_settimanale_media = totale_retribuzioni / settimane_contributive
    return retribuzione_settimanale_media * COEFFICIENTE_SETTIMANALE

def calcola_piano_decalage(importo_mensile_iniziale: float, giorni_totali_diritto: int, over_55: bool):
    """
    --- FUNZIONE COMPLETAMENTE RISCRITTA ---
    Calcola il piano di ammortamento mensile su base giornaliera, gestendo la rata finale parziale.
    """
    piano = []
    giorni_rimanenti = giorni_totali_diritto
    importo_mensile_corrente = importo_mensile_iniziale
    mese_corrente = 1
    mese_inizio_decalage = 8 if over_55 else 6

    while giorni_rimanenti > 0:
        # Applica il décalage all'importo mensile di riferimento per il mese corrente
        if mese_corrente >= mese_inizio_decalage:
            importo_mensile_corrente = importo_mensile_iniziale * (0.97 ** (mese_corrente - mese_inizio_decalage + 1))

        # Calcola l'importo giornaliero per il mese corrente
        importo_giornaliero = importo_mensile_corrente / GIORNI_PER_MESE_COMMERCIALE
        
        # Determina quanti giorni pagare in questa rata
        giorni_da_pagare_in_questo_mese = min(GIORNI_PER_MESE_COMMERCIALE, giorni_rimanenti)
        
        # Calcola l'importo della rata
        importo_rata_corrente = importo_giornaliero * giorni_da_pagare_in_questo_mese
        
        piano.append(round(importo_rata_corrente, 2))
        
        # Aggiorna i contatori
        giorni_rimanenti -= giorni_da_pagare_in_questo_mese
        mese_corrente += 1
        
    return piano
