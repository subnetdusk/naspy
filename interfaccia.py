# interfaccia.py

import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

def crea_form_input():
    """
    Crea un form, mostra i widget e restituisce i dati e lo stato del pulsante.
    Questa versione usa una sintassi estremamente sicura per evitare errori.
    """
    with st.form("calcolo_form"):
        st.subheader("1. Inserisci i dati per il calcolo")

        # --- Sezione Data ---
        data_inizio_naspi = st.date_input(
            label="Seleziona la data di decorrenza della NASpI",
            value=date.today(),
            min_value=date(2020, 1, 1),
            max_value=date.today().replace(year=date.today().year + 1),
            format="DD/MM/YYYY",
            help="È la data di inizio della disoccupazione.",
        )

        st.markdown("---")

        # --- Sezione Calcolo Periodo e Guida ---
        fine_periodo = data_inizio_naspi
        inizio_periodo = fine_periodo - relativedelta(years=4)
        
        start_str = inizio_periodo.strftime('%d/%m/%Y')
        end_str = fine_periodo.strftime('%d/%m/%Y')

        st.info(f"Periodo di riferimento calcolato (48 mesi): Dal **{start_str}** al **{end_str}**.")
        st.write("Inserisci le retribuzioni lorde percepite in questo intervallo, suddivise per anno solare.")

        # --- Sezione Input RAL (5 anni) ---
        anni_coinvolti = list(range(inizio_periodo.year, fine_periodo.year + 1))
        lista_ral = []
        valori_default = [0, 0, 21000, 22000, 11000]

        for i, anno in enumerate(anni_coinvolti):
            help_text = f"Inserire la RAL totale per l'anno {anno}."
            if anno == inizio_periodo.year:
                help_text = f"ATTENZIONE: Inserire solo la retribuzione da {inizio_periodo.strftime('%B %Y')} in poi."
            if anno == fine_periodo.year:
                 help_text = f"ATTENZIONE: Inserire solo la retribuzione fino a {fine_periodo.strftime('%B %Y')}."

            ral_input = st.number_input(
                label=f"Retribuzione percepita nell'anno {anno}",
                min_value=0.0,
                value=float(valori_default[i] if i < len(valori_default) else 0.0),
                step=100.0,
                help=help_text,
            )
            lista_ral.append(ral_input)
