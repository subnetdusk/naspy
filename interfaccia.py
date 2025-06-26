# interfaccia.py

import streamlit as st

def crea_sidebar_input():
    """
    Crea la sidebar con i campi di input per il calcolo della NASpI.

    Returns:
        dict: Un dizionario con i valori inseriti dall'utente.
    """
    st.sidebar.header("Inserisci i tuoi dati")
    
    retribuzione_media = st.sidebar.number_input(
        label="Retribuzione Media Mensile Imponibile (€)",
        min_value=0.0,
        max_value=10000.0,
        value=1500.0,
        step=50.0,
        help="Inserisci la retribuzione lorda media mensile degli ultimi 4 anni."
    )
    
    settimane_contributive = st.sidebar.slider(
        label="Settimane di Contribuzione negli Ultimi 4 Anni",
        min_value=0,
        max_value=208,  # 4 anni * 52 settimane
        value=52,
        step=1,
        help="Numero totale di settimane con contributi versati negli ultimi 48 mesi (minimo 13)."
    )
    
    over_55 = st.sidebar.checkbox(
        label="Hai più di 55 anni?",
        value=False,
        help="Seleziona se hai compiuto 55 anni. Cambia l'inizio della riduzione mensile (décalage)."
    )

    calcola_btn = st.sidebar.button(
        label="Calcola NASpI",
        type="primary"
    )

    return {
        "retribuzione": retribuzione_media,
        "settimane": settimane_contributive,
        "over_55": over_55,
        "calcola": calcola_btn
    }
