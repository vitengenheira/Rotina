import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import random
import base64
from streamlit_calendar import calendar

# --- Configuração da Página ---
st.set_page_config(page_title="Minha Rotina", page_icon="🧘‍♀️", layout="wide")

# --- FUNÇÃO PARA ADICIONAR IMAGEM DE FUNDO ---
def set_bg_hack(main_bg):
    main_bg_ext = "png"
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }}
         /* Efeito de vidro para o bloco principal */
         [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {{
            background-color: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 15px;
            margin-top: 2rem;
         }}
         /* Remove o fundo branco do menu lateral */
         [data-testid="stSidebar"] > div:first-child {{
             background: transparent;
         }}
         /* Estilo para os botões */
         .stButton > button {{
             border-radius: 20px;
             border: 2px solid #8A2BE2; /* Roxo azulado */
             color: #8A2BE2;
             background-color: transparent;
             transition: all 0.3s ease-in-out;
             font-weight: bold;
         }}
         .stButton > button:hover {{
             border-color: #4B0082; /* Indigo */
             color: white;
             background-color: #8A2BE2;
             transform: scale(1.05);
             box-shadow: 0 4px 15px rgba(138, 43, 226, 0.4);
         }}
         /* Aumenta o tamanho da fonte nos cabeçalhos dos expanders */
         .st-expander header {{
             font-size: 1.25rem;
             font-weight: bold;
             color: #4B0082;
         }}
         /* Estilo para os itens da lista */
         .item-container {{
             padding: 10px;
             border-left: 4px solid #9370DB; /* Roxo médio */
             margin-bottom: 8px;
             background-color: rgba(255, 255, 255, 0.7);
             border-radius: 8px;
             transition: all 0.2s ease-in-out;
         }}
         .item-container:hover {{
            transform: translateX(5px);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
         }}
         /* Estilo para a Frase do Dia */
         .quote-container {{
             padding: 1rem;
             background-color: rgba(230, 230, 250, 0.8); /* Lavanda com transparência */
             border-left: 5px solid #8A2BE2;
             border-radius: 8px;
             margin-bottom: 1rem;
             font-style: italic;
             text-align: center;
             font-size: 1.1rem;
             color: #4B0082;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

if os.path.exists("background.png"):
    set_bg_hack("background.png")

# --- Arquivos de Dados ---
AULAS_CSV = "aulas.csv"
EVENTOS_CSV = "eventos.csv"
TAREFAS_CSV = "tarefas_semanais.csv"
COMPRAS_CSV = "lista_compras.csv"
ROTINA_MATINAL_CSV = "rotina_matinal.csv"
HABITOS_CSV = "habitos.csv" # Para água e hábitos fixos
MEUS_HABITOS_CSV = "meus_habitos.csv" # Para hábitos personalizáveis
HABITOS_FEITOS_CSV = "habitos_feitos.csv" # Para marcar os hábitos personalizáveis
DIARIO_CSV = "diario.csv" # Novo arquivo para o diário

# --- Constantes e Dicionários ---
FRASES = [
    "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
    "Comece onde você está. Use o que você tem. Faça o que você pode.",
    "Acredite em você mesmo e tudo será possível."
]
DIAS_PT = {
    "Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira",
    "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"
}

# --- Funções Auxiliares ---
def carregar_csv(caminho, colunas):
    if not os.path.exists(caminho):
        return pd.DataFrame(columns=colunas)
    df = pd.read_csv(caminho)
    for col in colunas:
        if col not in df.columns:
            df[col] = False if col != 'item' else ''
    return df

# --- Inicializar DataFrames ---
colunas_rotina_matinal = ["data", "cama_arrumada", "dentes_escovados", "rosto_lavado", "meditacao"]
colunas_habitos = ["data", "agua"] # Simplificado para apenas água
colunas_meus_habitos = ["habito"]
colunas_habitos_feitos = ["data", "habito", "feito"]
colunas_diario = ["data", "gratidao", "desafio", "aprendizado", "observacao"]

df_aulas = carregar_csv(AULAS_CSV, ["dia", "hora_inicio", "hora_fim", "disciplina", "sala"])
df_eventos = carregar_csv(EVENTOS_CSV, ["data", "tipo", "titulo", "descricao"])
df_tarefas = carregar_csv(TAREFAS_CSV, ["dia_semana", "tarefa"])
df_compras = carregar_csv(COMPRAS_CSV, ["item", "comprado"])
df_rotina_matinal = carregar_csv(ROTINA_MATINAL_CSV, colunas_rotina_matinal)
df_habitos = carregar_csv(HABITOS_CSV, colunas_habitos)
df_meus_habitos = carregar_csv(MEUS_HABITOS_CSV, colunas_meus_habitos)
df_habitos_feitos = carregar_csv(HABITOS_FEITOS_CSV, colunas_habitos_feitos)
df_diario = carregar_csv(DIARIO_CSV, colunas_diario)

# --- Menu Lateral ---
menu = st.sidebar.radio("Menu", ["Hoje", "Calendário e Visão Geral", "Cadastrar Aulas", "Cadastrar Evento", "Organizar Tarefas da Casa", "Lista de Compras", "Personalizar Hábitos"])

# ==========================================================
# PÁGINA "HOJE"
# ==========================================================
if menu == "Hoje":
    st.title("📅 Minha Rotina")
    hoje_dt = datetime.now()
    hoje_str = hoje_dt.strftime("%Y-%m-%d")
    dia_semana_en = hoje_dt.strftime("%A")
    dia_semana_pt = DIAS_PT.get(dia_semana_en, dia_semana_en)

    st.header(f"Resumo de hoje: {dia_semana_pt}, {hoje_dt.strftime('%d/%m/%Y')}")

    # Frase do Dia
    random.seed(hoje_dt.toordinal())
    frase_escolhida = random.choice(FRASES)
    st.markdown(f'<div class="quote-container">"{frase_escolhida}"</div>', unsafe_allow_html=True)

    # Aulas, Compromissos e Tarefas (código existente)
    aulas_hoje = df_aulas[df_aulas["dia"] == dia_semana_en].sort_values("hora_inicio")
    eventos_hoje = df_eventos[df_eventos["data"] == hoje_str]
    tarefas_de_hoje = df_tarefas[df_tarefas['dia_semana'] == dia_semana_en]

    if not aulas_hoje.empty:
        with st.expander("📚 Suas Aulas de Hoje", expanded=True):
            for _, aula in aulas_hoje.iterrows(): st.markdown(f"- **{aula['hora_inicio']} - {aula['hora_fim']}:** Aula de **{aula['disciplina']}** na sala **{aula['sala']}**.")
    if not eventos_hoje.empty:
        with st.expander("🗓️ Seus Compromissos de Hoje", expanded=True):
            icones_tipo = {"Prova": "📝", "Trabalho": "💼", "Consulta": "🩺", "Estudo": "📚", "Lembrete": "�"}
            for _, evento in eventos_hoje.iterrows(): st.markdown(f"""<div class="item-container">{icones_tipo.get(evento['tipo'], "🔔")} **{evento['tipo']}: {evento['titulo']}** <br><small>{evento['descricao']}</small></div>""", unsafe_allow_html=True)
    if not tarefas_de_hoje.empty:
        with st.expander("🏠 Tarefas da Casa", expanded=True):
            for _, tarefa in tarefas_de_hoje.iterrows(): st.markdown(f'<div class="item-container">🧹 **Hoje é dia de:** {tarefa["tarefa"]}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Autocuidado & Hábitos
    st.subheader("💧 Autocuidado & Hábitos")
    
    # Carregar dados
    agua = int(df_habitos[df_habitos["data"] == hoje_str]["agua"].iloc[0]) if hoje_str in df_habitos["data"].values else 0
    if hoje_str in df_rotina_matinal["data"].values:
        rotina_hoje = df_rotina_matinal[df_rotina_matinal["data"] == hoje_str].iloc[0]
        cama, dentes, rosto, meditacao = bool(rotina_hoje["cama_arrumada"]), bool(rotina_hoje["dentes_escovados"]), bool(rotina_hoje["rosto_lavado"]), bool(rotina_hoje["meditacao"])
    else:
        cama, dentes, rosto, meditacao = False, False, False, False

    # Rotina Matinal
    st.markdown("##### ☀️ Rotina Matinal")
    cama_check = st.checkbox("🛏️ Arrumar a cama", value=cama)
    dentes_check = st.checkbox("🦷 Escovar os dentes", value=dentes)
    rosto_check = st.checkbox("🧼 Lavar o rosto", value=rosto)
    meditacao_check = st.checkbox("🧘‍♀️ Meditar", value=meditacao)

    st.markdown("---")

    # Hábito de Beber Água
    st.markdown("##### 💧 Hábito de Beber Água")
    meta_agua = 2000
    copo_padrao = st.number_input("⚙️ Tamanho do copo (ml)", 50, 1000, 250, 50)
    c1, c2, c3 = st.columns(3)
    if c1.button(f"💧 Beber 1 copo (+{copo_padrao} ml)"): agua += copo_padrao
    if c2.button("🥤 Beber 500 ml"): agua += 500
    if c3.button("🍼 Beber 1 garrafa (1000 ml)"): agua += 1000
    st.progress(min(1.0, agua / meta_agua)); st.write(f"Você já bebeu **{agua} ml** de água hoje. Meta: **{meta_agua} ml**")

    # Demais Hábitos (Dinâmico)
    st.markdown("##### 🎨 Demais Hábitos")
    habitos_personalizados = df_meus_habitos["habito"].tolist()
    habitos_feitos_hoje = df_habitos_feitos[df_habitos_feitos["data"] == hoje_str]
    
    habitos_marcados = {}
    for habito in habitos_personalizados:
        feito = bool(habitos_feitos_hoje[habitos_feitos_hoje["habito"] == habito]["feito"].iloc[0]) if habito in habitos_feitos_hoje["habito"].values else False
        habitos_marcados[habito] = st.checkbox(habito, value=feito)

    if st.button("Salvar Autocuidado & Hábitos"):
        # Salvar rotina matinal
        df_rotina_matinal = df_rotina_matinal[df_rotina_matinal["data"] != hoje_str]
        nova_rotina = pd.DataFrame([[hoje_str, cama_check, dentes_check, rosto_check, meditacao_check]], columns=colunas_rotina_matinal)
        df_rotina_matinal = pd.concat([df_rotina_matinal, nova_rotina], ignore_index=True)
        df_rotina_matinal.to_csv(ROTINA_MATINAL_CSV, index=False)
        # Salvar água
        df_habitos = df_habitos[df_habitos["data"] != hoje_str]
        novo_habito = pd.DataFrame([[hoje_str, agua]], columns=colunas_habitos)
        df_habitos = pd.concat([df_habitos, novo_habito], ignore_index=True)
        df_habitos.to_csv(HABITOS_CSV, index=False)
        # Salvar hábitos personalizáveis
        df_habitos_feitos = df_habitos_feitos[df_habitos_feitos["data"] != hoje_str]
        for habito, feito in habitos_marcados.items():
            novo_feito = pd.DataFrame([[hoje_str, habito, feito]], columns=colunas_habitos_feitos)
            df_habitos_feitos = pd.concat([df_habitos_feitos, novo_feito], ignore_index=True)
        df_habitos_feitos.to_csv(HABITOS_FEITOS_CSV, index=False)
        st.toast("Seus hábitos foram salvos!", icon="🎉")

    st.markdown("---")

    # --- Reflexão do Dia ---
    st.subheader("📝 Reflexão do Dia")
    if hoje_str in df_diario["data"].values:
        diario_hoje = df_diario[df_diario["data"] == hoje_str].iloc[0]
        gratidao, desafio, aprendizado, obs = diario_hoje["gratidao"], diario_hoje["desafio"], diario_hoje["aprendizado"], diario_hoje["observacao"]
    else:
        gratidao, desafio, aprendizado, obs = "", "", "", ""
        
    gratidao_txt = st.text_input("Pelo que você é grato(a) hoje?", value=gratidao)
    desafio_txt = st.text_input("Qual foi o maior desafio do dia e como você lidou com ele?", value=desafio)
    aprendizado_txt = st.text_input("O que você aprendeu de novo hoje?", value=aprendizado)
    obs_txt = st.text_area("Observações gerais sobre o seu dia:", value=obs)
    
    if st.button("Salvar Reflexão do Dia"):
        df_diario = df_diario[df_diario["data"] != hoje_str]
        novo_diario = pd.DataFrame([[hoje_str, gratidao_txt, desafio_txt, aprendizado_txt, obs_txt]], columns=colunas_diario)
        df_diario = pd.concat([df_diario, novo_diario], ignore_index=True)
        df_diario.to_csv(DIARIO_CSV, index=False)
        st.toast("Sua reflexão foi salva! Volte amanhã.", icon="💖")

# ==========================================================
# PÁGINA "CALENDÁRIO"
# ==========================================================
elif menu == "Calendário e Visão Geral":
    st.title("🗓️ Calendário e Visão Geral")
    # ... (código do calendário permanece o mesmo) ...
    calendar_events = []
    cores_eventos = {"Prova": "#FF4B4B", "Trabalho": "#FFA500", "Consulta": "#1E90FF", "Estudo": "#32CD32", "Lembrete": "#9370DB"}
    for _, row in df_eventos.iterrows(): calendar_events.append({"title": f"{row['tipo']}: {row['titulo']}", "start": row["data"], "end": row["data"], "color": cores_eventos.get(row['tipo'], "#808080")})
    hoje = datetime.now()
    for i in range(60):
        data_atual = hoje + timedelta(days=i)
        dia_semana_en = data_atual.strftime("%A")
        for _, aula in df_aulas[df_aulas['dia'] == dia_semana_en].iterrows(): calendar_events.append({"title": f"Aula: {aula['disciplina']}", "start": data_atual.strftime("%Y-%m-%d"), "end": data_atual.strftime("%Y-%m-%d"), "color": "#4B0082"})
        for _, tarefa in df_tarefas[df_tarefas['dia_semana'] == dia_semana_en].iterrows(): calendar_events.append({"title": f"Casa: {tarefa['tarefa']}", "start": data_atual.strftime("%Y-%m-%d"), "end": data_atual.strftime("%Y-%m-%d"), "color": "#2E8B57"})
    calendar(events=calendar_events, options={"headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek,timeGridDay"}, "initialView": "dayGridMonth", "locale": "pt-br"})

# ==========================================================
# PÁGINAS DE CADASTRO
# ==========================================================
elif menu == "Personalizar Hábitos":
    st.title("🎨 Personalizar Hábitos")
    st.write("Adicione ou remova os hábitos que você deseja acompanhar no seu dia a dia.")
    
    with st.form("form_novo_habito", clear_on_submit=True):
        novo_habito_txt = st.text_input("Digite um novo hábito (Ex: Cuidar da pele, Ler 10 páginas)")
        if st.form_submit_button("Adicionar Hábito"):
            if novo_habito_txt and novo_habito_txt not in df_meus_habitos["habito"].values:
                novo_df = pd.DataFrame([[novo_habito_txt]], columns=colunas_meus_habitos)
                df_meus_habitos = pd.concat([df_meus_habitos, novo_df], ignore_index=True)
                df_meus_habitos.to_csv(MEUS_HABITOS_CSV, index=False)
                st.toast(f'Hábito "{novo_habito_txt}" adicionado!', icon="✨")
            else:
                st.warning("Hábito já existe ou campo está vazio.")

    st.markdown("### Seus Hábitos Atuais")
    if not df_meus_habitos.empty:
        for index, row in df_meus_habitos.iterrows():
            col1, col2 = st.columns([0.8, 0.2])
            col1.write(f"- {row['habito']}")
            if col2.button("Excluir", key=f"del_{index}"):
                df_meus_habitos.drop(index, inplace=True)
                df_meus_habitos.to_csv(MEUS_HABITOS_CSV, index=False)
                st.rerun()
    else:
        st.info("Você ainda não adicionou nenhum hábito personalizado.")


# ... (outras páginas de cadastro permanecem as mesmas) ...
elif menu == "Cadastrar Aulas":
    st.title("📚 Cadastrar Aulas")
    with st.form("form_aulas", clear_on_submit=True):
        dia_pt = st.selectbox("Dia da semana", options=list(DIAS_PT.values()))
        dia_en = [k for k, v in DIAS_PT.items() if v == dia_pt][0]
        hora_inicio, hora_fim = st.text_input("Hora de início (HH:MM)", "07:10"), st.text_input("Hora de término (HH:MM)", "08:00")
        disciplina, sala = st.text_input("Disciplina"), st.text_input("Sala")
        if st.form_submit_button("Salvar Aula"):
            nova = pd.DataFrame([[dia_en, hora_inicio, hora_fim, disciplina, sala]], columns=["dia", "hora_inicio", "hora_fim", "disciplina", "sala"])
            df_aulas = pd.concat([df_aulas, nova], ignore_index=True); df_aulas.to_csv(AULAS_CSV, index=False)
            st.toast("Aula cadastrada!", icon="✅")
    st.markdown("### Aulas Cadastradas"); st.dataframe(df_aulas)

elif menu == "Cadastrar Evento":
    st.title("🗓️ Cadastrar Novo Evento")
    with st.form("form_eventos", clear_on_submit=True):
        data = st.date_input("Data do Evento")
        tipo = st.selectbox("Tipo de Evento", ["Prova", "Trabalho", "Consulta", "Estudo", "Lembrete"])
        titulo, descricao = st.text_input("Título (Ex: Prova de Cálculo)"), st.text_area("Descrição (Opcional)")
        if st.form_submit_button("Salvar Evento"):
            nova = pd.DataFrame([[data.strftime("%Y-%m-%d"), tipo, titulo, descricao]], columns=["data", "tipo", "titulo", "descricao"])
            df_eventos = pd.concat([df_eventos, nova], ignore_index=True); df_eventos.to_csv(EVENTOS_CSV, index=False)
            st.toast("Evento salvo!", icon="✅")
    st.markdown("### Eventos Cadastrados"); st.dataframe(df_eventos)

elif menu == "Organizar Tarefas da Casa":
    st.title("🏠 Organizar Tarefas da Semana")
    with st.form("form_tarefas", clear_on_submit=True):
        dia_pt = st.selectbox("Selecione o dia da semana", options=list(DIAS_PT.values()))
        dia_en = [k for k, v in DIAS_PT.items() if v == dia_pt][0]
        tarefa = st.text_input("Qual tarefa você quer agendar?", placeholder="Ex: Lavar roupa, Fazer feira")
        if st.form_submit_button("Agendar Tarefa"):
            if tarefa:
                nova_tarefa = pd.DataFrame([[dia_en, tarefa]], columns=["dia_semana", "tarefa"])
                df_tarefas = pd.concat([df_tarefas, nova_tarefa], ignore_index=True); df_tarefas.to_csv(TAREFAS_CSV, index=False)
                st.toast(f'Tarefa "{tarefa}" agendada para toda {dia_pt}!', icon="👍")
    st.markdown("### Seu Cronograma de Tarefas"); st.dataframe(df_tarefas)

elif menu == "Lista de Compras":
    st.title("🛒 Lista de Compras")
    with st.form("form_compras", clear_on_submit=True):
        item = st.text_input("Adicionar item à lista")
        if st.form_submit_button("Adicionar"):
            if item:
                novo_item = pd.DataFrame([[item, False]], columns=["item", "comprado"])
                df_compras = pd.concat([df_compras, novo_item], ignore_index=True); df_compras.to_csv(COMPRAS_CSV, index=False)
                st.toast(f'"{item}" adicionado à lista!', icon="➕")
    st.markdown("### Itens para comprar:")
    for index, row in df_compras.iterrows():
        comprado = st.checkbox(row["item"], value=bool(row["comprado"]), key=f"item_{index}")
        if comprado != bool(row["comprado"]):
            df_compras.at[index, "comprado"] = comprado; df_compras.to_csv(COMPRAS_CSV, index=False); st.rerun()
    if not df_compras.empty and st.button("Limpar itens comprados"):
        df_compras = df_compras[df_compras["comprado"] == False]; df_compras.to_csv(COMPRAS_CSV, index=False)
        st.toast("Lista limpa!", icon="🗑️"); st.rerun()
