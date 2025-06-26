# interfaccia.py

import streamlit as st
from datetime import date

def mostra_campi_input():
    """
    Mostra i widget per l'inserimento dei dati (4 RAL annuali in ordine cronologico) 
    e restituisce i valori.

    Returns:
        dict: Un dizionario con i valori inseriti dall'utente.
    """
    st.subheader("1. Inserisci i dati per il calcolo")
    
    st.write("Inserisci la **Retribuzione Annua Lorda (RAL)** per ciascuno degli ultimi quattro anni. Se un anno non è stato lavorato, lascia il valore a 0.")
    
    # Calcola dinamicamente gli anni di riferimento
    anno_corrente = date.today().year
    anno_piu_recente = anno_corrente - 1
    
    # Creiamo i 4 box di input per le RAL in ordine cronologico
    ral_1 = st.number_input(
        label=f"Primo Anno ({anno_piu_recente - 3})", 
        min_value=0.0, 
        value=0.0, 
        step=100.0
    )
    ral_2 = st.number_input(
        label=f"Secondo Anno ({anno_piu_recente - 2})", 
        min_value=0.0, 
        value=0.0, 
        step=100.0
    )
    ral_3 = st.number_input(
        label=f"Terzo Anno ({anno_piu_recente - 1})", 
        min_value=0.0, 
        value=0.0, 
        step=100.0
    )
    ral_4
