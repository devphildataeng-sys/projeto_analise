import yfinance as yf
import pandas as pd

print("=========================================")
print("🤖 INICIANDO MÓDULO DE EXTRAÇÃO DA V1...")
print("=========================================")

# 1. Escolhendo a ação (Ticker) e definindo o período de análise
# Vamos puxar o histórico de 1 ano da Apple (AAPL)
ticker = "AAPL"
print(f"📥 Buscando dados históricos para: {ticker}...")
dados_acao = yf.Ticker(ticker)

# Extrai o histórico diário de 1 ano
historico = dados_acao.history(period="1y")

print("✅ Dados extraídos com sucesso!\n")

# 2. Mostrando a estrutura inicial dos dados
print("📋 Primeiras 5 linhas da tabela de dados extraída:")
print(historico[['Open', 'High', 'Low', 'Close', 'Volume']].head())
print("-" * 50)

# 3. CALCULANDO AS MÉTRICAS DO NÍVEL 1
print("📊 EXECUTANDO ANÁLISE ESTATÍSTICA DESCRITIVA:")

preco_maximo = historico['High'].max()
preco_minimo = historico['Low'].min()
media_fechamento = historico['Close'].mean()

print(f"📈 Preço Mais Alto no Ano:  USD {preco_maximo:.2f}")
print(f"📉 Preço Mais Baixo no Ano: USD {preco_minimo:.2f}")
print(f"⚖️  Preço Médio de Fechamento: USD {media_fechamento:.2f}")
print("=========================================")