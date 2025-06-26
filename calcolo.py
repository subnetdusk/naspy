# calcolo.py

import math

# --- Costanti Normative (Valori 2024, da aggiornare per il 2025 appena disponibili) ---
IMPORTO_RIFERIMENTO_MENSILE = 1425.21
MASSIMALE_MENSILE = 1550.42
COEFFICIENTE_SETTIMANALE = 4.33

def calcola_naspi(lista_ral: list, settimane_contributive: int):
    """
    Calcola l'importo mensile lordo e la durata decimale in mesi della NASpI.
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
    # Calcoliamo e restituiamo la durata precisa in mesi decimali
    durata_mesi_decimale = durata_settimane / COEFFICIENTE_SETTIMANALE

    return {
        "retribuzione_riferimento_calcolata": round(retribuzione_riferimento, 2),
        "importo_mensile_lordo": round(importo_mensile_lordo, 2),
        "durata_settimane": durata_settimane,
        "durata_mesi_decimale": durata_mesi_decimale, # Nuovo, per il calcolo preciso del piano
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

def calcola_piano_decalage(importo_mensile_iniziale: float, durata_mesi_decimale: float, over_55: bool):
    """
    --- FUNZIONE RISCRITTA SECONDO LA NUOVA LOGICA ---
    Calcola il piano di ammortamento usando i mesi decimali.
    """
    piano = []
    # Arrotondiamo il numero di rate al numero intero superiore
    numero_rate_totali = math.ceil(durata_mesi_decimale)
    durata_residua_mesi = durata_mesi_decimale
    importo_mensile_base = importo_mensile_iniziale
    mese_inizio_decalage = 8 if over_55 else 6

    for mese_corrente in range(1, numero_rate_totali + 1):
        # Applica il décalage se necessario
        importo_mensile_con_decalage = importo_mensile_base
        if mese_corrente >= mese_inizio_decalage:
            # La formula corretta del décalage progressivo
            fattore_riduzione = 0.97 ** (mese_corrente - mese_inizio_decalage + 1)
            importo_mensile_con_decalage *= fattore_riduzione

        # Calcola la rata per il mese corrente
        if durata_residua_mesi >= 1:
            importo_rata_corrente = importo_mensile_con_decalage
            durata_residua_mesi -= 1
        else:
            # Ultima rata parziale
            importo_rata_corrente = import
