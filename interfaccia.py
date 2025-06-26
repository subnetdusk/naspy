# interfaccia.py

import streamlit as st
from datetime import date

def mostra_campi_input():
    """
    Mostra i widget per l'inserimento dei dati (4 RAL annuali) e restituisce i valori.

    Returns:
        dict: Un dizionario con i valori inseriti dall'utente.
    """
    st.subheader("1. Inserisci i dati per il calcolo")
    
    st.write("Inserisci la **Retribuzione Annua Lorda (RAL)** per ciascuno degli ultimi quattro anni. Se un anno non è stato lavorato, lascia il valore a 0.")
    
    anno_corrente = date.today().year
    
    # Creiamo i 4 box di input per le RAL
    ral_1 = st.number_input(f"RAL anno {anno_corrente - 1}", min_value=0.0, value=20000.0, step=100.0)
    ral_2 = st.number_input(f"RAL anno {anno_corrente - 2}", min_value=0.0, value=0.0, step=100.0)
    ral_3 = st.number_input(f"RAL anno {anno_corrente - 3}", min_value=0.0, value=0.0, step=100.0)
    ral_4 = st.number_input(f"RAL anno {anno_corrente - 4}", min_value=0.0, value=0.0, step=100.0)
    
    lista_ral = [ral_1, ral_2, ral_3, ral_4]
    
    st.markdown("---")

    settimane_contributive = st.slider(
        label="Totale Settimane di Contribuzione negli Ultimi 4 Anni",
        min_value=0,
        max_value=208,  # 4 anni * 52 settimane
        value=38, # Valore tipico per un contratto 1 Sett - 30 Giu
        step=1,
        help="Numero totale di settimane con contributi versati negli ultimi 48 mesi (minimo 13)."
    )
    
    over_55 = st.checkbox(
        label="Hai più di 55 anni?",
        value=False,
        help="Seleziona se hai compiuto 55 anni. Cambia l'inizio della riduzione mensile (décalage)."
    )

    return {
        "lista_ral": lista_ral,
        "settimane": settimane_contributive,
        "over_55": over_55
    }
