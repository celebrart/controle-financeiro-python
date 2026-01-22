import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Finanças Premium", page_icon="📈", layout="wide")

# ================== ESTILO ==================
st.markdown("""
<style>
.main { background-color: #0e1117; }
div[data-testid="stMetric"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================== CONEXÃO ==================
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    df = conn.read(ttl="0s")
    if df is None or df.empty:
        return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])
    return df

# ================== SIDEBAR ==================
st.sidebar.title("💎 Finanças Pro")
renda = st.sidebar.number_input("Renda Mensal (R$)", min_value=0.0, value=3000.0)
st.sidebar.success("✔️ Salvando direto no Google Sheets")

# ================== APP ==================
st.title("📊 Painel Financeiro")

aba1, aba2, aba3 = st.tabs(["✨ Dashboard", "📅 Calendário", "➕ Novo Gasto"])

df = carregar_dados()

# ================== DASHBOARD ==================
with aba1:
    if not df.empty:
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0)
        total = df["Valor"].sum()
        sobra = renda - total

        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Renda", f"R$ {renda:,.2f}")
        c2.metric("📉 Gastos", f"R$ {total:,.2f}")
        c3.metric("🔋 Sobra", f"R$ {sobra:,.2f}")

        st.bar_chart(df.groupby("Categoria")["Valor"].sum())
        st.dataframe(df.tail(5), hide_index=True)
    else:
        st.warning("Planilha vazia. Adicione um gasto 👇")

# ================== NOVO GASTO ==================
with aba3:
    with st.form("form_gasto", clear_on_submit=True):
        nome = st.text_input("O que você pagou?")
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
        categoria = st.selectbox("Categoria", ["🏠 Essencial", "🎡 Lazer", "💳 Dívida", "📈 Investimento"])
        data_pago = st.date_input("Data", value=date.today())

        salvar = st.form_submit_button("💾 REGISTRAR")

        if salvar and nome:
            novo = pd.DataFrame([{
                "Conta": nome,
                "Valor": valor,
                "Categoria": categoria,
                "Data": str(data_pago)
            }])

            df_final = pd.concat([df, novo], ignore_index=True)

            conn.update(
                worksheet="db_financas",
                data=df_final
            )

            st.success("✅ Dado salvo no Google Sheets!")
            st.balloons()

# ================== CALENDÁRIO ==================
with aba2:
    if not df.empty:
        hoje = str(date.today())
        futuros = df[df["Data"] >= hoje].sort_values("Data")
        st.table(futuros)
    else:
        st.info("Nenhum lançamento ainda.")
