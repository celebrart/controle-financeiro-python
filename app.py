import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Finanças Premium", page_icon="📈", layout="wide")

# Design Customizado (CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #161b22; border-radius: 5px; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl="0s")
        # Se a planilha for nova/vazia, cria a estrutura
        if df is None or df.empty or "Valor" not in df.columns:
            return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])
        return df
    except:
        return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])

# Sidebar
st.sidebar.title("💎 Finanças Pro")
renda = st.sidebar.number_input("Renda Mensal (R$)", min_value=0.0, value=3000.0)
st.sidebar.info("Os dados são salvos automaticamente na sua planilha do Google.")

# Interface Principal
st.title("📊 Seu Painel Financeiro")

aba1, aba2, aba3 = st.tabs(["✨ Dashboard", "📅 Calendário", "➕ Novo Gasto"])

df = carregar_dados()

with aba1:
    if not df.empty:
        # Garante que Valor é número
        df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce').fillna(0)
        total_gasto = df["Valor"].sum()
        sobra = renda - total_gasto
        
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Renda", f"R$ {renda:,.2f}")
        c2.metric("📉 Gastos", f"R$ {total_gasto:,.2f}", delta=f"{(total_gasto/renda)*100:.1f}%", delta_color="inverse")
        c3.metric("🔋 Sobra", f"R$ {sobra:,.2f}", delta=f"{(sobra/renda)*100:.1f}%")
        
        st.divider()
        col_esq, col_dir = st.columns([2, 1])
        with col_esq:
            st.subheader("Análise por Categoria")
            st.bar_chart(df.groupby("Categoria")["Valor"].sum(), color="#58a6ff")
        with col_dir:
            st.subheader("Últimos Lançamentos")
            st.dataframe(df.tail(5), hide_index=True)
    else:
        st.warning("⚠️ Planilha vazia! Adicione um gasto na aba 'Novo Gasto' para começar.")

with aba3:
    st.subheader("🚀 Cadastro Rápido")
    with st.form("form_v2", clear_on_submit=True):
        c_nome, c_valor = st.columns(2)
        nome = c_nome.text_input("O que você pagou?")
        valor = c_valor.number_input("Valor (R$)", min_value=0.0, step=0.01)
        
        c_cat, c_data = st.columns(2)
        categoria = c_cat.selectbox("Categoria", ["🏠 Essencial", "🎡 Lazer", "💳 Dívida", "📈 Investimento"])
        data_pago = c_data.date_input("Data", value=date.today())
        
        btn = st.form_submit_button("REGISTRAR NA NUVEM")
        
        if btn and nome:
            novo_dado = pd.DataFrame([{"Conta": nome, "Valor": valor, "Categoria": categoria, "Data": str(data_pago)}])
            df_final = pd.concat([df, novo_dado], ignore_index=True)
            try:
                conn.update(data=df_final)
                st.balloons()
                st.success("✅ Sincronizado com sucesso!")
            except:
                st.error("Erro técnico: Limpe sua planilha do Google e tente novamente.")

with aba2:
    st.subheader("📅 Pagamentos Futuros")
    if not df.empty:
        hoje = str(date.today())
        futuros = df[df["Data"] >= hoje].sort_values(by="Data")
        st.table(futuros)
    else:
        st.write("Sem registros.")
