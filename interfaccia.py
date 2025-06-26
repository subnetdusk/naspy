# interfaccia.py

import streamlit as st
from datetime import date

def crea_form_input():
    """
    Crea un form, mostra i widget per l'inserimento dati, e restituisce
    i dati e lo stato del pulsante.

    Returns:
        tuple: (dict_dati, bool_inviato)
               - dict_dati: dizionario con i valori del form.
               - bool_inviato: True se il form è stato inviato, altrimenti False.
    """
    with st.form("calcolo_form"):
        st.subheader("1. Inserisci i dati per il calcolo")
        
        st.write("""
        Inserisci la **Retribuzione Annua Lorda (RAL)** per ciascuno degli ultimi quattro anni.
        - Per l'**anno in corso**, inserisci la retribuzione percepita fino alla data di fine contratto.
        - Se un anno non è stato lavorato, lascia il valore a 0.
        """)
        
        anno_corrente = date.today().year
        
        ral_1 = st.number_input(
            label=f"Primo Anno ({anno_corrente - 3})", 
            min_value=0.0, 
            value=0.0, 
            step=100.0
        )
        ral_2 = st.number_input(
            label=f"Secondo Anno ({anno_corrente - 2})", 
            min_value=0.0, 
            value=0.0, 
            step=100.0
        )
        ral_3 = st.number_input(
            label=f"Terzo Anno ({anno_corrente - 1})", 
            min_value=0.0, 
            value=20000.0, 
            step=100.0
        )
        ral_4 = st.number_input(
            label=f"Quarto Anno ({anno_corrente})", 
            min_value=0.0, 
            value=10000.0, 
            step=100.0,
            help="Inserisci la retribuzione lorda percepita quest'anno fino alla fine del contratto."
        )
        
        lista_ral = [ral_1, ral_2, ral_3, ral_4]
        
        st.markdown("---")

        # --- BLOCCO CORRETTO ---
        # La parentesi di chiusura ')' è stata ripristinata.
        settimane_contributive = st.slider(
            label="Totale Settimane di Contribuzione negli Ultimi 4 Anni",
            min_value=0, 
            max_value=208, 
            value=38, 
            step=1,
            help="Numero totale di settimane con contributi versati negli ultimi 48 mesi (minimo 13)."
        )
        
        over_55 = st.checkbox(
            label="Hai più di 55 anni?",
            value=False,
            help="Seleziona se hai compiuto 55 anni. Cambia l'inizio della riduzione mensile (décalage)."
        )

        submitted = st.form_submit_button(
            "Calcola Stima NASpI", 
            use_container_width=True, 
            type="primary"
        )
        
        dati_input = {
            "lista_ral": [ral_1, ral_2, ral_3, ral_4],
            "settimane": settimane_contributive,
            "over_55": over_55
        }

    return dati_input, submitted
