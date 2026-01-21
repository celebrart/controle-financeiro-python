import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Finanças Pro - Estilo Mobills", layout="wide")

# Inicialização do "Banco de Dados" (Simulado na memória do navegador)
if 'agendamentos' not in st.session_state:
    st.session_state.agendamentos = []

st.title("🛡️ Finanças Pro: Análise & Calendário")

# --- BARRA LATERAL (CONFIGURAÇÕES) ---
st.sidebar.header("💰 Configurações")
renda = st.sidebar.number_input("Renda Líquida Mensal", min_value=0.0, value=3000.0)

# --- ABA DE NAVEGAÇÃO ---
aba1, aba2, aba3 = st.tabs(["📊 Análise Estilo Mobills", "📅 Calendário de Pagamentos", "⚙️ Cadastrar Despesa"])

with aba3:
    st.subheader("Cadastrar Nova Despesa/Pagamento")
    with st.form("nova_despesa"):
        nome_conta = st.text_input("Nome da Conta (ex: Aluguel, Netflix)")
        valor = st.number_input("Valor (R$)", min_value=0.0)
        categoria = st.selectbox("Categoria", ["Essencial", "Lazer", "Dívida", "Educação", "Reserva"])
        data_vencimento = st.date_input("Data de Vencimento", value=date.today())
        
        btn_salvar = st.form_submit_button("Agendar Pagamento")
        
        if btn_salvar:
            st.session_state.agendamentos.append({
                "Conta": nome_conta,
                "Valor": valor,
                "Categoria": categoria,
                "Data": data_vencimento,
                "Status": "Pendente" if data_vencimento > date.today() else "Vencido"
            })
            st.success("Lançamento realizado com sucesso!")

with aba1:
    st.subheader("🔍 Análise de Gastos")
    if st.session_state.agendamentos:
        df = pd.DataFrame(st.session_state.agendamentos)
        
        # Resumo Mobills
        total_gasto = df['Valor'].sum()
        saldo_restante = renda - total_gasto
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Gastos", f"R$ {total_gasto:.2f}")
        col2.metric("Saldo Restante", f"R$ {saldo_restante:.2f}", delta=f"{(saldo_restante/renda)*100:.1f}%")
        col3.metric("Nº de Contas", len(df))

        # Gráfico por Categoria
        st.write("### Gastos por Categoria")
        chart_data = df.groupby('Categoria')['Valor'].sum()
        st.bar_chart(chart_data)
        
        st.write("### Detalhes dos Lançamentos")
        st.table(df)
    else:
        st.info("Nenhuma despesa cadastrada ainda.")

with aba2:
    st.subheader("📅 Calendário de Compromissos")
    if st.session_state.agendamentos:
        hoje = date.today()
        proximos = [a for a in st.session_state.agendamentos if a['Data'] >= hoje]
        
        if proximos:
            for p in proximos:
                dias_para_vencer = (p['Data'] - hoje).days
                cor = "red" if dias_para_vencer <= 2 else "blue"
                st.markdown(f"🔔 **{p['Conta']}** - R$ {p['Valor']:.2f} - Vence em: :{cor}[{p['Data'].strftime('%d/%m/%Y')}] ({dias_para_vencer} dias)")
        else:
            st.write("Sem pagamentos futuros agendados.")
    else:
        st.write("O calendário está vazio.")
