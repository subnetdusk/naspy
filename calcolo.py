# calcolo.py

import math

IMPORTO_RIFERIMENTO_MENSILE = 1425.21
MASSIMALE_MENSILE = 1550.42
COEFFICIENTE_SETTIMANALE = 4.33

def calcola_naspi(lista_ral, settimane_contributive):
    if settimane_contributive < 13:
        return {
            "requisiti_soddisfatti": False,
            "messaggio_errore": "Requisito non soddisfatto: sono necessarie almeno 13 settimane di contribuzione.",
        }

    retribuzione_riferimento = calcola_retribuzione_riferimento(lista_ral, settimane_contributive)

    importo_mensile = 0.0
    if retribuzione_riferimento <= IMPORTO_RIFERIMENTO_MENSILE:
        importo_mensile = retribuzione_riferimento * 0.75
    else:
        importo_mensile = (IMPORTO_RIFERIMENTO_MENSILE * 0.75) + ((retribuzione_riferimento - IMPORTO_RIFERIMENTO_MENSILE) * 0.25)
    
    importo_mensile_lordo = min(importo_mensile, MASSIMALE_MENSILE)

    durata_settimane = math.floor(settimane_contributive / 2)
    durata_settimane = min(durata_settimane, 104)
    
    durata_mesi_decimale = durata_settimane / COEFFICIENTE_SETTIMANALE

    return {
        "retribuzione_riferimento_calcolata": round(retribuzione_riferimento, 2),
        "importo_mensile_lordo": round(importo_mensile_lordo, 2),
        "durata_settimane": durata_settimane,
        "durata_mesi_decimale": durata_mesi_decimale,
        "requisiti_soddisfatti": True,
        "messaggio_errore": None,
    }

def calcola_retribuzione_riferimento(lista_ral, settimane_contributive):
    if settimane_contributive == 0:
        return 0.0
    
    totale_retribuzioni = sum(lista_ral)
    retribuzione_settimanale_media = totale_retribuzioni / settimane_contributive
    return retribuzione_settimanale_media * COEFFICIENTE_SETTIMANALE

def calcola_piano_decalage(importo_mensile_iniziale, durata_mesi_decimale, over_55):
    piano = []
    if durata_mesi_decimale <= 0:
        return piano

    numero_rate = math.ceil(durata_mesi_decimale)
    durata_residua = durata_mesi_decimale
    mese_inizio_decalage = 8 if over_55 else 6

    for mese_corrente in range(1, numero_rate + 1):
        
        importo_base_mese = importo_mensile_iniziale
        if mese_corrente >= mese_inizio_decalage:
            num_mesi_con_riduzione = mese_corrente - mese_inizio_decalage + 1
            fattore_riduzione = 0.97 ** num_mesi_con_riduzione
            importo_base_mese = importo_mensile_iniziale * fattore_riduzione

        rata_corrente = 0.0
        if durata_residua >= 1.0:
            rata_corrente = importo_base_mese
            durata_residua -= 1.0
        elif durata_residua > 0:
            rata_corrente = importo_base_mese * durata_residua
            durata_residua = 0
        
        piano.append(round(rata_corrente, 2))
            
    return piano
