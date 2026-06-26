# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
import pandas as pd
import numpy as np
import yfinance as yf

print("\n*****************************************\nANÁLISE DE TENDÊNCIA E VOLATILIDADE\n*****************************************")

ticker = "AAPL"
print(f"Buscando o histórico dos últimos 3 anos para: {ticker}...")
dados_da_acao = yf.Ticker(ticker)
historico = dados_da_acao.history(period="3y")
print(f"Dados coletados com Sucesso!\n")

#IDENTIFICANDO O ANO E CALCULANDOA VOLATILIDADE EM %

historico['ANO'] = historico.index.year

historico['DIARIO'] = historico['Close'].pct_change()*100

print("\n*****************************************\nRESULTADOS ANUAIS COMPLETOS\n*****************************************")

#LOOP PELOS ANOS SELECIONADOS

for ano in sorted(historico['ANO'].unique()):
    dados_por_ano = historico[historico['ANO'] == ano]

#ANÁLISE DE TENDÊNCIA(VALOR E DATA)

    maior_valor = dados_por_ano['High'].max()
    menor_valor = dados_por_ano['Low'].min()

    data_maior_valor = dados_por_ano['High'].idxmax().strftime('%d/%m/%Y')
    data_menor_valor = dados_por_ano['Low'] .idxmin().strftime('%d/%m/%Y')

    media_fechamento_anual = dados_por_ano['Close'].mean()

#ANÁLISE DE VOLATILIDADE(VALOR E DATA)

    retorno = dados_por_ano['DIARIO'].dropna()
    volat_anual = retorno.std() * np.sqrt(252)

    maior_alta = retorno.max()
    maior_queda = retorno.min()

    data_maior_alta = retorno.idxmax().strftime('%d/%m/%Y')
    data_maior_queda = retorno.idxmin().strftime('%d/%m/%Y')

#MOSTRANDO OS RESULTADOS ANUAIS NA TELA

    print(f"""ANO:{ano}
        Maior Valor: {maior_valor:.2f} em {data_maior_valor}
        Menor Valor: {menor_valor:.2f} em {data_menor_valor}
        Média de Fechamento: USD {media_fechamento_anual:.2f}
        Volatilidade Anualizada: {volat_anual:.2f}%
        Maior Alta Diária: {maior_alta:.2f} em {data_maior_alta}
        Maior Queda Diária: {maior_queda:.2f} em {data_maior_queda}
_____________________________________________________________________
    """)