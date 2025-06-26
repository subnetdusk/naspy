# testi.py

def get_introduzione():
    """Restituisce il testo introduttivo sulla NASpI."""
    # Il testo precedente è stato rimosso come richiesto.
    # Puoi lasciare una stringa vuota o una frase più concisa.
    return "Usa questo strumento per calcolare una stima della tua indennità di disoccupazione NASpI."

def get_guida_input():
    """Restituisce la guida alla compilazione degli input."""
    return """
    ### Guida alla Compilazione
    
    1.  **Retribuzione Annua Lorda (RAL)**: Inserisci la retribuzione lorda totale percepita in ciascuno degli ultimi quattro anni solari. Se in un anno non hai lavorato o non hai avuto reddito da lavoro dipendente, lascia il valore a 0.
    
    2.  **Totale Settimane di Contribuzione**: Indica il numero totale di settimane per cui sono stati versati contributi previdenziali nei 48 mesi che precedono la data di cessazione del rapporto di lavoro. Il requisito minimo per accedere alla NASpI è di 13 settimane.
    """

def get_spiegazione_risultati():
    """Restituisce la spiegazione delle regole di calcolo applicate."""
    return """
    ### Come viene calcolato l'importo?
    
    L'importo mensile della NASpI si calcola nel seguente modo:
    
    * **Retribuzione di Riferimento**: Si calcola la retribuzione imponibile previdenziale totale degli ultimi 4 anni e la si divide per il numero di settimane di contribuzione. Il risultato viene moltiplicato per il coefficiente **4,33**.
    
    * **Calcolo dell'Indennità**:
        * Se la retribuzione di riferimento è **pari o inferiore** a un importo di riferimento stabilito annualmente dall'INPS (per il 2025, si utilizza il dato più aggiornato disponibile, qui stimato a €1.425,21), l'indennità è pari al **75%** di tale retribuzione.
        * Se è **superiore**, l'indennità è pari al 75% dell'importo di riferimento più il **25%** della differenza tra la retribuzione di riferimento e l'importo stesso.
    
    * **Massimale**: L'importo dell'indennità non può comunque superare un limite massimo mensile (stimato per il 2025 a €1.550,42).
    
    * **Décalage (Riduzione)**: L'importo si riduce del **3% ogni mese** a partire dal sesto mese di fruizione (o dall'ottavo mese per beneficiari over 55).
    
    ### Come viene calcolata la durata?
    
    La NASpI spetta per un numero di settimane pari alla **metà delle settimane di contribuzione** degli ultimi quattro anni, per un massimo di 24 mesi (104 settimane).
    """
