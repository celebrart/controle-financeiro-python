import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestor Financeiro Inteligente", layout="wide")

st.title("💰 Planejador Financeiro Inteligente")
st.markdown("Organize sua renda e saiba exatamente quanto pode gastar.")

# Sidebar para entradas
st.sidebar.header("Configurações de Renda")
renda = st.sidebar.number_input("Sua Renda Líquida (R$)", min_value=0.0, value=3000.0)

# Colunas para organizar os campos
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Gastos e Dívidas")
    essenciais = st.number_input("Gastos Essenciais (Aluguel, Luz, etc)", min_value=0.0)
    dividas = st.number_input("Pagamento de Dívidas/Empréstimos", min_value=0.0)
    lazer = st.number_input("Gastos com Lazer/Desejos", min_value=0.0)

# Cálculos
total_gastos = essenciais + dividas + lazer
saldo = renda - total_gastos

# Regra 50-30-20
ideal_essencial = renda * 0.5
ideal_lazer = renda * 0.3
ideal_reserva = renda * 0.2

with col2:
    st.subheader("📊 Análise do Plano")
    if saldo < 0:
        st.error(f"Seu saldo está negativo em R$ {abs(saldo):.2f}")
    else:
        st.success(f"Saldo restante: R$ {saldo:.2f}")

    # Gráfico Comparativo
    dados_grafico = pd.DataFrame({
        'Categoria': ['Essenciais', 'Lazer', 'Dívidas/Reserva'],
        'Atual': [essenciais, lazer, dividas],
        'Recomendado (50-30-20)': [ideal_essencial, ideal_lazer, ideal_reserva]
    })
    st.bar_chart(dados_grafico.set_index('Categoria'))

st.divider()
st.info("💡 **Dica de Especialista:** Tente manter seus gastos essenciais abaixo de 50% da sua renda para garantir segurança financeira.")
