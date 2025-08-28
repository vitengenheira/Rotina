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
            background-color: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(12px);
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
         /* Estilo para a agenda do dia */
         .agenda-item {{
            padding: 10px;
            border-left: 4px solid #9370DB;
            margin-bottom: 8px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
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
HABITOS_CSV = "habitos.csv"
MEUS_HABITOS_CSV = "meus_habitos.csv"
HABITOS_FEITOS_CSV = "habitos_feitos.csv"
DIARIO_CSV = "diario.csv"

# --- Constantes e Dicionários ---
FRASES = ["O sucesso é a soma de pequenos esforços repetidos dia após dia.", "Comece onde você está. Use o que você tem. Faça o que você pode.", "Acredite em você mesmo e tudo será possível."]
DIAS_PT = {"Monday": "Segunda-feira", "Tuesday": "Terça-feira", "Wednesday": "Quarta-feira", "Thursday": "Quinta-feira", "Friday": "Sexta-feira", "Saturday": "Sábado", "Sunday": "Domingo"}

# --- Funções Auxiliares ---
def carregar_csv(caminho, colunas):
    if not os.path.exists(caminho):
        return pd.DataFrame(columns=colunas)
    df = pd.read_csv(caminho)
    for col in colunas:
        if col not in df.columns:
            df[col] = ''
    return df

# --- Inicializar DataFrames ---
colunas_eventos = ["data", "tipo", "titulo", "descricao", "hora_inicio", "hora_fim"]
df_aulas = carregar_csv(AULAS_CSV, ["dia", "hora_inicio", "hora_fim", "disciplina", "sala"])
df_eventos = carregar_csv(EVENTOS_CSV, colunas_eventos)
df_tarefas = carregar_csv(TAREFAS_CSV, ["dia_semana", "tarefa"])
# ... (outros dataframes)
df_compras = carregar_csv(COMPRAS_CSV, ["item", "comprado"])
df_rotina_matinal = carregar_csv(ROTINA_MATINAL_CSV, ["data", "cama_arrumada", "dentes_escovados", "rosto_lavado", "meditacao"])
df_habitos = carregar_csv(HABITOS_CSV, ["data", "agua"])
df_meus_habitos = carregar_csv(MEUS_HABITOS_CSV, ["habito"])
df_habitos_feitos = carregar_csv(HABITOS_FEITOS_CSV, ["data", "habito", "feito"])
df_diario = carregar_csv(DIARIO_CSV, ["data", "gratidao", "desafio", "aprendizado", "observacao"])


# --- Menu Lateral ---
menu = st.sidebar.radio("Menu", ["Hoje", "Calendário e Visão Geral", "Cadastrar Aulas", "Cadastrar Evento", "Organizar Tarefas da Casa", "Lista de Compras", "Personalizar Hábitos"])

# ==========================================================
# PÁGINA "HOJE" - REESTRUTURADA
# ==========================================================
if menu == "Hoje":
    st.title("📅 Minha Rotina")
    hoje_dt = datetime.now()
    hoje_str = hoje_dt.strftime("%Y-%m-%d")
    dia_semana_en = hoje_dt.strftime("%A")
    dia_semana_pt = DIAS_PT.get(dia_semana_en, dia_semana_en)

    st.header(f"Resumo de hoje: {dia_semana_pt}, {hoje_dt.strftime('%d/%m/%Y')}")

    random.seed(hoje_dt.toordinal())
    st.markdown(f'<div class="quote-container">"{random.choice(FRASES)}"</div>', unsafe_allow_html=True)

    # --- Montando a Agenda do Dia ---
    agenda_do_dia = []
    
    # 1. Adicionar Aulas
    aulas_hoje = df_aulas[df_aulas["dia"] == dia_semana_en]
    for _, aula in aulas_hoje.iterrows():
        agenda_do_dia.append({
            "hora_inicio": aula["hora_inicio"],
            "hora_fim": aula["hora_fim"],
            "tipo": "Aula",
            "titulo": f"{aula['disciplina']} (Sala: {aula['sala']})",
            "icone": "📚"
        })

    # 2. Adicionar Eventos com horário
    eventos_hoje = df_eventos[df_eventos["data"] == hoje_str]
    eventos_com_horario = eventos_hoje[eventos_hoje['hora_inicio'] != '']
    icones_tipo = {"Prova": "📝", "Trabalho": "💼", "Consulta": "🩺", "Estudo": "📚", "Lembrete": "📌"}
    for _, evento in eventos_com_horario.iterrows():
        agenda_do_dia.append({
            "hora_inicio": evento["hora_inicio"],
            "hora_fim": evento["hora_fim"],
            "tipo": evento["tipo"],
            "titulo": f"{evento['titulo']} - {evento['descricao']}",
            "icone": icones_tipo.get(evento['tipo'], "🔔")
        })

    # 3. Ordenar a agenda por hora de início
    agenda_do_dia.sort(key=lambda x: datetime.strptime(x['hora_inicio'], '%H:%M').time())

    # --- Exibindo a Agenda Cronológica ---
    st.subheader("🕒 Sua Agenda para Hoje")
    if not agenda_do_dia:
        st.info("Você não tem nenhum evento com horário agendado para hoje.")
    else:
        for item in agenda_do_dia:
            horario = f"{item['hora_inicio']}"
            if item['hora_fim']:
                horario += f" - {item['hora_fim']}"
            st.markdown(f"""
            <div class="agenda-item">
                <strong>{horario}</strong>: {item['icone']} {item['tipo']} - {item['titulo']}
            </div>
            """, unsafe_allow_html=True)

    # --- Exibindo Tarefas e Lembretes do Dia (sem horário) ---
    tarefas_de_hoje = df_tarefas[df_tarefas['dia_semana'] == dia_semana_en]
    eventos_sem_horario = eventos_hoje[eventos_hoje['hora_inicio'] == '']
    
    if not tarefas_de_hoje.empty or not eventos_sem_horario.empty:
        with st.expander("📋 Tarefas e Lembretes do Dia (sem horário fixo)"):
            for _, tarefa in tarefas_de_hoje.iterrows():
                st.markdown(f"🏠 **Casa:** {tarefa['tarefa']}")
            for _, evento in eventos_sem_horario.iterrows():
                st.markdown(f"{icones_tipo.get(evento['tipo'], '🔔')} **{evento['tipo']}:** {evento['titulo']} - {evento['descricao']}")

    st.markdown("---")
    
    # ... (Restante da página Hoje: Autocuidado e Reflexão) ...
    st.subheader("💧 Autocuidado & Hábitos")
    # ... (código existente) ...
    st.markdown("---")
    st.subheader("📝 Reflexão do Dia")
    # ... (código existente) ...


# ==========================================================
# PÁGINA "CALENDÁRIO" - ATUALIZADA
# ==========================================================
elif menu == "Calendário e Visão Geral":
    st.title("🗓️ Calendário e Visão Geral")
    calendar_events = []
    cores_eventos = {"Prova": "#FF4B4B", "Trabalho": "#FFA500", "Consulta": "#1E90FF", "Estudo": "#32CD32", "Lembrete": "#9370DB"}

    # Adicionar eventos com e sem horário
    for _, row in df_eventos.iterrows():
        start_time = f"{row['data']}T{row['hora_inicio']}:00" if row['hora_inicio'] else row['data']
        end_time = f"{row['data']}T{row['hora_fim']}:00" if row['hora_fim'] else row['data']
        calendar_events.append({
            "title": f"{row['tipo']}: {row['titulo']}",
            "start": start_time,
            "end": end_time,
            "color": cores_eventos.get(row['tipo'], "#808080")
        })

    # Adicionar aulas e tarefas recorrentes
    hoje = datetime.now()
    for i in range(60):
        data_atual = hoje + timedelta(days=i)
        data_str = data_atual.strftime("%Y-%m-%d")
        dia_semana_en = data_atual.strftime("%A")
        
        for _, aula in df_aulas[df_aulas['dia'] == dia_semana_en].iterrows():
            calendar_events.append({"title": f"Aula: {aula['disciplina']}", "start": f"{data_str}T{aula['hora_inicio']}", "end": f"{data_str}T{aula['hora_fim']}", "color": "#4B0082"})
        for _, tarefa in df_tarefas[df_tarefas['dia_semana'] == dia_semana_en].iterrows():
            calendar_events.append({"title": f"Casa: {tarefa['tarefa']}", "start": data_str, "end": data_str, "color": "#2E8B57", "allDay": True})

    calendar(events=calendar_events, options={"headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek,timeGridDay"}, "initialView": "timeGridWeek", "locale": "pt-br"})

# ==========================================================
# PÁGINA "CADASTRAR EVENTO" - ATUALIZADA
# ==========================================================
elif menu == "Cadastrar Evento":
    st.title("🗓️ Cadastrar Novo Evento")
    with st.form("form_eventos", clear_on_submit=True):
        data = st.date_input("Data do Evento")
        tipo = st.selectbox("Tipo de Evento", ["Prova", "Trabalho", "Consulta", "Estudo", "Lembrete"])
        titulo = st.text_input("Título (Ex: Prova de Cálculo, Caminhar no parque)")
        
        col1, col2 = st.columns(2)
        hora_inicio = col1.time_input("Hora de Início (opcional)", value=None)
        hora_fim = col2.time_input("Hora de Término (opcional)", value=None)

        descricao = st.text_area("Descrição (Opcional)")
        
        if st.form_submit_button("Salvar Evento"):
            hora_inicio_str = hora_inicio.strftime('%H:%M') if hora_inicio else ''
            hora_fim_str = hora_fim.strftime('%H:%M') if hora_fim else ''
            
            nova = pd.DataFrame([[data.strftime("%Y-%m-%d"), tipo, titulo, descricao, hora_inicio_str, hora_fim_str]], columns=colunas_eventos)
            df_eventos = pd.concat([df_eventos, nova], ignore_index=True)
            df_eventos.to_csv(EVENTOS_CSV, index=False)
            st.toast("Evento salvo!", icon="✅")
            
    st.markdown("### Eventos Cadastrados"); st.dataframe(df_eventos)

# ... (Restante do código permanece o mesmo) ...
# ==========================================================
# PÁGINAS DE CADASTRO (EXISTENTES)
# ==========================================================
elif menu == "Personalizar Hábitos":
    st.title("🎨 Personalizar Hábitos")
    # ... (código existente) ...

elif menu == "Cadastrar Aulas":
    st.title("📚 Cadastrar Aulas")
    # ... (código existente) ...

elif menu == "Organizar Tarefas da Casa":
    st.title("🏠 Organizar Tarefas da Semana")
    # ... (código existente) ...

elif menu == "Lista de Compras":
    st.title("🛒 Lista de Compras")
    # ... (código existente) ...
