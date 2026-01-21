import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

# Configuração de Layout e Tema
st.set_page_config(page_title="Finanças Pro", page_icon="💰", layout="wide")

# CSS para Design Customizado (Cards e Fontes)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; color: #00ff7f; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e1e26;
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        color: white;
    }
    .main-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00ff7f;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl="0s")
        if df.empty or "Valor" not in df.columns:
            return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])
        return df
    except:
        return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])

# --- HEADER ---
st.title("💎 Seu Dashboard Inteligente")
st.markdown("---")

# Barra Lateral
st.sidebar.header("⚙️ Configurações")
renda = st.sidebar.number_input("Sua Renda Mensal (R$)", min_value=0.0, value=3000.0)

# Carregamento de dados
df = carregar_dados()

# --- DASHBOARD ANALÍTICO ---
aba1, aba2, aba3 = st.tabs(["📈 Dashboard Analítico", "📅 Próximas Contas", "➕ Novo Lançamento"])

with aba1:
    if not df.empty:
        # Processamento de dados seguro
        df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce').fillna(0)
        total_gasto = df["Valor"].sum()
        saldo = renda - total_gasto
        
        # Cards de Resumo com Design
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.metric("💰 Renda Total", f"R$ {renda:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="main-card" style="border-left-color: #ff4b4b;">', unsafe_allow_html=True)
            st.metric("📉 Total Gasto", f"R$ {total_gasto:.2f}", delta=f"{(total_gasto/renda)*100:.1f}%", delta_color="inverse")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="main-card" style="border-left-color: #00ff7f;">', unsafe_allow_html=True)
            st.metric("✅ Saldo Livre", f"R$ {saldo:.2f}", delta=f"{(saldo/renda)*100:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("### 📊 Gastos por Categoria")
        chart_data = df.groupby("Categoria")["Valor"].sum()
        st.bar_chart(chart_data, color="#00ff7f")
        
        st.markdown("### 📝 Histórico de Transações")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("👋 Bem-vindo! Vá na aba 'Novo Lançamento' para registrar seu primeiro gasto.")

with aba2:
    st.subheader("📅 Contas Futuras e Agendamentos")
    if not df.empty:
        hoje = str(date.today())
        pendentes = df[df["Data"] >= hoje].sort_values(by="Data")
        if not pendentes.empty:
            st.table(pendentes)
        else:
            st.success("Tudo pago por hoje! Nenhuma conta futura encontrada.")
    else:
        st.write("O calendário está vazio.")

with aba3:
    st.subheader("🚀 Cadastro Rápido")
    with st.form("form_lindo", clear_on_submit=True):
        col_n, col_v = st.columns(2)
        nome = col_n.text_input("Nome da Conta (ex: Aluguel)")
        valor = col_v.number_input("Valor (R$)", min_value=0.0, step=0.01)
        
        col_c, col_d = st.columns(2)
        categoria = col_c.selectbox("Categoria", ["Essencial", "Lazer", "Dívida", "Investimento"])
        data_venc = col_d.date_input("Data", value=date.today())
        
        botao = st.form_submit_button("REGISTRAR GASTO")

        if botao and nome:
            df_atual = carregar_dados()
            novo = pd.DataFrame([{"Conta": nome, "Valor": valor, "Categoria": categoria, "Data": str(data_venc)}])
            df_final = pd.concat([df_atual, novo], ignore_index=True)
            
            try:
                conn.update(data=df_final)
                st.balloons()
                st.success("Dados salvos na nuvem com sucesso!")
            except Exception as e:
                st.error("Erro de permissão! Verifique se a planilha está como 'Editor' para qualquer pessoa com o link.")
