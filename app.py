# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from dateutil.relativedelta import relativedelta

# Le funzioni che non danno problemi rimangono nei loro file
from calcolo import calcola_naspi, calcola_piano_decalage
from testi import get_introduzione, get_guida_input, get_spiegazione_risultati

# --- IMPOSTAZIONI PAGINA ---
st.set_page_config(
    page_title="Calcolatore NASpI Scuola 2025",
    page_icon="🎓",
    layout="wide",
)

# --- TITOLO E INTRODUZIONE ---
st.title("🎓 Calcolatore NASpI per Personale Scuola 2025")
st.markdown(get_introduzione())
st.markdown("---")

# --- LAYOUT PRINCIPALE A DUE COLONNE ---
col1, col2 = st.columns(spec=[1.5, 2], gap="large")

# --- COLONNA 1: INPUT E GUIDE ---
with col1:
    st.subheader("1. Inserisci i dati per il calcolo")

    data_inizio_naspi = st.date_input(
        label="Seleziona la data di decorrenza della NASpI",
        value=date.today(),
        format="DD/MM/YYYY",
        help="È la data di inizio della disoccupazione.",
    )
    
    fine_periodo = data_inizio_naspi
    inizio_periodo = fine_periodo - relativedelta(years=4)
    
    with st.form("calcolo_form"):
        start_str = inizio_periodo.strftime('%d/%m/%Y')
        end_str = fine_periodo.strftime('%d/%m/%Y')

        st.info(f"Periodo di riferimento (48 mesi): Dal **{start_str}** al **{end_str}**.")
        st.write("Inserisci le retribuzioni lorde per ogni anno solare in questo intervallo.")
        
        anni_coinvolti = list(range(inizio_periodo.year, fine_periodo.year + 1))
        lista_ral = []
        valori_default = [0.0, 0.0, 21000.0, 22000.0, 11000.0]

        for i, anno in enumerate(anni_coinvolti):
            if anno == inizio_periodo.year:
                data_fine_anno = date(anno, 12, 31)
                etichetta = f"Retribuzione dal {inizio_periodo.strftime('%d/%m/%Y')} al {data_fine_anno.strftime('%d/%m/%Y')}"
            else:
                etichetta = f"Retribuzione percepita nell'anno {anno}"
            
            default_val = valori_default[i] if i < len(valori_default) else 0.0
            
            help_text_ultimo_anno = ""
            if anno == fine_periodo.year and anno != inizio_periodo.year:
                help_text_ultimo_anno = f"Inserire la retribuzione fino al {fine_periodo.strftime('%d/%m/%Y')}."

            ral_input = st.number_input(
                label=etichetta,
                min_value=0.0,
                value=default_val,
                step=100.0,
                key=f"ral_{anno}",
                help=help_text_ultimo_anno
            )
            lista_ral.append(ral_input)

        st.markdown("---")

        settimane_contributive = st.slider(
            label="Totale Settimane di Contribuzione nei 48 mesi",
            min_value=0, max_value=208, value=38, step=1,
            help=f"Inserire le settimane con contributi versati tra il {start_str} e il {end_str}.",
        )
        
        over_55 = st.checkbox(
            label="Hai più di 55 anni alla data di richiesta?",
            value=False,
            help="Cambia l'inizio della riduzione mensile (décalage).",
        )

        submitted = st.form_submit_button(
            label="Calcola Stima NASpI",
            use_container_width=True,
            type="primary",
        )

    st.subheader("Approfondimenti")
    with st.expander("Guida alla compilazione dei dati"):
        st.markdown(get_guida_input())
    
    with st.expander("Come funziona il calcolo? (Riferimenti Normativi)"):
        st.markdown(get_spiegazione_risultati())
    
    st.info(
        "**Nota Bene**: I valori di riferimento sono basati sui dati più recenti e verranno aggiornati appena disponibili quelli per l'anno in corso."
    )

# --- COLONNA 2: RISULTATI ---
with col2:
    st.subheader("2. Visualizza il Risultato")

    if submitted:
        st.success(f"**Stima calcolata per il periodo dal {inizio_periodo.strftime('%d/%m/%Y')} al {fine_periodo.strftime('%d/%m/%Y')}**")

        user_input_data = {
            "lista_ral": lista_ral,
            "settimane": settimane_contributive,
            "over_55": over_55
        }
        risultato = calcola_naspi(user_input_data["lista_ral"], user_input_data["settimane"])
        
        if not risultato["requisiti_soddisfatti"]:
            st.error(f"**Requisiti non soddisfatti.**\n\n{risultato['messaggio_errore']}")
        else:
            st.metric(
                label="Retribuzione Mensile di Riferimento (calcolata)",
                value=f"€ {risultato['retribuzione_riferimento_calcolata']:.2f}",
                help="Retribuzione media mensile usata come base per il calcolo.",
            )
            st.markdown("---")
            
            m1, m2 = st.columns(2)
            m1.metric(label="Indennità Mensile Lorda Iniziale", value=f"€ {risultato['importo_mensile_lordo']:.2f}")
            m2.metric(label="Durata Massima", value=f"{risultato['durata_mesi']} mesi ({risultato['durata_settimane']} settimane)")
            
            st.markdown("---")
            
            piano_lordo = calcola_piano_decalage(
                risultato["importo_mensile_lordo"],
                risultato["durata_mesi"],
                user_input_data["over_55"],
            )
            
            tassazione = 0.15
            piano_netto = [round(lordo * (1 - tassazione), 2) for lordo in piano_lordo]

            df_wide = pd.DataFrame({
                "Mese": range(1, len(piano_lordo) + 1),
                "Importo Lordo (€)": piano_lordo,
                f"Importo Netto (stima -{tassazione:.0%})": piano_netto
            })
            
            st.write("**Andamento dell'indennità nel tempo (Lordo vs. Netto)**")
            
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=df_wide['Mese'],
                y=df_wide['Importo Lordo (€)'],
                name='Lordo',
                marker_color='royalblue',
                text=df_wide['Importo Lordo (€)'],
                texttemplate='%{text:.2f}',
                textposition='outside',
                textfont=dict(color='black') # Rendiamo il testo nero
            ))

            fig.add_trace(go.Bar(
                x=df_wide['Mese'],
                y=df_wide[f"Importo Netto (stima -{tassazione:.0%})"],
                name='Netto',
                marker_color='darkorange',
                text=df_wide[f"Importo Netto (stima -{tassazione:.0%})"],
                texttemplate='%{text:.2f}',
                textposition='inside',
                insidetextanchor='middle'
            ))

            # --- MODIFICA ESEGUITA QUI ---
            # 1. Calcoliamo il valore massimo sull'asse Y
            max_y_value = df_wide['Importo Lordo (€)'].max()
            # 2. Aggiungiamo un 15% di "aria" per far spazio all'etichetta
            y_axis_upper_limit = max_y_value * 1.15 

            fig.update_layout(
                barmode='overlay',
                xaxis_title='Mese',
                yaxis_title='Importo (€)',
                legend_title_text='Tipo Importo',
                # 3. Applichiamo il nuovo limite massimo all'asse Y
                yaxis=dict(range=[0, y_axis_upper_limit]) 
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("Mostra tabella dettagliata del piano di erogazione"):
                st.dataframe(df_wide, hide_index=True, use_container_width=True)
    else:
        st.info("Compila i dati nel modulo a sinistra e premi il pulsante 'Calcola Stima NASpI'.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center;'>Realizzato per il repository 'naspy'.</div>", unsafe_allow_html=True)
