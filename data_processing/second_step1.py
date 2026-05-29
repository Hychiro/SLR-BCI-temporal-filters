"""
Este script é a primeira etapa do processo de 
classificação dos artigos. Ele lê os títulos dos 
artigos de um arquivo CSV de referência, apresenta 
cada título ao usuário e solicita que ele classifique o 
artigo como "passou" ou "não passou". O progresso é salvo 
em um arquivo CSV de saída para que o usuário possa retomar 
o processo posteriormente, se necessário.
"""

import pandas as pd
import os

REFERENCE_FILE = "C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/structured_data/sortedDataFromFirstStepOutput.csv"
OUTPUT_FILE = "C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/structured_data/secondStepBaixados.csv"


def load_data():
    print("Carregando dados...")
    ref_df = pd.read_csv(REFERENCE_FILE)

    if os.path.exists(OUTPUT_FILE):
        out_df = pd.read_csv(OUTPUT_FILE)
    else:
        columns = ref_df.columns.to_list()
        columns.append("Baixou")
        out_df = pd.DataFrame(columns=columns)


    return ref_df, out_df

def get_pending_articles(ref_df, out_df):
    print("Verificando artigos pendentes...")
    processed_titles = set(out_df["Titulo"])
    pending = ref_df[~ref_df["Titulo"].isin(processed_titles)]
    return pending

def ask_user(title, source, status, eeg, bci, mi, classification, model_pipeline, temporal_filter):
    
    result = ""
    while True:
        print("\n==============================")
        print(f"Título do artigo:\n{title}")
        print(f"Fonte: {source}")
        print("Classificação atual:")
        print(f"Status: {status} | EEG: {eeg} | BCI: {bci} | MI: {mi} | Classification: {classification} | Model/pipeline: {model_pipeline} | Temporal_filter: {temporal_filter}")
        print("==============================")
        response = input("Baixou? (s/n/d): ").strip().lower()
        if response in ["s", "sim"]:
                result = "passou"
                break
        
    return result

def save_progress(out_df):
    out_df.to_csv(OUTPUT_FILE, index=False)

def main():
    ref_df, out_df = load_data()
    pending = get_pending_articles(ref_df, out_df)

    print(f"{len(pending)} artigos pendentes.\n")
    columns = out_df.columns.to_list()
    columns = [col for col in columns if col not in ["Titulo", "Fonte","Status","Anotation","Autores","Ano de Publicacao"]]
    for _, row in pending.iterrows():
        title = row["Titulo"]
        source = row["Fonte"]
        status = row["Status"]
        eeg = row["EEG"]
        bci = row["BCI"]
        mi = row["MI"]
        classification = row["Classification"]
        model_pipeline = row["Model/pipeline"]
        temporal_filter = row["Temporal_filter"]
        
        result = ask_user(title, source, status, eeg, bci, mi, classification, model_pipeline, temporal_filter)


        new_row = ref_df.loc[ref_df["Titulo"] == title].iloc[0].to_dict()

        new_row["Baixou"] = result

        new_row = pd.DataFrame([new_row])

        out_df = pd.concat([out_df, new_row], ignore_index=True)

        save_progress(out_df)

    print("\n✔ Todos os artigos foram processados!")

if __name__ == "__main__":
    main()