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
        #put colum review_survey after status
        columns.append("Review_Survey")
        change_index = columns.index("Status")
        columns.insert(change_index + 1, columns.pop(columns.index("Review_Survey")))
        print(columns)
        columns.append("Objective")
        columns.append("Model_used")
        columns.append("Temporal_filters_used")
        columns.append("Datasets_used")
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
            if criteria == "Review_Survey" :
                string = "O artigo é uma review ou survey da area? Se for, vale a pena considerar."\
                "O que caracteriza como survey ou review da área? Fala de EEG,BCI,MI ou muitas " \
                "areas ao mesmo tempo desde que tenha MI, Metodos/Modelos) (focar na ideologia)"
            if criteria == "EEG" :
                string = "os dados coletados ou o dataset desses dados é de origem de EEG? Os dados " \
                "devem ser puros na classificação, ou seja não ser dado hybrido de EEG+outra fonte de coleta."
            elif criteria == "BCI" :
                string = "é uma aplicação de BCI ou só usa isso de referencia pra outro trabalho?"
            elif criteria == "MI" :
                string = "o artigo fala sobre motor imagery como proposito de paradigma a ser trabalhado?" \
                " É um paradigma misto que envolve MI ? Se for misto verificar se existe uma separação clara " \
                "dos paradigmas em datasets pois ai ao menos um dos datasets poderá ser trabalhado como MI." \
                " Verificar se a classificação permanece pura também para comparação na SLR."
            elif criteria == "Classification" :
                string = "ocorre a classificação  das tarefas obtidas da coleta? Os dados são só de BCI MI?" \
                " Está claro como foi feita a comparação das classes? Se o artigo não explicita com o que é feita " \
                "a comparação e nem como é feita a comparação pode cortar o artigo."
            elif criteria == "Model/pipeline" :
                string = "Existem metodos ou etapas a serem aplicados para o processamento dos dado (como por exemplo sequencia de camadas de redes neurais)?"
            elif criteria == "Temporal_filter" :
                string = "existe algum filtro temporal presente na sequencia do pipeline?"\
                "O modelo tem integrado um filtro temporal? É possivel separar o filtro do modelo?"\
                "Saber o filtro é o mais importante para poder depois discutir na SLR sua funcionalidade,"\
                "classificação e proposito. Não ficando clara, seja por não especificação do autor, seja por"\
                "dificuldade interpretativa do revisor (eu) separar esse paper a parte com um depende e depois" \
                "voltar revisão os artigos daqui 1 a 1.\n" \
                "Ou seja, atua: " \
                "\n- Removing noise and unwanted fluctuations" \
                "\n- Smoothing the signal" \
                "\n- Selecting important frequency ranges (1 or more, thus including filterbank types)" \
                "\n- Reducing errors and artifacts" \
                "\n- Highlighting relevant temporal patterns or changes" 
            print(f"\n{string}")
            response = input("Passou? (s/n): ").strip().lower()
            if response in ["s", "sim"]:
                result = "sim"
                break
            elif response in ["n", "nao", "não"]:
                result = "nao"
                break
            elif response in ["d", "depende"]:
                result = "depende"
                break
            else:
                print("Resposta inválida. Digite 's', 'n' ou 'd'.")
        responseList.append(result)
    new_status = ""
    status2 = ""
    if  responseList[1] == "nao" or responseList[2] == "nao" or responseList[3] == "nao" or responseList[4] == "nao" or responseList[5] == "nao" or responseList[6] == "nao":
        new_status = "nao"
    else:
        new_status = "sim"
    status2 = input("Artigo em inglês? (s/n): ").strip().lower()
    if status2 in ["n", "nao", "não"]:
        new_status = "nao"

    new_anotation = input("Anotação (opcional): ").strip()
    return new_status, responseList, new_anotation

def second_ask_user(title, columns):
    
    
    print("\n==============================")
    print("Continuando classificação do artigo")
    print(f"Título do artigo:\n{title}")
    print("==============================")
    responseList = []
    for criteria in columns:
        string = ""
        result = ""
        while True:
            if criteria == "Objective" :
                string = "Qual o objetivo do artigo?"
            elif criteria == "Model_used" :
                string = "Qual o modelo usado no artigo?"
            elif criteria == "Temporal_filters_used" :
                string = "Quais os filtros temporais utilizados (separar por virgula)?"
            elif criteria == "Datasets_used" :
                string = "Quais os datasets utilizados (separar por virgula e colocar a media para cada um)?"
            print(f"\n{string}")
            result = input().strip().lower()
            if result == "":
                print("Resposta inválida.")
            else:
                break
        responseList.append(result)
    return responseList


def save_progress(out_df):
    out_df.to_csv(OUTPUT_FILE, index=False)

def main():
    ref_df, out_df = load_data()
    pending = get_pending_articles(ref_df, out_df)
    len_pending = len(pending)
    print(f"{len_pending} artigos pendentes.\n")
    
    columns = out_df.columns.to_list()
    columns = [col for col in columns if col not in ["Titulo", "Fonte","Status","Anotation","Autores","Ano de Publicacao"]]
    columns1 = columns[:7]
    columns2 = columns[-4:]
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
        responseList = []
        responseList2 = []
        status, responseList, new_anotation = ask_user(len_pending, title, source, status, eeg, bci, mi, classification, model_pipeline, temporal_filter, anotation, columns1)
        len_pending -= 1
        if status == "sim":
            responseList2 = second_ask_user(title, columns2)
        else:
            responseList2 = ["-"] * 4
        new_row = ref_df.loc[ref_df["Titulo"] == title].iloc[0].to_dict()

        new_row["Status"] = status
        new_row["Anotation"] = new_anotation
        new_row["Review_Survey"] = responseList[0]
        new_row["EEG"] = responseList[1]
        new_row["BCI"] = responseList[2]
        new_row["MI"] = responseList[3]
        new_row["Classification"] = responseList[4]
        new_row["Model/pipeline"] = responseList[5]
        new_row["Temporal_filter"] = responseList[6]
        new_row["Objective"] = responseList2[0]
        new_row["Model_used"] = responseList2[1]
        new_row["Temporal_filters_used"] = responseList2[2]
        new_row["Datasets_used"] = responseList2[3]
  
        new_row = pd.DataFrame([new_row])
  
        out_df = pd.concat([out_df, new_row], ignore_index=True)

        save_progress(out_df)

    print("\n✔ Todos os artigos foram processados!")

if __name__ == "__main__":
    main()