# testi.py

def get_introduzione():
    """Restituisce il testo introduttivo sulla NASpI."""
    return "Usa questo strumento per calcolare una stima accurata della tua indennità di disoccupazione NASpI basata sul quadriennio mobile."

def get_guida_input():
    """Restituisce la guida alla compilazione degli input."""
    return """
    ### Guida alla Compilazione
    
    1.  **Data di Decorrenza NASpI**: Seleziona il primo giorno di disoccupazione. Il sistema calcolerà automaticamente il periodo di 48 mesi a ritroso su cui si basa il calcolo.
    
    2.  **Retribuzione per Anno**: Inserisci la retribuzione lorda percepita per ciascun anno solare all'interno del periodo di riferimento calcolato.
        - **Anni Intermedi**: Inserisci la Retribuzione Annua Lorda (RAL) completa.
        - **Primo e Ultimo Anno**: Questi sono spesso anni parziali. Segui attentamente le indicazioni sotto ogni campo per inserire solo la retribuzione percepita nei mesi di competenza.
        
    3.  **Totale Settimane di Contribuzione**: Inserisci il numero totale di settimane coperte da contribuzione all'interno dello stesso periodo di riferimento di 48 mesi. Il requisito minimo è di 13 settimane.
    """

def get_spiegazione_risultati():
    """Restituisce la spiegazione delle regole di calcolo applicate."""
    return """
    ### Come viene calcolato l'importo?
    
    L'importo mensile della NASpI si calcola nel seguente modo:
    
    * **Retribuzione di Riferimento**: Si **sommano tutte le retribuzioni imponibili** percepite nei 48 mesi precedenti la data di disoccupazione. Il totale viene **diviso per il numero di settimane** di contribuzione nello stesso periodo. Il risultato viene poi **moltiplicato per il coefficiente 4,33**.
    
    * **Calcolo dell'Indennità**:
        * Se la retribuzione di riferimento è **pari o inferiore** a un importo di riferimento stabilito annualmente dall'INPS (per il 2025, si utilizza il dato più aggiornato disponibile, qui stimato a €1.425,21), l'indennità è pari al **75%** di tale retribuzione.
        * Se è **superiore**, l'indennità è pari al 75% dell'importo di riferimento più il **25%** della differenza tra la retribuzione di riferimento e l'importo stesso.
    
    * **Massimale**: L'importo dell'indennità non può comunque superare un limite massimo mensile (stimato per il 2025 a €1.550,42).
    
    * **Décalage (Riduzione)**: L'importo si riduce del **3% ogni mese** a partire dal sesto mese di fruizione (o dall'ottavo mese per beneficiari over 55).
    
    ### Come viene calcolata la durata?
    
    La NASpI spetta per un numero di settimane pari alla **metà delle settimane di contribuzione** degli ultimi 48 mesi, per un massimo di 24 mesi (104 settimane).
    """
