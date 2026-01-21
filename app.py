import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# Configuração da página com tema escuro e layout largo
st.set_page_config(page_title="Finanças Pro | Smart Dashboard", layout="wide", initial_sidebar_state="expanded")

# Estilização Personalizada (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4255; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #00ff7f; color: black; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1e2130; border-radius: 5px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl="0s")
        return df
    except:
        return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/552/552791.png", width=100)
st.sidebar.title("Configurações")
renda = st.sidebar.number_input("💵 Renda Mensal Líquida", min_value=0.0, value=3000.0, step=100.0)
st.sidebar.divider()
st.sidebar.markdown("### 🎯 Metas (50-30-20)")
st.sidebar.progress(0.5, text="Essenciais (50%)")
st.sidebar.progress(0.3, text="Lazer (30%)")
st.sidebar.progress(0.2, text="Reserva (20%)")

# --- CORPO PRINCIPAL ---
st.title("🛡️ Finanças Pro: Seu Dashboard Inteligente")

aba1, aba2, aba3 = st.tabs(["📈 Dashboard Analítico", "📅 Próximas Contas", "➕ Novo Lançamento"])

with aba1:
    df = carregar_dados()
    if not df.empty:
        # Cálculos
        df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce').fillna(0)
        total_gasto = df["Valor"].sum()
        sobra = renda - total_gasto
        perc_gasto = (total_gasto / renda) * 100 if renda > 0 else 0

        # Cards de Resumo Superior
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("💰 Renda Total", f"R$ {renda:.2f}")
        c2.metric("📉 Total Gasto", f"R$ {total_gasto:.2f}", delta=f"{perc_gasto:.1f}%", delta_color="inverse")
        c3.metric("✅ Sobra Livre", f"R$ {sobra:.2f}", delta=f"{100-perc_gasto:.1f}%")
        c4.metric("📊 Lançamentos", len(df))

        st.divider()

        # Gráficos e Tabelas
        col_graf, col_tab = st.columns([2, 1])
        
        with col_graf:
            st.subheader("Distribuição por Categoria")
            chart_data = df.groupby("Categoria")["Valor"].sum()
            st.bar_chart(chart_data, color="#00ff7f")
            
        with col_tab:
            st.subheader("Últimos Registros")
            st.dataframe(df.tail(10), use_container_width=True, hide_index=True)
    else:
        st.info("👋 Bem-vindo! Comece cadastrando seus gastos na aba 'Novo Lançamento'.")

with aba2:
    st.subheader("📅 Calendário de Vencimentos")
    df = carregar_dados()
    if not df.empty:
        hoje = str(date.today())
        pendentes = df[df["Data"] >= hoje].sort_values(by="Data")
        
        for index, row in pendentes.iterrows():
            with st.expander(f"📌 {row['Data']} - {row['Conta']}"):
                cc1, cc2 = st.columns(2)
                cc1.write(f"**Valor:** R$ {row['Valor']:.2f}")
                cc1.write(f"**Categoria:** {row['Categoria']}")
                if st.button(f"Marcar como Pago: {row['Conta']}", key=index):
                    st.toast("Funcionalidade em desenvolvimento!")
    else:
        st.write("Nada agendado por enquanto.")

with aba3:
    st.subheader("🚀 Lançamento Rápido")
    with st.container():
        with st.form("form_lindo", clear_on_submit=True):
            f1, f2 = st.columns(2)
            nome = f1.text_input("O que você pagou? (Ex: Aluguel)")
            valor = f2.number_input("Qual o valor? (R$)", min_value=0.0, step=0.01)
            
            f3, f4 = st.columns(2)
            categoria = f3.selectbox("Categoria", ["🏠 Essencial", "🎡 Lazer", "💳 Dívida", "📈 Investimento"])
            data_venc = f4.date_input("Data do Pagamento", value=date.today())
            
            enviar = st.form_submit_button("REGISTRAR AGORA")

            if enviar and nome:
                df_atual = carregar_dados()
                novo = pd.DataFrame([{"Conta": nome, "Valor": valor, "Categoria": categoria, "Data": str(data_venc)}])
                df_final = pd.concat([df_atual, novo], ignore_index=True)
                
                try:
                    conn.update(data=df_final)
                    st.balloons()
                    st.success(f"Sucesso! {nome} foi adicionado à sua nuvem.")
                except:
                    st.error("Erro de Permissão! Verifique se a planilha está como EDITOR.")
