import streamlit as st
import pandas as pd
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(page_title="Minha Rotina", page_icon="📅", layout="wide")

# --- Arquivos para armazenar dados ---
AULAS_CSV = "aulas.csv"
ATIVIDADES_CSV = "atividades.csv"
HABITOS_CSV = "habitos.csv"
LEMBRETES_CSV = "lembretes.csv"

# --- Função para carregar CSV ---
def carregar_csv(caminho, colunas):
    try:
        return pd.read_csv(caminho)
    except FileNotFoundError:
        return pd.DataFrame(columns=colunas)

# --- Inicializar dataframes ---
df_aulas = carregar_csv(AULAS_CSV, ["dia", "hora_inicio", "hora_fim", "disciplina", "sala"])
df_atividades = carregar_csv(ATIVIDADES_CSV, ["data", "disciplina", "descricao"])
df_habitos = carregar_csv(HABITOS_CSV, ["data", "agua", "exercicio", "hobby", "leitura"])
df_lembretes = carregar_csv(LEMBRETES_CSV, ["data", "descricao"])

# --- Menu lateral ---
menu = st.sidebar.radio("Menu", ["Hoje", "Cadastrar Aulas", "Cadastrar Atividade", "Cadastrar Lembrete"])

# ==========================================================
# PÁGINA "HOJE"
# ==========================================================
if menu == "Hoje":
    st.title("📅 Rotina de Hoje")

    hoje = datetime.now().strftime("%Y-%m-%d")
    dia_semana = datetime.now().strftime("%A")  # exemplo: Monday, Tuesday

    st.subheader(f"Hoje é {dia_semana}, {hoje}")

    # --- Mostrar aulas de hoje ---
    st.markdown("### 📚 Aulas de Hoje")
    aulas_hoje = df_aulas[df_aulas["dia"] == dia_semana]
    if aulas_hoje.empty:
        st.info("Nenhuma aula cadastrada para hoje.")
    else:
        st.table(aulas_hoje[["hora_inicio", "hora_fim", "disciplina", "sala"]])

    # --- Mostrar atividades avaliativas ---
    st.markdown("### 📝 Atividades Avaliativas")
    atividades_hoje = df_atividades[df_atividades["data"] == hoje]
    if atividades_hoje.empty:
        st.info("Nenhuma atividade para hoje.")
    else:
        st.table(atividades_hoje[["disciplina", "descricao"]])

    # --- Mostrar lembretes ---
    st.markdown("### 📌 Lembretes / Consultas")
    lembretes_hoje = df_lembretes[df_lembretes["data"] == hoje]
    if lembretes_hoje.empty:
        st.info("Nenhum lembrete para hoje.")
    else:
        st.table(lembretes_hoje[["descricao"]])

    # --- Hábitos ---
    st.markdown("### 💧 Hábitos do Dia")

    if hoje in df_habitos["data"].values:
        habito_hoje = df_habitos[df_habitos["data"] == hoje].iloc[0]
        agua = habito_hoje["agua"]
        exercicio = bool(habito_hoje["exercicio"])
        hobby = bool(habito_hoje["hobby"])
        leitura = bool(habito_hoje["leitura"])
    else:
        agua, exercicio, hobby, leitura = 0, False, False, False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💧 Beber 1 copo de água"):
            agua += 1
    st.write(f"Copos de água hoje: {agua}")

    exercicio = st.checkbox("✅ Fiz exercício", value=exercicio)
    hobby = st.checkbox("🎸 Fiz hobby/violão", value=hobby)
    leitura = st.checkbox("📖 Fiz leitura", value=leitura)

    if st.button("Salvar hábitos de hoje"):
        df_habitos = df_habitos[df_habitos["data"] != hoje]
        novo = pd.DataFrame([[hoje, agua, exercicio, hobby, leitura]],
                            columns=["data", "agua", "exercicio", "hobby", "leitura"])
        df_habitos = pd.concat([df_habitos, novo], ignore_index=True)
        df_habitos.to_csv(HABITOS_CSV, index=False)
        st.success("Hábitos salvos!")

# ==========================================================
# PÁGINA "CADASTRAR AULAS"
# ==========================================================
elif menu == "Cadastrar Aulas":
    st.title("📚 Cadastrar Aulas")

    dias_semana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    dia = st.selectbox("Dia da semana", dias_semana)
    hora_inicio = st.text_input("Hora início (HH:MM)", "07:10")
    hora_fim = st.text_input("Hora fim (HH:MM)", "08:00")
    disciplina = st.text_input("Disciplina")
    sala = st.text_input("Sala")

    if st.button("Salvar Aula"):
        nova = pd.DataFrame([[dia, hora_inicio, hora_fim, disciplina, sala]],
                            columns=["dia", "hora_inicio", "hora_fim", "disciplina", "sala"])
        df_aulas = pd.concat([df_aulas, nova], ignore_index=True)
        df_aulas.to_csv(AULAS_CSV, index=False)
        st.success("Aula cadastrada!")

    st.dataframe(df_aulas)

# ==========================================================
# PÁGINA "CADASTRAR ATIVIDADE"
# ==========================================================
elif menu == "Cadastrar Atividade":
    st.title("📝 Cadastrar Atividade Avaliativa")

    data = st.date_input("Data")
    disciplina = st.text_input("Disciplina")
    descricao = st.text_area("Descrição")

    if st.button("Salvar Atividade"):
        nova = pd.DataFrame([[data.strftime("%Y-%m-%d"), disciplina, descricao]],
                            columns=["data", "disciplina", "descricao"])
        df_atividades = pd.concat([df_atividades, nova], ignore_index=True)
        df_atividades.to_csv(ATIVIDADES_CSV, index=False)
        st.success("Atividade salva!")

    st.dataframe(df_atividades)

# ==========================================================
# PÁGINA "CADASTRAR LEMBRETE"
# ==========================================================
elif menu == "Cadastrar Lembrete":
    st.title("📌 Cadastrar Lembrete / Consulta")

    data = st.date_input("Data")
    descricao = st.text_area("Descrição do lembrete")

    if st.button("Salvar Lembrete"):
        nova = pd.DataFrame([[data.strftime("%Y-%m-%d"), descricao]],
                            columns=["data", "descricao"])
        df_lembretes = pd.concat([df_lembretes, nova], ignore_index=True)
        df_lembretes.to_csv(LEMBRETES_CSV, index=False)
        st.success("Lembrete salvo!")

    st.dataframe(df_lembretes)
