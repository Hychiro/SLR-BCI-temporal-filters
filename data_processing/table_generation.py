import pandas as pd
import os


# ============================================================
# CONFIGURAÇÃO
# ============================================================

REFERENCE_FILE = r"C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/structured_data/final_output.csv"

OUTPUT_FILE1 = r"C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/structured_data/filter_final_output.csv"

OUTPUT_FILE2 = r"C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/structured_data/datasets_final_output.csv"



COLUNAS1 = [
    "Filter_type", # tipo e nome do filtro
    "Frequency",
    "Titulo",
    "Ano de Publicacao",
    "Country"
]
COLUNAS2 = [
    "Titulo",
    "Fonte",
    "Datasets_used",
    "Ano de Publicacao",
    "Classes",
    "Resultados",
    "Metrics_used"
]


def load_data():
    print("Carregando dados...")
    ref_df = pd.read_csv(REFERENCE_FILE)

    out_df_D = None
    out_df_F = None

    if os.path.exists(OUTPUT_FILE2):

        out_df_D = pd.read_csv(
            OUTPUT_FILE2,
            encoding="utf-8"
        )

        print("\nCSV encontrado!")
        print(f"Total de registros existentes: {len(out_df_D)}")
    else:

        print("\nCSV não encontrado.")
        print("Um novo CSV será criado.")

        out_df_D = pd.DataFrame(columns=COLUNAS2)



    if os.path.exists(OUTPUT_FILE1):

        out_df_F = pd.read_csv(
            OUTPUT_FILE1,
            encoding="utf-8"
        )

        print("\nCSV encontrado!")
        print(f"Total de registros existentes: {len(out_df_F)}")
    else:

        print("\nCSV não encontrado.")
        print("Um novo CSV será criado.")

        out_df_F = pd.DataFrame(columns=COLUNAS1)



    return ref_df, out_df_D, out_df_F

# ============================================================
# 4. FUNÇÃO PARA ADICIONAR UMA LINHA
# ============================================================

def add_linha_F(
    df,
    filter_type,
    frequency,
    country,
    article_name,
    tempo
):

    nova_linha = {
        "Filter_type": filter_type,
        "Frequency": frequency,
        "Country": country,
        "Titulo": article_name,
        "Ano de Publicacao": tempo
    }

    nova_linha_df = pd.DataFrame([nova_linha])

    df = pd.concat(
        [df, nova_linha_df],
        ignore_index=True
    )
    df_final = save_progress(df, OUTPUT_FILE1)
    return df_final

def add_linha_D(
    df,
    titulo,
    fonte,
    datasets_used,
    ano_publicacao,
    classes,
    resultados,
    metrics_used
):
    
    nova_linha = {
        "Titulo": titulo,
        "Fonte": fonte,
        "Datasets_used": datasets_used,
        "Ano de Publicacao": ano_publicacao,
        "Classes": classes,
        "Resultados": resultados,
        "Metrics_used": metrics_used
    }

    nova_linha_df = pd.DataFrame([nova_linha])

    df = pd.concat(
        [df, nova_linha_df],
        ignore_index=True
    )
    df_final = save_progress(df, OUTPUT_FILE2)
    return df_final

def get_pending_articles(ref_df, out_df_D, out_df_F):
    print("Verificando artigos pendentes...")
    processed_titles = set(out_df_D["Titulo"]) | set(out_df_F["Titulo"])
    pending = ref_df[~ref_df["Titulo"].isin(processed_titles)]
    return pending

def ask_user(out_df_D, out_df_F, len_pending, anotation, title, source, year, temporal_filters, datasets):
    
    result = ""
    print("\n==============================")
    print(f"Artigos pendentes: {len_pending}")
    print("------------------------------")
    print(f"Título do artigo:\n{title}")
    print("------------------------------")
    print(f"Fonte: {source}")
    print("------------------------------")
    print(f"Ano de publicação: {year}")
    print("------------------------------")
    print(f"Anotação: {anotation}")
    print("------------------------------")
    print(f"Filtros temporais: {temporal_filters}")
    print("------------------------------")
    print(f"Datasets utilizados: {datasets}")
    print("==============================")
    flag = True
    while flag:
        print("\nDeseja adicionar informações sobre os filtros do artigo? (sim/não)")
        result = input().strip().lower()
        response = []
        if result in ["sim", "s"]:
            for criteria in ["Filter_type","Frequency","Country"]:
                while True:
                    result2 = ""
                    if criteria == "Filter_type" :
                        string = "Qual o filtro do artigo?"
                    elif criteria == "Frequency" :
                        string = "Qual/is a/s frequencia/s usada/s?"
                    elif criteria == "Country" :
                        string = "Qual o país de origem do artigo?"
                    print(f"\n{string}")
                    result2 = input().strip().lower()
                    if result2 == "":
                        print("Resposta inválida.")
                    else:
                        response.append(result2)
                        break
            out_df_F = add_linha_F(
                                out_df_F,
                                filter_type=response[0],
                                frequency=response[1],
                                country=response[2],
                                article_name=title,
                                tempo=year
                                )
                    
        else:
            flag = False

        
    ###################################################################################

    flag = True
    while flag:
        print("\nDeseja adicionar informações sobre os datasets do artigo? (sim/não)")
        result = input().strip().lower()
        response = []
        if result in ["sim", "s"]:
            for criteria in ["Datasets_used","Classes","Metrics_used"]:
                while True:
                    result2 = ""
                    if criteria == "Datasets_used":
                        string = "Qual o dataset utilizado?"
                    elif criteria == "Classes":
                        string = "Qual a quantidade de classes?"
                    elif criteria == "Metrics_used":
                        string = "Qual(is) a(s) métrica(s) utilizada(s)?"
                    print(f"\n{string}")
                    result2 = input().strip().lower()
                    if result2 == "":
                        print("Resposta inválida.")
                    else:
                        response.append(result2)
                        break
            out_df_D = add_linha_D(
                out_df_D,
                titulo=title,
                fonte=source,
                datasets_used=response[0],
                ano_publicacao=year,
                classes=response[1],
                metrics_used=response[2],
                resultados=datasets
            )
        else:
            flag = False

    return out_df_D, out_df_F


def save_progress(out_df, OUTPUT_FILE):
    out_df.to_csv(OUTPUT_FILE, index=False)
    print("\n Progresso salvo.\n")
    return out_df

def main():
    ref_df, out_df_D, out_df_F = load_data()
    pending = get_pending_articles(ref_df, out_df_D, out_df_F)
    len_pending = len(pending)
    print(f"{len_pending} artigos pendentes.\n")
    for _, row in pending.iterrows():
        title = row["Titulo"]
        source = row["Fonte"]
        anotation = row["Anotation"]
        year = row["Ano de Publicacao"]
        temporal_filters  = row["Temporal_filters_used"]
        datasets = row["Datasets_used"]
        
        out_df_D, out_df_F = ask_user(out_df_D, out_df_F,len_pending, anotation, title, source, year, temporal_filters, datasets)
        len_pending -= 1
    
    print("\n✔ Todos os artigos foram processados!")

if __name__ == "__main__":
    main()

