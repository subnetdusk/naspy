# interfaccia.py

import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta # Dobbiamo importare questa utilità

def crea_form_input():
    """
    Crea un form che chiede la data di inizio disoccupazione e 5 RAL parziali/totali,
    e restituisce i dati e lo stato del pulsante.
    """
    with st.form("calcolo_form"):
        st.subheader("1. Inserisci i dati per il calcolo")
        
        # --- NUOVO: INPUT DATA ---
        data_inizio_naspi = st.date_input(
            "Seleziona la data di decorrenza della NASpI",
            value=date.today(),
            min_value=date(2020, 1, 1),
            max_value=date.today().replace(year=date.today().year + 1),
            format="DD/MM/YYYY",
            help="È la data di inizio della disoccupazione (solitamente il giorno dopo la fine del contratto)."
        )

        st.markdown("---")

        # --- LOGICA DINAMICA PER 5 ANNI E PERIODI PARZIALI ---
        fine_periodo = data_inizio_naspi
        inizio_periodo = fine_periodo - relativedelta(years=4)

        st.info(f"""
        **Periodo di riferimento per il calcolo (48 mesi):** Dal **{inizio_periodo.strftime('%d/%m/%Y')}** al **{fine_periodo.strftime('%d/%m/%Y')}**.
        
        Inserisci di seguito le retribuzioni lorde percepite in questo intervallo, suddivise per anno solare.
        """)

        anni_coinvolti = range(inizio_periodo.year, fine_periodo.year + 1)
        lista_ral = []
        valori_default = [0, 0, 21000, 22000, 11000] # Valori di esempio

        for i, anno in enumerate(anni_coinvolti):
            help_text = ""
            # Gestione dinamica dell'help text per anni parziali
            if anno == inizio_periodo.year and anno != fine_periodo.year:
                help_text = f"ATTENZIONE: Inserire solo la retribuzione da {inizio_periodo.strftime('%B %Y')} a Dicembre {anno}."
            elif anno == fine_periodo.year and anno != inizio_periodo.year:
                 help_text = f"ATTENZIONE: Inserire solo la retribuzione da Gen
