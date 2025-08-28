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
            background-color: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(15px);
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
            background-color: rgba(255, 255, 255, 0.8);
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
ATIVIDADES_RECORRENTES_CSV = "atividades_recorrentes.csv"
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
ICON_MAP = {"Prova": "📝", "Trabalho": "💼", "Consulta": "🩺", "Estudo": "📚", "Lembrete": "📌", "Exercício": "🏋️‍♀️", "Outro": "✨"}


# --- Funções Auxiliares ---
def carregar_csv(caminho, colunas):
    if not os.path.exists(caminho):
        return pd.DataFrame(columns=colunas)
    df = pd.read_csv(caminho, dtype=str).fillna('') # Lê todas as colunas como texto para evitar erros
    for col in colunas:
        if col not in df.columns:
            df[col] = ''
    return df

# --- Inicializar DataFrames ---
colunas_aulas = ["disciplina", "sala", "dia_semana", "hora_inicio", "hora_fim"]
colunas_eventos = ["data", "tipo", "titulo", "descricao", "hora_inicio", "hora_fim"]
colunas_atividades_recorrentes = ["titulo", "tipo", "dia_semana", "hora_inicio", "hora_fim"]
colunas_rotina_matinal = ["data", "cama_arrumada", "dentes_escovados", "rosto_lavado", "meditacao"]
colunas_habitos = ["data", "agua"]
colunas_meus_habitos = ["habito"]
colunas_habitos_feitos = ["data", "habito", "feito"]
colunas_diario = ["data", "gratidao", "desafio", "aprendizado", "observacao"]

df_aulas = carregar_csv(AULAS_CSV, colunas_aulas)
df_eventos = carregar_csv(EVENTOS_CSV, colunas_eventos)
df_atividades_recorrentes = carregar_csv(ATIVIDADES_RECORRENTES_CSV, colunas_atividades_recorrentes)
df_tarefas = carregar_csv(TAREFAS_CSV, ["dia_semana", "tarefa"])
df_compras = carregar_csv(COMPRAS_CSV, ["item", "comprado"])
df_rotina_matinal = carregar_csv(ROTINA_MATINAL_CSV, colunas_rotina_matinal)
df_habitos = carregar_csv(HABITOS_CSV, colunas_habitos)
df_meus_habitos = carregar_csv(MEUS_HABITOS_CSV, colunas_meus_habitos)
df_habitos_feitos = carregar_csv(HABITOS_FEITOS_CSV, colunas_habitos_feitos)
df_diario = carregar_csv(DIARIO_CSV, colunas_diario)


# --- Menu Lateral Simplificado ---
menu = st.sidebar.radio("Menu", ["Hoje", "Calendário", "Cadastros", "Lista de Compras"])

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
    random.seed(hoje_dt.toordinal())
    st.markdown(f'<div class="quote-container">"{random.choice(FRASES)}"</div>', unsafe_allow_html=True)

    # --- Montando a Agenda do Dia ---
    agenda_do_dia = []
    # 1. Aulas
    aulas_hoje = df_aulas[df_aulas["dia_semana"].str.strip() == dia_semana_en]
    for _, aula in aulas_hoje.iterrows():
        agenda_do_dia.append({"hora_inicio": aula["hora_inicio"], "hora_fim": aula["hora_fim"], "tipo": "Aula", "titulo": f"{aula['disciplina']} (Sala: {aula['sala']})", "icone": "📚"})
    # 2. Eventos com horário
    eventos_hoje = df_eventos[df_eventos["data"] == hoje_str]
    for _, evento in eventos_hoje[eventos_hoje['hora_inicio'] != ''].iterrows():
        agenda_do_dia.append({"hora_inicio": evento["hora_inicio"], "hora_fim": evento["hora_fim"], "tipo": evento["tipo"], "titulo": f"{evento['titulo']}", "icone": ICON_MAP.get(evento['tipo'], "🔔")})
    # 3. Atividades Recorrentes com horário
    atividades_hoje = df_atividades_recorrentes[df_atividades_recorrentes["dia_semana"].str.strip() == dia_semana_en]
    for _, atividade in atividades_hoje.iterrows():
        agenda_do_dia.append({"hora_inicio": atividade["hora_inicio"], "hora_fim": atividade["hora_fim"], "tipo": atividade["tipo"], "titulo": atividade["titulo"], "icone": ICON_MAP.get(atividade['tipo'], "✨")})

    # Ordenar a agenda
    if agenda_do_dia:
        agenda_do_dia.sort(key=lambda x: datetime.strptime(x['hora_inicio'], '%H:%M').time())

    # --- LAYOUT COM COLUNAS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🕒 Agenda do Dia")
        if not agenda_do_dia:
            st.info("Você não tem nenhum evento com horário agendado para hoje.")
        else:
            for item in agenda_do_dia:
                horario = f"{item['hora_inicio']}" + (f" - {item['hora_fim']}" if item['hora_fim'] else "")
                st.markdown(f"""<div class="agenda-item"><strong>{horario}</strong>: {item['icone']} {item['titulo']}</div>""", unsafe_allow_html=True)
        
        st.subheader("📋 Lembretes e Tarefas da Casa")
        # Tarefas da casa (sem horário)
        tarefas_de_hoje = df_tarefas[df_tarefas['dia_semana'].str.strip() == dia_semana_en]
        for _, tarefa in tarefas_de_hoje.iterrows():
            st.markdown(f"🏠 **Casa:** {tarefa['tarefa']}")
        # Eventos do dia (sem horário)
        for _, evento in eventos_hoje[eventos_hoje['hora_inicio'] == ''].iterrows():
            titulo_evento = f"{ICON_MAP.get(evento['tipo'], '🔔')} **{evento['tipo']}:** {evento['titulo']}"
            if evento['descricao']:
                with st.expander(titulo_evento):
                    st.write(evento['descricao'])
            else:
                st.markdown(titulo_evento)


    with col2:
        st.subheader("☀️ Autocuidado Diário")
        agua = int(df_habitos[df_habitos["data"] == hoje_str]["agua"].iloc[0]) if hoje_str in df_habitos["data"].values else 0
        if hoje_str in df_rotina_matinal["data"].values:
            rotina_hoje = df_rotina_matinal[df_rotina_matinal["data"] == hoje_str].iloc[0]
            cama, dentes, rosto, meditacao = bool(eval(str(rotina_hoje["cama_arrumada"]))), bool(eval(str(rotina_hoje["dentes_escovados"]))), bool(eval(str(rotina_hoje["rosto_lavado"]))), bool(eval(str(rotina_hoje["meditacao"])))
        else:
            cama, dentes, rosto, meditacao = False, False, False, False

        cama_check = st.checkbox("🛏️ Arrumar a cama", value=cama)
        dentes_check = st.checkbox("🦷 Escovar os dentes", value=dentes)
        rosto_check = st.checkbox("🧼 Lavar o rosto", value=rosto)
        meditacao_check = st.checkbox("🧘‍♀️ Meditar", value=meditacao)

        meta_agua = 2000
        copo_padrao = st.number_input("⚙️ Tamanho do copo (ml)", 50, 1000, 250, 50)
        c1, c2, c3 = st.columns(3)
        if c1.button(f"💧 Beber 1 copo (+{copo_padrao} ml)"): agua += copo_padrao
        if c2.button("🥤 Beber 500 ml"): agua += 500
        if c3.button("🍼 Beber 1 garrafa (1000 ml)"): agua += 1000
        st.progress(min(1.0, agua / meta_agua)); st.write(f"Você já bebeu **{agua} ml** de água hoje. Meta: **{meta_agua} ml**")

        habitos_personalizados = df_meus_habitos["habito"].tolist()
        habitos_feitos_hoje = df_habitos_feitos[df_habitos_feitos["data"] == hoje_str]
        habitos_marcados = {}
        for habito in habitos_personalizados:
            feito_df = habitos_feitos_hoje[habitos_feitos_hoje["habito"] == habito]
            feito = bool(eval(str(feito_df["feito"].iloc[0]))) if not feito_df.empty else False
            habitos_marcados[habito] = st.checkbox(habito, value=feito)

        if st.button("Salvar Autocuidado"):
            df_rotina_matinal = df_rotina_matinal[df_rotina_matinal["data"] != hoje_str]
            nova_rotina = pd.DataFrame([[hoje_str, cama_check, dentes_check, rosto_check, meditacao_check]], columns=colunas_rotina_matinal)
            df_rotina_matinal = pd.concat([df_rotina_matinal, nova_rotina], ignore_index=True)
            df_rotina_matinal.to_csv(ROTINA_MATINAL_CSV, index=False)
            df_habitos = df_habitos[df_habitos["data"] != hoje_str]
            novo_habito = pd.DataFrame([[hoje_str, agua]], columns=colunas_habitos)
            df_habitos = pd.concat([df_habitos, novo_habito], ignore_index=True)
            df_habitos.to_csv(HABITOS_CSV, index=False)
            df_habitos_feitos = df_habitos_feitos[df_habitos_feitos["data"] != hoje_str]
            for habito, feito in habitos_marcados.items():
                novo_feito = pd.DataFrame([[hoje_str, habito, feito]], columns=["data", "habito", "feito"])
                df_habitos_feitos = pd.concat([df_habitos_feitos, novo_feito], ignore_index=True)
            df_habitos_feitos.to_csv(HABITOS_FEITOS_CSV, index=False)
            st.toast("Seu autocuidado foi salvo!", icon="💖")

        st.subheader("📝 Reflexão do Dia")
        if hoje_str in df_diario["data"].values:
            diario_hoje = df_diario[df_diario["data"] == hoje_str].iloc[0]
            gratidao, desafio, aprendizado, obs = diario_hoje["gratidao"], diario_hoje["desafio"], diario_hoje["aprendizado"], diario_hoje["observacao"]
        else:
            gratidao, desafio, aprendizado, obs = "", "", "", ""
        gratidao_txt = st.text_input("Pelo que você é grato(a) hoje?", value=gratidao)
        desafio_txt = st.text_input("Qual foi o maior desafio do dia?", value=desafio)
        aprendizado_txt = st.text_input("O que você aprendeu de novo hoje?", value=aprendizado)
        obs_txt = st.text_area("Observações gerais:", value=obs)
        if st.button("Salvar Reflexão"):
            df_diario = df_diario[df_diario["data"] != hoje_str]
            novo_diario = pd.DataFrame([[hoje_str, gratidao_txt, desafio_txt, aprendizado_txt, obs_txt]], columns=colunas_diario)
            df_diario = pd.concat([df_diario, novo_diario], ignore_index=True)
            df_diario.to_csv(DIARIO_CSV, index=False)
            st.toast("Sua reflexão foi salva!", icon="✨")

# ==========================================================
# PÁGINA "CALENDÁRIO"
# ==========================================================
elif menu == "Calendário":
    st.title("🗓️ Calendário e Visão Geral")
    calendar_events = []
    cores_eventos = {"Prova": "#FF4B4B", "Trabalho": "#FFA500", "Consulta": "#1E90FF", "Estudo": "#32CD32", "Lembrete": "#9370DB", "Exercício": "#3CB371", "Outro": "#D3D3D3"}

    for _, row in df_eventos.iterrows():
        start_time = f"{row['data']}T{row['hora_inicio']}:00" if row['hora_inicio'] else row['data']
        end_time = f"{row['data']}T{row['hora_fim']}:00" if row['hora_fim'] else row['data']
        calendar_events.append({"title": f"{row['tipo']}: {row['titulo']}", "start": start_time, "end": end_time, "color": cores_eventos.get(row['tipo'], "#808080")})

    hoje = datetime.now()
    for i in range(60):
        data_atual = hoje + timedelta(days=i)
        data_str = data_atual.strftime("%Y-%m-%d")
        dia_semana_en = data_atual.strftime("%A")
        
        for _, aula in df_aulas[df_aulas['dia_semana'] == dia_semana_en].iterrows():
            calendar_events.append({"title": f"Aula: {aula['disciplina']}", "start": f"{data_str}T{aula['hora_inicio']}", "end": f"{data_str}T{aula['hora_fim']}", "color": "#4B0082"})
        for _, tarefa in df_tarefas[df_tarefas['dia_semana'] == dia_semana_en].iterrows():
            calendar_events.append({"title": f"Casa: {tarefa['tarefa']}", "start": data_str, "end": data_str, "color": "#2E8B57", "allDay": True})
        for _, atividade in df_atividades_recorrentes[df_atividades_recorrentes['dia_semana'] == dia_semana_en].iterrows():
            calendar_events.append({"title": f"{atividade['tipo']}: {atividade['titulo']}", "start": f"{data_str}T{atividade['hora_inicio']}", "end": f"{data_str}T{atividade['hora_fim']}", "color": cores_eventos.get(atividade['tipo'], "#808080")})

    calendar(events=calendar_events, options={"headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,timeGridWeek,timeGridDay"}, "initialView": "timeGridWeek", "locale": "pt-br"})

# ==========================================================
# PÁGINA "CADASTROS" UNIFICADA
# ==========================================================
elif menu == "Cadastros":
    st.title("⚙️ Central de Cadastros")
    
    tipo_cadastro = st.selectbox("O que você deseja cadastrar ou gerenciar?", 
                                 ["Aulas", "Compromissos", "Tarefas da Casa", "Checklist de Hábitos (sem horário)"])

    if tipo_cadastro == "Aulas":
        st.subheader("📚 Gerenciar Disciplinas e Aulas")
        with st.form("form_aulas", clear_on_submit=True):
            disciplina = st.text_input("Nome da Disciplina")
            sala = st.text_input("Sala (opcional)")
            dias_selecionados = st.multiselect("Selecione os dias da semana para esta disciplina:", options=list(DIAS_PT.values()))
            horarios = {}
            for dia_pt in dias_selecionados:
                st.markdown(f"--- \n **Horário para {dia_pt}**")
                col1, col2 = st.columns(2)
                hora_inicio = col1.time_input("Hora de Início", key=f"inicio_{dia_pt}")
                hora_fim = col2.time_input("Hora de Término", key=f"fim_{dia_pt}")
                horarios[dia_pt] = (hora_inicio, hora_fim)
            if st.form_submit_button("Salvar Disciplina e Horários"):
                for dia_pt, (inicio, fim) in horarios.items():
                    if inicio and fim:
                        dia_en = [k for k, v in DIAS_PT.items() if v == dia_pt][0]
                        nova_aula = pd.DataFrame([[disciplina, sala, dia_en, inicio.strftime('%H:%M'), fim.strftime('%H:%M')]], columns=colunas_aulas)
                        df_aulas = pd.concat([df_aulas, nova_aula], ignore_index=True)
                df_aulas.to_csv(AULAS_CSV, index=False)
                st.success(f"Disciplina '{disciplina}' salva com sucesso!")

        st.markdown("### Aulas Cadastradas")
        for index, row in df_aulas.iterrows():
            col1, col2 = st.columns([0.9, 0.1])
            dia_pt = DIAS_PT.get(row['dia_semana'], '')
            col1.write(f"**{row['disciplina']}** - {dia_pt} ({row['hora_inicio']} - {row['hora_fim']}) Sala: {row['sala']}")
            if col2.button("Excluir", key=f"del_aula_{index}"):
                df_aulas.drop(index, inplace=True)
                df_aulas.to_csv(AULAS_CSV, index=False)
                st.rerun()

    elif tipo_cadastro == "Compromissos":
        st.subheader("🗓️ Agendar Compromissos")
        recorrente = st.checkbox("É um compromisso recorrente? (Ex: estudar, se exercitar)")
        if recorrente:
            st.markdown("#### Cadastrar Compromisso Recorrente")
            with st.form("form_recorrente", clear_on_submit=True):
                titulo = st.text_input("Título do Compromisso (Ex: Academia, Estudar Python)")
                tipo = st.selectbox("Tipo de Compromisso", ["Estudo", "Exercício", "Lembrete", "Outro"])
                dias_recorrentes = st.multiselect("Selecione os dias em que se repete:", options=list(DIAS_PT.values()))
                horarios_recorrentes = {}
                for dia_pt in dias_recorrentes:
                    st.markdown(f"--- \n **Horário para {dia_pt}**")
                    col1, col2 = st.columns(2)
                    hora_inicio_rec = col1.time_input("Hora de Início", key=f"rec_inicio_{dia_pt}")
                    hora_fim_rec = col2.time_input("Hora de Término (opcional)", key=f"rec_fim_{dia_pt}")
                    horarios_recorrentes[dia_pt] = (hora_inicio_rec, hora_fim_rec)
                
                if st.form_submit_button("Salvar Compromisso Recorrente"):
                    for dia_pt, (inicio, fim) in horarios_recorrentes.items():
                        if inicio:
                            dia_en = [k for k, v in DIAS_PT.items() if v == dia_pt][0]
                            nova_ativ = pd.DataFrame([[titulo, tipo, dia_en, inicio.strftime('%H:%M'), fim.strftime('%H:%M') if fim else '']], columns=colunas_atividades_recorrentes)
                            df_atividades_recorrentes = pd.concat([df_atividades_recorrentes, nova_ativ], ignore_index=True)
                    df_atividades_recorrentes.to_csv(ATIVIDADES_RECORRENTES_CSV, index=False)
                    st.success("Compromisso recorrente salvo!")
            st.markdown("#### Compromissos Recorrentes Cadastrados")
            for index, row in df_atividades_recorrentes.iterrows():
                col1, col2 = st.columns([0.9, 0.1])
                dia_pt = DIAS_PT.get(row['dia_semana'], '')
                col1.write(f"**{row['titulo']}** ({row['tipo']}) - {dia_pt} ({row['hora_inicio']})")
                if col2.button("Excluir", key=f"del_ativ_rec_{index}"):
                    df_atividades_recorrentes.drop(index, inplace=True)
                    df_atividades_recorrentes.to_csv(ATIVIDADES_RECORRENTES_CSV, index=False)
                    st.rerun()
        else:
            st.markdown("#### Cadastrar Compromisso Único")
            with st.form("form_eventos", clear_on_submit=True):
                data = st.date_input("Data do Compromisso")
                tipo = st.selectbox("Tipo de Compromisso", ["Prova", "Trabalho", "Consulta", "Lembrete"])
                titulo = st.text_input("Título (Ex: Prova de Cálculo, Dentista)")
                col1, col2 = st.columns(2)
                hora_inicio = col1.time_input("Hora de Início (opcional)", value=None)
                hora_fim = col2.time_input("Hora de Término (opcional)", value=None)
                descricao = st.text_area("Descrição (Opcional)")
                if st.form_submit_button("Salvar Compromisso"):
                    hora_inicio_str = hora_inicio.strftime('%H:%M') if hora_inicio else ''
                    hora_fim_str = hora_fim.strftime('%H:%M') if hora_fim else ''
                    nova = pd.DataFrame([[data.strftime("%Y-%m-%d"), tipo, titulo, descricao, hora_inicio_str, hora_fim_str]], columns=colunas_eventos)
                    df_eventos = pd.concat([df_eventos, nova], ignore_index=True)
                    df_eventos.to_csv(EVENTOS_CSV, index=False)
                    st.toast("Compromisso salvo!", icon="✅")
            st.markdown("#### Compromissos Únicos Cadastrados")
            for index, row in df_eventos.iterrows():
                col1, col2 = st.columns([0.9, 0.1])
                col1.write(f"**{row['data']}** - {row['titulo']} ({row['tipo']})")
                if col2.button("Excluir", key=f"del_evento_{index}"):
                    df_eventos.drop(index, inplace=True)
                    df_eventos.to_csv(EVENTOS_CSV, index=False)
                    st.rerun()

    elif tipo_cadastro == "Tarefas da Casa":
        st.subheader("🏠 Organizar Tarefas da Semana")
        with st.form("form_tarefas", clear_on_submit=True):
            dia_pt = st.selectbox("Selecione o dia da semana", options=list(DIAS_PT.values()))
            dia_en = [k for k, v in DIAS_PT.items() if v == dia_pt][0]
            tarefa = st.text_input("Qual tarefa você quer agendar?", placeholder="Ex: Lavar roupa, Fazer feira")
            if st.form_submit_button("Agendar Tarefa"):
                if tarefa:
                    nova_tarefa = pd.DataFrame([[dia_en, tarefa]], columns=["dia_semana", "tarefa"])
                    df_tarefas = pd.concat([df_tarefas, nova_tarefa], ignore_index=True)
                    df_tarefas.to_csv(TAREFAS_CSV, index=False)
                    st.toast(f'Tarefa "{tarefa}" agendada para toda {dia_pt}!', icon="👍")
        st.markdown("### Seu Cronograma de Tarefas")
        for index, row in df_tarefas.iterrows():
            col1, col2 = st.columns([0.9, 0.1])
            dia_pt = DIAS_PT.get(row['dia_semana'], '')
            col1.write(f"**{dia_pt}**: {row['tarefa']}")
            if col2.button("Excluir", key=f"del_tarefa_{index}"):
                df_tarefas.drop(index, inplace=True)
                df_tarefas.to_csv(TAREFAS_CSV, index=False)
                st.rerun()

    elif tipo_cadastro == "Checklist de Hábitos (sem horário)":
        st.subheader("🎨 Personalizar Hábitos do Checklist")
        st.write("Adicione ou remova os hábitos que você deseja marcar como 'feitos' no seu dia a dia (sem horário fixo).")
        with st.form("form_novo_habito", clear_on_submit=True):
            novo_habito_txt = st.text_input("Digite um novo hábito (Ex: Cuidar da pele, Ler 10 páginas)")
            if st.form_submit_button("Adicionar Hábito"):
                if novo_habito_txt and novo_habito_txt not in df_meus_habitos["habito"].values:
                    novo_df = pd.DataFrame([[novo_habito_txt]], columns=["habito"])
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
    for index, row in df_compras.iterrows():
        # A conversão para bool é importante aqui
        comprado = st.checkbox(row["item"], value=bool(eval(str(row["comprado"]))), key=f"item_{index}")
        if comprado != bool(eval(str(row["comprado"]))):
            df_compras.at[index, "comprado"] = comprado
            df_compras.to_csv(COMPRAS_CSV, index=False)
            st.rerun()
    if not df_compras.empty and st.button("Limpar itens comprados"):
        df_compras = df_compras[df_compras["comprado"] == False]
        df_compras.to_csv(COMPRAS_CSV, index=False)
        st.toast("Lista limpa!", icon="🗑️")
        st.rerun()
