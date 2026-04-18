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

REFERENCE_FILE = "C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/structured_data/dataframe_completo_sem_duplicatas.csv"
OUTPUT_FILE = "C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/structured_data/firstStep.csv"

def load_data():
    print("Carregando dados...")
    ref_df = pd.read_csv(REFERENCE_FILE)

    if os.path.exists(OUTPUT_FILE):
        out_df = pd.read_csv(OUTPUT_FILE)
    else:
        columns = ref_df.columns.to_list()
        columns.append("status") 
        columns.append("anotation")
        out_df = pd.DataFrame(columns=columns)


    return ref_df, out_df

def get_pending_articles(ref_df, out_df):
    print("Verificando artigos pendentes...")
    processed_titles = set(out_df["Titulo"])
    pending = ref_df[~ref_df["Titulo"].isin(processed_titles)]
    return pending

def ask_user(title,source):
    
    result = None
    anotation = None
    while True:
        print("\n==============================")
        print(f"Título do artigo:\n{title}")
        print(f"Fonte: {source}")
        print("==============================")
        response = input("Passou? (s/n/d): ").strip().lower()
        anotation = input("Anotação (opcional): ").strip()
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
    return result, anotation

def save_progress(out_df):
    out_df.to_csv(OUTPUT_FILE, index=False)

def main():
    ref_df, out_df = load_data()
    pending = get_pending_articles(ref_df, out_df)

    print(f"{len(pending)} artigos pendentes.\n")

    for _, row in pending.iterrows():
        title = row["Titulo"]
        source = row["Fonte"]
        status, anotation = ask_user(title, source)


        new_row = ref_df.loc[ref_df["Titulo"] == title].iloc[0].to_dict()

        new_row["status"] = status
        new_row["anotation"] = anotation

        new_row = pd.DataFrame([new_row])

        out_df = pd.concat([out_df, new_row], ignore_index=True)

        save_progress(out_df)

    print("\n✔ Todos os artigos foram processados!")

if __name__ == "__main__":
    main()