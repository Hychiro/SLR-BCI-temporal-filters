import pandas as pd
import os
import ast
import numpy as np

# ============================================================
# CAMINHOS
# ============================================================

path_accuracy = r"C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/results/filtro_accuracy.csv"

path_f1 = r"C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/results/filtro_f1_score.csv"

path_kappa = r"C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/results/filtro_kappa.csv"

# arquivo onde o progresso será salvo
path_progresso = r"C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/results/progresso_metricas.csv"

# arquivo final
path_saida = r"C:/Users/Hychiro/Documents/Mestrado/Mestrado/Mestrado/Review/SLR-BCI-temporal-filters/results/resultados_filtros_metricas.csv"

# ============================================================
# FUNÇÃO PARA CONVERTER TEXTO DO CSV EM NUMPY ARRAY
# ============================================================

def string_para_array(valor):

    if isinstance(valor, np.ndarray):
        return valor

    valor = str(valor).strip()

    # Remove [ ]
    valor = valor.strip("[]")

    if valor == "":
        return np.array([], dtype=float)

    return np.array(
        [float(v.strip()) for v in valor.split(",")],
        dtype=float
    )


# ============================================================
# LEITURA DOS DATASETS
# ============================================================

df_accuracy = pd.read_csv(path_accuracy)
df_f1 = pd.read_csv(path_f1)
df_kappa = pd.read_csv(path_kappa)

df_accuracy["Metric"] = "Accuracy"
df_f1["Metric"] = "F1-score"
df_kappa["Metric"] = "Kappa"

df_todos = pd.concat(
    [df_accuracy, df_f1, df_kappa],
    ignore_index=True
)


# ============================================================
# NORMALIZAÇÃO
# ============================================================

df_todos["Titulo"] = (
    df_todos["Titulo"]
    .astype(str)
    .str.strip()
)

df_todos["Filter_type"] = (
    df_todos["Filter_type"]
    .astype(str)
    .str.strip()
)

df_todos = df_todos[
    (df_todos["Titulo"] != "") &
    (df_todos["Titulo"].str.lower() != "nan")
].copy()


# ============================================================
# ORDENAÇÃO
# ============================================================

df_todos = df_todos.sort_values(
    "Titulo",
    key=lambda x: x.str.lower()
).reset_index(drop=True)


# ============================================================
# CARREGA PROGRESSO ANTERIOR
# ============================================================

if os.path.exists(path_progresso):

    progresso = pd.read_csv(path_progresso)

    # Recupera a coluna Valor como numpy array
    progresso["Valor"] = progresso["Valor"].apply(
        string_para_array
    )

    print("\n==============================================")
    print("PROGRESSO ANTERIOR ENCONTRADO")
    print("==============================================")
    print(f"Registros já preenchidos: {len(progresso)}")
    print("Continuando de onde você parou...\n")

else:

    progresso = pd.DataFrame(
        columns=[
            "Titulo",
            "Filter_type",
            "Metric",
            "Valor"
        ]
    )

    print("\nNenhum progresso anterior encontrado.")
    print("Iniciando novo preenchimento.\n")


# ============================================================
# FUNÇÃO PARA SALVAR PROGRESSO
# ============================================================

def salvar_progresso(progresso):

    # O CSV não possui tipo numpy array.
    # Portanto, convertemos temporariamente para string.

    progresso_csv = progresso.copy()

    progresso_csv["Valor"] = progresso_csv["Valor"].apply(
        lambda x: np.array2string(
            x,
            separator=", ",
            precision=15
        )
    )

    progresso_csv.to_csv(
        path_progresso,
        index=False,
        encoding="utf-8-sig"
    )


# ============================================================
# PROCESSAMENTO
# ============================================================

for _, linha in df_todos.iterrows():

    titulo = linha["Titulo"]
    metodo = linha["Filter_type"]
    metrica = linha["Metric"]

    # --------------------------------------------------------
    # Verifica se já foi preenchido
    # --------------------------------------------------------

    ja_preenchido = (
        (progresso["Titulo"] == titulo) &
        (progresso["Filter_type"] == metodo) &
        (progresso["Metric"] == metrica)
    ).any()

    if ja_preenchido:
        continue


    # --------------------------------------------------------
    # Mostra artigo
    # --------------------------------------------------------

    print("\n==============================================")
    print(f"Faltam preencher {len(df_todos) - len(progresso)} registros.")
    print(f"Artigo: {titulo}")
    print(f"Método: {metodo}")
    print(f"Métrica: {metrica}")
    print("==============================================")


    try:

        entrada = input(
            "Digite o melhor valor para o metodo apresentado para cada dataset (separados por vírgula)"
            "(ENTER para pular): "
        ).strip()

    except KeyboardInterrupt:

        print("\n\n==============================================")
        print("EXECUÇÃO INTERROMPIDA")
        print("==============================================")
        print("Todo o progresso anterior já foi salvo.")
        print(f"Arquivo: {path_progresso}")

        break


    # --------------------------------------------------------
    # ENTER = pular
    # --------------------------------------------------------

    if entrada == "":
        continue


    # --------------------------------------------------------
    # CONVERTE INPUT PARA NUMPY ARRAY
    # --------------------------------------------------------

    try:

        valores = np.array(
            [
                float(v.strip())
                for v in entrada.split(",")
                if v.strip() != ""
            ],
            dtype=float
        )

        if valores.size == 0:
            raise ValueError

    except ValueError:

        print("\nValor inválido.")
        print("Digite os valores separados por vírgula.")
        print("Exemplo:")
        print("75.365, 80.291")
        print("O artigo não foi salvo.")

        continue


    # --------------------------------------------------------
    # MOSTRA O ARRAY
    # --------------------------------------------------------

    print("\nArray registrado:")
    print(valores)

    print("Tipo:")
    print(type(valores))


    # --------------------------------------------------------
    # SALVA NOVO REGISTRO
    # --------------------------------------------------------

    novo_registro = pd.DataFrame({
        "Titulo": [titulo],
        "Filter_type": [metodo],
        "Metric": [metrica],
        "Valor": [valores]
    })

    progresso = pd.concat(
        [progresso, novo_registro],
        ignore_index=True
    )


    # --------------------------------------------------------
    # SALVA IMEDIATAMENTE
    # --------------------------------------------------------

    salvar_progresso(progresso)

    print("✓ Resultado salvo.")


# ============================================================
# CONSTRÓI DATASET FINAL
# ============================================================

if len(progresso) > 0:

    resultados = {}

    for _, linha in progresso.iterrows():

        metodo = linha["Filter_type"]
        metrica = linha["Metric"]

        # Já é numpy array
        valor = linha["Valor"]

        if metodo not in resultados:

            resultados[metodo] = {
                "Accuracy": [],
                "F1-score": [],
                "Kappa": []
            }

        # Adiciona os valores do array
        resultados[metodo][metrica].extend(valor.tolist())


    # --------------------------------------------------------
    # DATAFRAME FINAL
    # --------------------------------------------------------

    df_resultados = pd.DataFrame.from_dict(
        resultados,
        orient="index"
    )

    df_resultados.index.name = "Filter_type"

    df_resultados = df_resultados.reset_index()


    # --------------------------------------------------------
    # CONVERTE LISTAS PARA ARRAY
    # --------------------------------------------------------

    for coluna in ["Accuracy", "F1-score", "Kappa"]:

        df_resultados[coluna] = df_resultados[coluna].apply(
            lambda x: np.array(x, dtype=float)
        )


    # --------------------------------------------------------
    # MOSTRA RESULTADO
    # --------------------------------------------------------

    print("\n==============================================")
    print("DATASET FINAL ATUALIZADO")
    print("==============================================")

    print(df_resultados)

    print("\nExemplo de acesso:")

    if len(df_resultados) > 0:

        array = df_resultados.iloc[0]["Accuracy"]

        print(array)
        print(type(array))


    # --------------------------------------------------------
    # SALVA DATASET FINAL
    # --------------------------------------------------------

    df_resultados_csv = df_resultados.copy()

    for coluna in ["Accuracy", "F1-score", "Kappa"]:

        df_resultados_csv[coluna] = (
            df_resultados_csv[coluna]
            .apply(
                lambda x: np.array2string(
                    x,
                    separator=", ",
                    precision=15
                )
            )
        )

    df_resultados_csv.to_csv(
        path_saida,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nArquivo final salvo em:")
    print(path_saida)

else:

    print("\nNenhum resultado foi preenchido.")