import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random

# --- Configuração da Página ---
st.set_page_config(page_title="Minha Rotina", page_icon="📅", layout="wide")

# --- Estilo CSS Customizado ---
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
    /* Estilo para os itens da lista de compromissos e tarefas */
    .item-container {
        padding: 8px;
        border-left: 4px solid #007BFF;
        margin-bottom: 8px;
        background-color: #f0f2f6;
        border-radius: 4px;
    }
    /* Estilo para a Frase do Dia */
    .quote-container {
        padding: 1rem;
        background-color: #e6f3ff;
        border-left: 5px solid #007BFF;
        border-radius: 5px;
        margin-bottom: 1rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)


# --- Arquivos para armazenar dados ---
AULAS_CSV = "aulas.csv"
EVENTOS_CSV = "eventos.csv"
HABITOS_CSV = "habitos.csv"
TAREFAS_CSV = "tarefas_semanais.csv"
COMPRAS_CSV = "lista_compras.csv"

# --- Lista de Frases do Dia ---
FRASES = [
    "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
    "Comece onde você está. Use o que você tem. Faça o que você pode.",
    "Acredite em você mesmo e tudo será possível.",
    "O único lugar onde o sucesso vem antes do trabalho é no dicionário.",
    "A persistência realiza o impossível."
]

# --- Função para carregar CSV ---
def carregar_csv(caminho, colunas):
    """Carrega um arquivo CSV. Se não existir, cria um DataFrame vazio."""
    if not os.path.exists(caminho):
        return pd.DataFrame(columns=colunas)
    df = pd.read_csv(caminho)
    for col in colunas:
        if col not in df.columns:
            df[col] = False if col == 'comprado' else ''
    return df

# --- Inicializar dataframes ---
colunas_habitos = ["data", "agua", "exercicio", "hobby", "leitura", "meditacao"]
df_aulas = carregar_csv(AULAS_CSV, ["dia", "hora_inicio", "hora_fim", "disciplina", "sala"])
df_eventos = carregar_csv(EVENTOS_CSV, ["data", "tipo", "titulo", "descricao"])
df_habitos = carregar_csv(HABITOS_CSV, colunas_habitos)
df_tarefas = carregar_csv(TAREFAS_CSV, ["dia_semana", "tarefa"])
df_compras = carregar_csv(COMPRAS_CSV, ["item", "comprado"])

# --- Menu lateral ---
menu = st.sidebar.radio("Menu", ["Hoje", "Cadastrar Aulas", "Cadastrar Evento", "Organizar Tarefas da Casa", "Lista de Compras"])

# ==========================================================
# PÁGINA "HOJE"
# ==========================================================
if menu == "Hoje":
    st.title("📅 Minha Rotina")

    hoje_dt = datetime.now()
    hoje_str = hoje_dt.strftime("%Y-%m-%d")
    dia_semana_en = hoje_dt.strftime("%A")

    dias_pt = {
        "Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"
    }
    dia_semana_pt = dias_pt.get(dia_semana_en, dia_semana_en)

    st.header(f"Resumo de hoje: {dia_semana_pt}, {hoje_dt.strftime('%d/%m/%Y')}")

    # Frase do Dia
    semente_diaria = hoje_dt.day + hoje_dt.month + hoje_dt.year
    random.seed(semente_diaria)
    frase_escolhida = random.choice(FRASES)
    st.markdown(f'<div class="quote-container">"{frase_escolhida}"</div>', unsafe_allow_html=True)

    # Aulas de Hoje
    aulas_hoje = df_aulas[df_aulas["dia"] == dia_semana_en].sort_values("hora_inicio")
    if not aulas_hoje.empty:
        with st.expander("📚 Suas Aulas de Hoje", expanded=True):
            for _, aula in aulas_hoje.iterrows():
                st.markdown(f"- **{aula['hora_inicio']} - {aula['hora_fim']}:** Aula de **{aula['disciplina']}** na sala **{aula['sala']}**.")
    
    # Compromissos de Hoje
    eventos_hoje = df_eventos[df_eventos["data"] == hoje_str]
    if not eventos_hoje.empty:
        with st.expander("🗓️ Seus Compromissos de Hoje", expanded=True):
            icones_tipo = {"Prova": "📝", "Trabalho": "💼", "Consulta": "🩺", "Estudo": "📚", "Lembrete": "📌"}
            for _, evento in eventos_hoje.iterrows():
                icone = icones_tipo.get(evento['tipo'], "🔔")
                st.markdown(f"""<div class="item-container">{icone} **{evento['tipo']}: {evento['titulo']}** <br><small>{evento['descricao']}</small></div>""", unsafe_allow_html=True)

    # Tarefas da Casa de Hoje
    tarefas_de_hoje = df_tarefas[df_tarefas['dia_semana'] == dia_semana_en]
    if not tarefas_de_hoje.empty:
        with st.expander("🏠 Tarefas da Casa", expanded=True):
            for _, tarefa in tarefas_de_hoje.iterrows():
                texto_tarefa = f"🧹 **Hoje é dia de:** {tarefa['tarefa']}"
                if "feira" in tarefa['tarefa'].lower() or "compras" in tarefa['tarefa'].lower():
                    texto_tarefa += " (Não esqueça de checar a **Lista de Compras**!)"
                st.markdown(f'<div class="item-container">{texto_tarefa}</div>', unsafe_allow_html=True)

    if aulas_hoje.empty and eventos_hoje.empty and tarefas_de_hoje.empty:
        st.success("🎉 Você não tem aulas, compromissos ou tarefas agendadas para hoje. Aproveite o dia!")

    st.markdown("---")

    # Autocuidado & Hábitos
    st.subheader("💧 Autocuidado & Hábitos")
    # ... (código de hábitos permanece o mesmo) ...
    if hoje_str in df_habitos["data"].values:
        habito_hoje = df_habitos[df_habitos["data"] == hoje_str].iloc[0]
        agua, exercicio, hobby, leitura, meditacao = int(habito_hoje["agua"]), bool(habito_hoje["exercicio"]), bool(habito_hoje["hobby"]), bool(habito_hoje["leitura"]), bool(habito_hoje["meditacao"])
    else:
        agua, exercicio, hobby, leitura, meditacao = 0, False, False, False, False
    meta_agua = 2000
    copo_padrao = st.number_input("⚙️ Tamanho do copo (ml)", 50, 1000, 250, 50)
    c1, c2, c3 = st.columns(3)
    if c1.button(f"💧 Beber 1 copo (+{copo_padrao} ml)"): agua += copo_padrao
    if c2.button("🥤 Beber 500 ml"): agua += 500
    if c3.button("🍼 Beber 1 garrafa (1000 ml)"): agua += 1000
    st.progress(min(1.0, agua / meta_agua))
    st.write(f"Você já bebeu **{agua} ml** de água hoje. Meta: **{meta_agua} ml**")
    st.markdown("##### O que mais você fez por você hoje?")
    exercicio_check = st.checkbox("✅ Fiz exercício", value=exercicio)
    leitura_check = st.checkbox("📖 Fiz uma leitura", value=leitura)
    meditacao_check = st.checkbox("🧘‍♀️ Meditei", value=meditacao)
    hobby_check = st.checkbox("🎸 Pratiquei um hobby", value=hobby)
    if st.button("Salvar Autocuidado & Hábitos"):
        df_habitos = df_habitos[df_habitos["data"] != hoje_str]
        novo_habito = pd.DataFrame([[hoje_str, agua, exercicio_check, hobby_check, leitura_check, meditacao_check]], columns=colunas_habitos)
        df_habitos = pd.concat([df_habitos, novo_habito], ignore_index=True)
        df_habitos.to_csv(HABITOS_CSV, index=False)
        st.toast("Seus hábitos foram salvos!", icon="🎉")

# ==========================================================
# PÁGINAS DE CADASTRO
# ==========================================================
elif menu == "Cadastrar Aulas":
    st.title("📚 Cadastrar Aulas")
    # ... (código de cadastro de aulas permanece o mesmo) ...
    with st.form("form_aulas", clear_on_submit=True):
        dias_semana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        dia = st.selectbox("Dia da semana", dias_semana)
        hora_inicio = st.text_input("Hora início (HH:MM)", "07:10")
        hora_fim = st.text_input("Hora fim (HH:MM)", "08:00")
        disciplina = st.text_input("Disciplina")
        sala = st.text_input("Sala")
        if st.form_submit_button("Salvar Aula"):
            nova = pd.DataFrame([[dia, hora_inicio, hora_fim, disciplina, sala]], columns=["dia", "hora_inicio", "hora_fim", "disciplina", "sala"])
            df_aulas = pd.concat([df_aulas, nova], ignore_index=True)
            df_aulas.to_csv(AULAS_CSV, index=False)
            st.toast("Aula cadastrada!", icon="✅")
    st.markdown("### Aulas Cadastradas"); st.dataframe(df_aulas)

elif menu == "Cadastrar Evento":
    st.title("🗓️ Cadastrar Novo Evento")
    # ... (código de cadastro de evento permanece o mesmo) ...
    with st.form("form_eventos", clear_on_submit=True):
        data = st.date_input("Data do Evento")
        tipo = st.selectbox("Tipo de Evento", ["Prova", "Trabalho", "Consulta", "Estudo", "Lembrete"])
        titulo = st.text_input("Título (Ex: Prova de Cálculo, Dentista)")
        descricao = st.text_area("Descrição (Opcional)")
        if st.form_submit_button("Salvar Evento"):
            nova = pd.DataFrame([[data.strftime("%Y-%m-%d"), tipo, titulo, descricao]], columns=["data", "tipo", "titulo", "descricao"])
            df_eventos = pd.concat([df_eventos, nova], ignore_index=True)
            df_eventos.to_csv(EVENTOS_CSV, index=False)
            st.toast("Evento salvo!", icon="✅")
    st.markdown("### Eventos Cadastrados"); st.dataframe(df_eventos)

# ==========================================================
# PÁGINA "ORGANIZAR TAREFAS DA CASA"
# ==========================================================
elif menu == "Organizar Tarefas da Casa":
    st.title("🏠 Organizar Tarefas da Semana")
    with st.form("form_tarefas", clear_on_submit=True):
        dias_semana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dia = st.selectbox("Selecione o dia da semana", dias_semana)
        tarefa = st.text_input("Qual tarefa você quer agendar?", placeholder="Ex: Lavar roupa, Fazer feira, Spa Day")
        if st.form_submit_button("Agendar Tarefa"):
            if tarefa:
                nova_tarefa = pd.DataFrame([[dia, tarefa]], columns=["dia_semana", "tarefa"])
                df_tarefas = pd.concat([df_tarefas, nova_tarefa], ignore_index=True)
                df_tarefas.to_csv(TAREFAS_CSV, index=False)
                st.toast(f'Tarefa "{tarefa}" agendada para toda {dias_pt.get(dia, dia)}!', icon="👍")
    st.markdown("### Seu Cronograma de Tarefas")
    st.dataframe(df_tarefas)

# ==========================================================
# PÁGINA "LISTA DE COMPRAS"
# ==========================================================
elif menu == "Lista de Compras":
    st.title("🛒 Lista de Compras")
    with st.form("form_compras", clear_on_submit=True):
        item = st.text_input("Adicionar item à lista")
        if st.form_submit_button("Adicionar"):
            if item:
                novo_item = pd.DataFrame([[item, False]], columns=["item", "comprado"])
                df_compras = pd.concat([df_compras, novo_item], ignore_index=True)
                df_compras.to_csv(COMPRAS_CSV, index=False)
                st.toast(f'"{item}" adicionado à lista!', icon="➕")

    st.markdown("### Itens para comprar:")
    
    # Itera sobre o dataframe para criar os checkboxes
    for index, row in df_compras.iterrows():
        comprado = st.checkbox(row["item"], value=bool(row["comprado"]), key=f"item_{index}")
        # Se o estado do checkbox mudou, atualiza o dataframe
        if comprado != bool(row["comprado"]):
            df_compras.at[index, "comprado"] = comprado
            df_compras.to_csv(COMPRAS_CSV, index=False)
            st.rerun() # Recarrega a página para refletir a mudança

    if not df_compras.empty and st.button("Limpar itens comprados"):
        df_compras = df_compras[df_compras["comprado"] == False]
        df_compras.to_csv(COMPRAS_CSV, index=False)
        st.toast("Lista limpa!", icon="🗑️")
        st.rerun()
