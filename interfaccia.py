# interfaccia.py

import streamlit as st

def mostra_campi_input():
    """
    Mostra i widget per l'inserimento dei dati e restituisce i valori inseriti.

    Returns:
        dict: Un dizionario con i valori inseriti dall'utente.
    """
    st.subheader("1. Inserisci i dati per il calcolo")
    
    retribuzione_media = st.number_input(
        label="Retribuzione Media Mensile Imponibile (€)",
        min_value=0.0,
        max_value=10000.0,
        value=1500.0,
        step=50.0,
        help="Inserisci la retribuzione lorda media mensile degli ultimi 4 anni."
    )
    
    settimane_contributive = st.slider(
        label="Settimane di Contribuzione negli Ultimi 4 Anni",
        min_value=0,
        max_value=208,  # 4 anni * 52 settimane
        value=52,
        step=1,
        help="Numero totale di settimane con contributi versati negli ultimi 48 mesi (minimo 13)."
    )
    
    over_55 = st.checkbox(
        label="Hai più di 55 anni?",
        value=False,
        help="Seleziona se hai compiuto 55 anni. Cambia l'inizio della riduzione mensile (décalage)."
    )

    return {
        "retribuzione": retribuzione_media,
        "settimane": settimane_contributive,
        "over_55": over_55
    }
