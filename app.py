import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Finanças Pro - Integrado", layout="wide")

# Conexão com o Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados():
    try:
        # Tenta ler a aba principal (Sheet1 ou Página1)
        return conn.read(ttl="0s")
    except:
        # Se estiver vazia, retorna um DataFrame com a estrutura correta
        return pd.DataFrame(columns=["Conta", "Valor", "Categoria", "Data"])

st.title("🛡️ Finanças Pro: Sincronizado com Google Sheets")

aba1, aba2, aba3 = st.tabs(["📊 Análise de Gastos", "📅 Agendamentos", "➕ Novo Lançamento"])

with aba3:
    st.subheader("Registrar no Google Sheets")
    with st.form("form_registro"):
        conta = st.text_input("Nome da Despesa")
        valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
        cat = st.selectbox("Categoria", ["Essencial", "Lazer", "Dívida", "Educação", "Reserva"])
        dt = st.date_input("Data de Vencimento", value=date.today())
        
        submit = st.form_submit_button("Salvar na Nuvem")

        if submit:
            df_atual = carregar_dados()
            # Criar nova linha
            novo_dado = pd.DataFrame([{
                "Conta": conta, 
                "Valor": valor, 
                "Categoria": cat, 
                "Data": dt.strftime('%Y-%m-%d')
            }])
            # Concatenar e salvar
            df_final = pd.concat([df_atual, novo_dado], ignore_index=True)
            conn.update(data=df_final)
            st.success("✅ Gravado com sucesso na planilha!")

with aba1:
    df = carregar_dados()
    if not df.empty:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Total Acumulado", f"R$ {df['Valor'].astype(float).sum():.2f}")
            st.write("### Histórico")
            st.dataframe(df, use_container_width=True)
            
        with col2:
            st.write("### Divisão por Categoria")
            chart_data = df.groupby('Categoria')['Valor'].sum()
            st.bar_chart(chart_data)
    else:
        st.info("Nenhum dado encontrado. Faça o primeiro lançamento na aba ao lado.")

with aba2:
    st.subheader("Próximos Pagamentos")
    df = carregar_dados()
    if not df.empty:
        # Filtra datas futuras
        hoje = date.today().strftime('%Y-%m-%d')
        pendentes = df[df['Data'] >= hoje]
        if not pendentes.empty:
            for _, row in pendentes.iterrows():
                st.info(f"📅 **{row['Data']}**: {row['Conta']} - R$ {row['Valor']}")
        else:
            st.write("Não há pagamentos futuros agendados.")
