def calcular_plano_financeiro():
    print("--- SISTEMA DE CONTROLE FINANCEIRO INTELIGENTE ---")
    
    # Entradas do Usuário
    renda = float(input("Digite sua renda mensal líquida (R$): "))
    
    print("\n--- CADASTRO DE GASTOS FIXOS (Aluguel, Luz, Internet) ---")
    essenciais = float(input("Total de gastos essenciais (R$): "))
    
    print("\n--- CADASTRO DE DÍVIDAS (Cartão, Empréstimos) ---")
    dividas = float(input("Total mensal destinado a pagar dívidas (R$): "))

    # Lógica de Separação (Regra 50-30-20 adaptada)
    # 50% Essencial, 20% Dívidas/Reserva, 30% Estilo de Vida
    limite_essencial = renda * 0.50
    limite_lazer = renda * 0.30
    
    saldo_apos_essencial = renda - essenciais
    saldo_final = saldo_apos_essencial - dividas
    
    # Análise Inteligente
    print("\n" + "="*30)
    print("RELATÓRIO DE SAÚDE FINANCEIRA")
    print("="*30)
    
    print(f"Renda Total: R$ {renda:.2f}")
    print(f"Gastos Essenciais: R$ {essenciais:.2f} ({(essenciais/renda)*100:.1f}% da renda)")
    
    if essenciais > limite_essencial:
        print("⚠️ ALERTA: Seus gastos essenciais estão acima de 50%. Tente reduzir contas fixas.")
    
    print(f"Dívidas Cadastradas: R$ {dividas:.2f}")
    print(f"Valor Restante para Lazer/Estilo de Vida: R$ {saldo_final:.2f}")
    
    if saldo_final < 0:
        print("❌ CRÍTICO: Seu orçamento está negativo! Você está acumulando novas dívidas.")
    elif saldo_final < limite_lazer:
        print(f"💡 DICA: Você tem R$ {saldo_final:.2f} para lazer. Está abaixo do recomendado, mas seguro.")
    else:
        valor_investimento = saldo_final - limite_lazer
        print(f"✅ EXCELENTE: Você pode gastar R$ {limite_lazer:.2f} com lazer e ainda investir R$ {valor_investimento:.2f}.")

if __name__ == "__main__":
    calcular_plano_financeiro()

