# app.py

import streamlit as st
import pandas as pd
from interfaccia import crea_form_input
from calcolo import calcola_naspi, calcola_piano_decalage
from testi import get_introduzione, get_guida_input, get_spiegazione_risultati

# --- IMPOSTAZIONI PAGINA ---
st.set_page_config(
    page_title="Calcolatore NASpI Scuola 2025",
    page_icon="🎓",
    layout="wide"
)

# --- TITOLO E INTRODUZIONE ---
st.title("🎓 Calcolatore NASpI per Personale Scuola 2025")
st.markdown(get_introduzione())
st.markdown("---")

# --- LAYOUT PRINCIPALE A DUE COLONNE ---
col1, col2 = st.columns(spec=[1.5, 2], gap="large")

# --- COLONNA 1: INPUT E GUIDE ---
with col1:
    # La funzione crea il form e restituisce i dati e lo stato di invio
    user_input, submitted = crea_form_input()

    # Le guide rimangono qui
    st.subheader("Approfondimenti")
    with st.expander("Guida alla compilazione dei dati"):
        st.markdown(get_guida_input())
    
    with st.expander("Come funziona il calcolo? (Riferimenti Normativi)"):
        st.markdown(get_spiegazione_risultati())
        st.info(
            "**Nota Bene**: I valori di riferimento per il calcolo (massimale e soglia) sono basati sugli importi "
            "del 2024 e verranno aggiornati con le circolari INPS per il 2025 non appena disponibili."
        )

# --- COLONNA 2: RISULTATI ---
with col2:
    st.subheader("2. Visualizza il Risultato")

    if submitted:
        # Esegui il calcolo solo dopo aver premuto il pulsante
        risultato = calcola_naspi(user_input["lista_ral"], user_input["settimane"])
        
        if not risultato["requisiti_soddisfatti"]:
            st.error(f"**Requisiti non soddisfatti.**\n\n{risultato['messaggio_errore']}")
        else:
            st.success("**Stima calcolata con successo!**")
            
            st.metric(
                label="Retribuzione Mensile di Riferimento (calcolata)",
                value=f"€ {risultato['retribuzione_riferimento_calcolata']:.2f}",
                help="Questa è la retribuzione media mensile, calcolata sulla base dei dati inseriti, che viene usata come base per il calcolo dell'indennità."
            )
            st.markdown("---")
            
            m1, m2 = st.columns(2)
            m1.metric(
                label="Indennità Mensile Lorda Iniziale",
                value=f"€ {risultato['importo_mensile_lordo']:.2f}"
            )
            m2.metric(
                label="Durata Massima",
                value=f"{risultato['durata_mesi']} mesi ({risultato['durata_settimane']} settimane)"
            )
            
            st.markdown("---")
            
            piano_ammortamento = calcola_piano_decalage(
                risultato["importo_mensile_lordo"],
                risultato["durata_mesi"],
                user_input["over_55"]
            )
            
            df_piano = pd.DataFrame({
                "Mese": range(1, len(piano_ammortamento) + 1),
                "Importo Lordo Mensile (€)": piano_ammortamento
            })

            st.write("**Andamento dell'indennità nel tempo (Décalage)**")
            st.line_chart(df_piano.set_index("Mese"), use_container_width=True)
            
            with st.expander("Mostra tabella dettagliata del piano di erogazione"):
                st.dataframe(df_piano, hide_index=True, use_container_width=True)
    else:
        st.info("Compila i dati nel modulo a sinistra e premi il pulsante 'Calcola Stima NASpI' per visualizzare il risultato.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center;'>Realizzato per il repository 'naspy' - Progetto di esempio Streamlit.</div>", unsafe_allow_html=True)
