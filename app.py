import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Configuração da Página ---
st.set_page_config(page_title="Minha Rotina", page_icon="📅", layout="wide")

# --- Estilo CSS Customizado ---
# Injetamos um pouco de CSS para melhorar a aparência dos botões e expanders.
st.markdown("""
<style>
    /* Estilo para os botões */
    .stButton > button {
        border-radius: 12px;
        border: 2px solid #007BFF;
        color: #007BFF;
        background-color: transparent;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        border-color: #0056b3;
        color: white;
        background-color: #007BFF;
    }
    /* Aumenta o tamanho da fonte nos cabeçalhos dos expanders */
    .st-expander header {
        font-size: 1.25rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# --- Arquivos para armazenar dados ---
AULAS_CSV = "aulas.csv"
ATIVIDADES_CSV = "atividades.csv"
HABITOS_CSV = "habitos.csv"
LEMBRETES_CSV = "lembretes.csv"

# --- Função para carregar CSV ---
def carregar_csv(caminho, colunas):
    """Carrega um arquivo CSV. Se não existir, cria um DataFrame vazio."""
    if not os.path.exists(caminho):
        return pd.DataFrame(columns=colunas)
    return pd.read_csv(caminho)

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
    st.title("📅 Minha Rotina")

    hoje_dt = datetime.now()
    hoje_str = hoje_dt.strftime("%Y-%m-%d")
    dia_semana_en = hoje_dt.strftime("%A") # English day name

    # Dicionário para traduzir o dia da semana
    dias_pt = {
        "Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    dia_semana_pt = dias_pt.get(dia_semana_en, dia_semana_en)

    st.subheader(f"Hoje é {dia_semana_pt}, {hoje_dt.strftime('%d/%m/%Y')}")

    # --- Seções com Expanders para melhor visualização no celular ---
    with st.expander("📚 Aulas de Hoje", expanded=True):
        aulas_hoje = df_aulas[df_aulas["dia"] == dia_semana_en].sort_values("hora_inicio")
        if aulas_hoje.empty:
            st.info("Nenhuma aula cadastrada para hoje.")
        else:
            st.table(aulas_hoje[["hora_inicio", "hora_fim", "disciplina", "sala"]])

    with st.expander("📝 Atividades Avaliativas", expanded=True):
        atividades_hoje = df_atividades[df_atividades["data"] == hoje_str]
        if atividades_hoje.empty:
            st.info("Nenhuma atividade para hoje.")
        else:
            st.table(atividades_hoje[["disciplina", "descricao"]])

    with st.expander("📌 Lembretes / Consultas"):
        lembretes_hoje = df_lembretes[df_lembretes["data"] == hoje_str]
        if lembretes_hoje.empty:
            st.info("Nenhum lembrete para hoje.")
        else:
            st.table(lembretes_hoje[["descricao"]])

    st.markdown("---") # Linha divisória

    # --- Hábitos ---
    st.subheader("💧 Hábitos do Dia")

    # Carregar ou inicializar os hábitos de hoje
    if hoje_str in df_habitos["data"].values:
        habito_hoje = df_habitos[df_habitos["data"] == hoje_str].iloc[0]
        agua = int(habito_hoje["agua"])
        exercicio = bool(habito_hoje["exercicio"])
        hobby = bool(habito_hoje["hobby"])
        leitura = bool(habito_hoje["leitura"])
    else:
        agua, exercicio, hobby, leitura = 0, False, False, False

    # Configuração da meta e copo
    meta_agua = 2000  # meta diária em ml
    copo_padrao = st.number_input("⚙️ Tamanho do copo (ml)", min_value=50, max_value=1000, value=250, step=50)

    col1, col2, col3 = st.columns(3)
    if col1.button(f"💧 Beber 1 copo (+{copo_padrao} ml)"):
        agua += copo_padrao
    if col2.button("🥤 Beber 500 ml"):
        agua += 500
    if col3.button("🍼 Beber 1 garrafa (1000 ml)"): # Ajustado para 1000ml para ser mais realista
        agua += 1000

    # Atualiza o DataFrame de hábitos em tempo real após clicar nos botões de água
    df_habitos = df_habitos[df_habitos["data"] != hoje_str]
    novo_habito = pd.DataFrame([[hoje_str, agua, exercicio, hobby, leitura]],
                               columns=["data", "agua", "exercicio", "hobby", "leitura"])
    df_habitos = pd.concat([df_habitos, novo_habito], ignore_index=True)
    df_habitos.to_csv(HABITOS_CSV, index=False)


    # Exibição do total de água
    st.progress(min(1.0, agua / meta_agua))
    st.write(f"Você já bebeu **{agua} ml** de água hoje. Meta: **{meta_agua} ml**")

    # Outros hábitos
    st.markdown("##### Outros Hábitos:")
    exercicio_check = st.checkbox("✅ Fiz exercício", value=exercicio)
    hobby_check = st.checkbox("🎸 Fiz hobby/violão", value=hobby)
    leitura_check = st.checkbox("📖 Fiz leitura", value=leitura)

    # Botão para salvar explicitamente (opcional, mas bom para confirmar)
    if st.button("Salvar Hábitos"):
        df_habitos = df_habitos[df_habitos["data"] != hoje_str]
        novo_habito_final = pd.DataFrame([[hoje_str, agua, exercicio_check, hobby_check, leitura_check]],
                                         columns=["data", "agua", "exercicio", "hobby", "leitura"])
        df_habitos = pd.concat([df_habitos, novo_habito_final], ignore_index=True)
        df_habitos.to_csv(HABITOS_CSV, index=False)
        st.toast("Hábitos salvos com sucesso!", icon="🎉")


# ==========================================================
# PÁGINA "CADASTRAR AULAS"
# ==========================================================
elif menu == "Cadastrar Aulas":
    st.title("📚 Cadastrar Aulas")

    with st.form("form_aulas", clear_on_submit=True):
        dias_semana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        dia = st.selectbox("Dia da semana", dias_semana)
        hora_inicio = st.text_input("Hora início (HH:MM)", "07:10")
        hora_fim = st.text_input("Hora fim (HH:MM)", "08:00")
        disciplina = st.text_input("Disciplina")
        sala = st.text_input("Sala")
        submitted = st.form_submit_button("Salvar Aula")

        if submitted:
            nova = pd.DataFrame([[dia, hora_inicio, hora_fim, disciplina, sala]],
                                columns=["dia", "hora_inicio", "hora_fim", "disciplina", "sala"])
            df_aulas = pd.concat([df_aulas, nova], ignore_index=True)
            df_aulas.to_csv(AULAS_CSV, index=False)
            st.toast("Aula cadastrada!", icon="✅")

    st.markdown("### Aulas Cadastradas")
    st.dataframe(df_aulas)

# ==========================================================
# PÁGINA "CADASTRAR ATIVIDADE"
# ==========================================================
elif menu == "Cadastrar Atividade":
    st.title("📝 Cadastrar Atividade Avaliativa")

    with st.form("form_atividades", clear_on_submit=True):
        data = st.date_input("Data")
        disciplina = st.text_input("Disciplina")
        descricao = st.text_area("Descrição")
        submitted = st.form_submit_button("Salvar Atividade")

        if submitted:
            nova = pd.DataFrame([[data.strftime("%Y-%m-%d"), disciplina, descricao]],
                                columns=["data", "disciplina", "descricao"])
            df_atividades = pd.concat([df_atividades, nova], ignore_index=True)
            df_atividades.to_csv(ATIVIDADES_CSV, index=False)
            st.toast("Atividade salva!", icon="✅")

    st.markdown("### Atividades Cadastradas")
    st.dataframe(df_atividades)

# ==========================================================
# PÁGINA "CADASTRAR LEMBRETE"
# ==========================================================
elif menu == "Cadastrar Lembrete":
    st.title("📌 Cadastrar Lembrete / Consulta")

    with st.form("form_lembretes", clear_on_submit=True):
        data = st.date_input("Data")
        descricao = st.text_area("Descrição do lembrete")
        submitted = st.form_submit_button("Salvar Lembrete")

        if submitted:
            nova = pd.DataFrame([[data.strftime("%Y-%m-%d"), descricao]],
                                columns=["data", "descricao"])
            df_lembretes = pd.concat([df_lembretes, nova], ignore_index=True)
            df_lembretes.to_csv(LEMBRETES_CSV, index=False)
            st.toast("Lembrete salvo!", icon="✅")

    st.markdown("### Lembretes Cadastrados")
    st.dataframe(df_lembretes)
