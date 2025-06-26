# app.py

import streamlit as st
import pandas as pd
from interfaccia import crea_sidebar_input
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

# --- SIDEBAR CON INPUT ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Inps_logo.svg/1200px-Inps_logo.svg.png", width=100)
user_input = crea_sidebar_input()

# --- AREA PRINCIPALE ---
col1, col2 = st.columns((1, 1), gap="large")

with col1:
    st.subheader("Guida e Riferimenti")
    with st.expander("Guida alla compilazione dei dati"):
        st.markdown(get_guida_input())
    
    with st.expander("Come funziona il calcolo? (Riferimenti Normativi)"):
        st.markdown(get_spiegazione_risultati())
        st.info(
            "**Nota Bene**: I valori di riferimento per il calcolo (massimale e soglia) sono basati sugli importi "
            "del 2024 e verranno aggiornati con le circolari INPS per il 2025 non appena disponibili. "
            "Il calcolo è da intendersi come una stima."
        )


with col2:
    st.subheader("Risultato del Calcolo")
    
    if user_input["calcola"]:
        # Esegui il calcolo
        risultato = calcola_naspi(user_input["retribuzione"], user_input["settimane"])
        
        if not risultato["requisiti_soddisfatti"]:
            st.error(risultato["messaggio_errore"])
        else:
            st.success("Requisiti per la NASpI soddisfatti!")
            
            # Visualizzazione metriche principali
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
            
            # Calcolo e visualizzazione piano di ammortamento (décalage)
            piano_ammortamento = calcola_piano_decalage(
                risultato["importo_mensile_lordo"],
                risultato["durata_mesi"],
                user_input["over_55"]
            )
            
            df_piano = pd.DataFrame({
                "Mese": range(1, len(piano_ammortamento) + 1),
                "Importo Lordo Mensile (€)": piano_ammortamento
            })

            st.write("**Piano di Erogazione Mensile (con décalage)**")
            st.dataframe(df_piano, hide_index=True)

            # Grafico dell'andamento
            st.write("**Andamento dell'indennità nel tempo**")
            st.line_chart(df_piano.set_index("Mese"))

    else:
        st.info("Inserisci i dati nella barra laterale e premi 'Calcola NASpI' per visualizzare i risultati.")


# --- FOOTER ---
st.markdown("---")
st.markdown("Realizzato per il repository 'naspy' - Progetto di esempio Streamlit.")
