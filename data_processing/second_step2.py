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
OUTPUT_FILE = "C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/structured_data/secondStepOutput.csv"


def load_data():
    print("Carregando dados...")
    ref_df = pd.read_csv(REFERENCE_FILE)

    if os.path.exists(OUTPUT_FILE):
        out_df = pd.read_csv(OUTPUT_FILE)
    else:
        columns = ref_df.columns.to_list()
        columns.append("Status")
        columns.append("EEG")
        columns.append("BCI")
        columns.append("MI")
        columns.append("Classification")
        columns.append("Model/pipeline")
        columns.append("Temporal_filter")
        columns.append("Anotation")
        out_df = pd.DataFrame(columns=columns)


    return ref_df, out_df

def get_pending_articles(ref_df, out_df):
    print("Verificando artigos pendentes...")
    processed_titles = set(out_df["Titulo"])
    pending = ref_df[~ref_df["Titulo"].isin(processed_titles)]
    return pending

def ask_user(len_pending, title, source, status, eeg, bci, mi, classification, model_pipeline, temporal_filter, anotation, columns):
    
    result = ""
    new_anotation = ""
    print("\n==============================")
    print(f"Artigos pendentes: {len_pending}")
    print(f"Título do artigo:\n{title}")
    print(f"Fonte: {source}")
    print("Classificação atual:")
    print(f"Status: {status} | EEG: {eeg} | BCI: {bci} | MI: {mi} | \n Classification: {classification} | Model/pipeline: {model_pipeline} | Temporal_filter: {temporal_filter}")
    print(f"\nAnotation: {anotation}")
    print("==============================")
    responseList = []
    for criteria in columns:
        string = ""
        while True:
            if criteria == "EEG" :
                string = "O artigo envolve o uso de EEG?"
            elif criteria == "BCI" :
                string = "O artigo envolve o uso de BCI?"
            elif criteria == "MI" :
                string = "O artigo envolve o paradigma de MI?"
            elif criteria == "Classification" :
                string = "O artigo envolve paradigma de classificação ?"
            elif criteria == "Model/pipeline" :
                string = "O artigo envolve o uso de um modelo/pipeline completo de ML?"
            elif criteria == "Temporal_filter" :
                string = "O artigo aparenta explicitamente ter o uso de" \
                " filtros temporais como filtros temporais?"
            print(f"\n{string}")
            response = input("Passou? (s/n/d): ").strip().lower()
            if response in ["s", "sim"]:
                result = "passou"
                break
            elif response in ["n", "nao", "não"]:
                result = "nao_passou"
                break
            elif response in ["d", "depende"]:
                result = "depende"
                break
            else:
                print("Resposta inválida. Digite 's', 'n' ou 'd'.")
        responseList.append(result)
    status = ""
    if responseList[0] == "nao_passou" or responseList[1] == "nao_passou" or responseList[2] == "nao_passou":
        status = "nao_passou"
    elif responseList[0] == "passou" and responseList[1] == "passou" and responseList[2] == "passou":
        if responseList[3] == "nao_passou" or responseList[4] == "nao_passou" or responseList[5] == "nao_passou":
            status = "depende"
        elif responseList[3] == "depende" or responseList[4] == "depende" or responseList[5] == "depende":
            status = "depende"
        else:
            status = "passou"
    elif responseList[0] == "depende" or responseList[1] == "depende" or responseList[2] == "depende":
            status = "depende"
    
    status2 = input("Artigo em inglês? (s/n/d): ").strip().lower()
    if status2 in ["n", "nao", "não"]:
        status = "nao_passou"

    new_anotation = input("Anotação (opcional): ").strip()
    return status, responseList, new_anotation

def save_progress(out_df):
    out_df.to_csv(OUTPUT_FILE, index=False)

def main():
    ref_df, out_df = load_data()
    pending = get_pending_articles(ref_df, out_df)
    len_pending = len(pending)
    print(f"{len_pending} artigos pendentes.\n")
    
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
        anotation = row["Anotation"]
        
        status, responseList, new_anotation = ask_user(len_pending, title, source, status, eeg, bci, mi, classification, model_pipeline, temporal_filter, anotation, columns)
        len_pending -= 1

        new_row = ref_df.loc[ref_df["Titulo"] == title].iloc[0].to_dict()

        new_row["Status"] = status
        new_row["Anotation"] = new_anotation
        new_row["EEG"] = responseList[0]
        new_row["BCI"] = responseList[1]
        new_row["MI"] = responseList[2]
        new_row["Classification"] = responseList[3]
        new_row["Model/pipeline"] = responseList[4]
        new_row["Temporal_filter"] = responseList[5]

        new_row = pd.DataFrame([new_row])

        out_df = pd.concat([out_df, new_row], ignore_index=True)

        save_progress(out_df)

    print("\n✔ Todos os artigos foram processados!")

if __name__ == "__main__":
    main()