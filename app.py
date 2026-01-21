import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Finanças Pro", layout="wide")

# Conexão com Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        df = conn.read(ttl="0s")
        # Se a planilha estiver vazia ou sem as colunas certas, cria um padrão
        if df.empty or "Valor" not in df.columns:
            return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])
        return df
    except:
        return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])

st.title("🛡️ Finanças Pro: Sincronizado")

# Renda Mensal na lateral
renda_mensal = st.sidebar.number_input("Sua Renda Mensal (R$)", min_value=0.0, value=3000.0)

aba1, aba2, aba3 = st.tabs(["📊 Análise", "📅 Agendamentos", "➕ Novo Gasto"])

with aba3:
    st.subheader("Registrar Novo Gasto")
    with st.form("meu_form"):
        nome = st.text_input("Nome da Conta")
        valor = st.number_input("Valor (R$)", min_value=0.0)
        cat = st.selectbox("Categoria", ["Essencial", "Lazer", "Dívida", "Reserva"])
        dt = st.date_input("Data")
        submit = st.form_submit_button("Salvar na Planilha")

        if submit and nome:
            df_atual = carregar_dados()
            novo_item = pd.DataFrame([{"Conta": nome, "Valor": valor, "Categoria": cat, "Data": str(dt)}])
            df_final = pd.concat([df_atual, novo_item], ignore_index=True)
            conn.update(data=df_final)
            st.success("✅ Salvo com sucesso! Vá na aba Análise.")

with aba1:
    df = carregar_dados()
    if not df.empty:
        # Garante que 'Valor' é número para não dar erro no cálculo
        df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce').fillna(0)
        
        total = df["Valor"].sum()
        sobra = renda_mensal - total
        
        c1, c2 = st.columns(2)
        c1.metric("Total de Gastos", f"R$ {total:.2f}")
        c2.metric("Sobra no Mês", f"R$ {sobra:.2f}", delta_color="normal")
        
        st.write("### Seus Lançamentos")
        st.dataframe(df, use_container_width=True)
        
        st.write("### Gastos por Categoria")
        st.bar_chart(df.groupby("Categoria")["Valor"].sum())
    else:
        st.info("Sua planilha está pronta! Use a aba 'Novo Lançamento' para começar.")

with aba2:
    st.subheader("Próximos Pagamentos")
    if not df.empty:
        hoje = str(date.today())
        futuros = df[df["Data"] >= hoje]
        if not futuros.empty:
            st.table(futuros)
        else:
            st.write("Nenhum pagamento futuro encontrado.")
