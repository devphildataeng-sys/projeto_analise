# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
import pandas as pd
import numpy as np
import yfinance as yf
import psycopg2 as pg

#INICIANDO CONEXÃO COM O BANCO DE DADOS

try: 
    conexao = pg.connect(
        host="172.17.0.1",
        database="db_analise_bolsa",
        user="phil",
        password="datana"
    )
    cursor = conexao.cursor()
    print("Conexão Realizada Com Sucesso!")
except Exception as error:
    print(f"Falha Ao Realizar Conexão: {error}")
    exit()

#CRIAÇÃO/ATUALIZAÇÃO DA TABELA NO BD

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dados_apple (
               id SERIAL PRIMARY KEY,
               ano INT UNIQUE,
               maior_valor NUMERIC(10,2),
               menor_valor NUMERIC(10,2),
               data_maior_valor VARCHAR(10),
               data_menor_valor VARCHAR(10),
               media_fechamento_anual NUMERIC(10,2),
               volat_anual NUMERIC(10,2),
               maior_alta NUMERIC(10,2),
               maior_queda NUMERIC(10,2),
               data_maior_alta VARCHAR(10),
               data_maior_queda VARCHAR(10)
    );
""")

conexao.commit()
print("Tabela 'dados_apple' verificada/criada")

print("\n*****************************************\nANÁLISE DE TENDÊNCIA E VOLATILIDADE\n*****************************************")

ticker = "AAPL"
print(f"Buscando o histórico dos últimos 3 anos para: {ticker}...")
dados_da_acao = yf.Ticker(ticker)
historico = dados_da_acao.history(period="3y")
# print(f"Dados coletados com Sucesso!\n")

#IDENTIFICANDO O ANO E CALCULANDO A VOLATILIDADE EM %

historico['ANO'] = historico.index.year

historico['DIARIO'] = historico['Close'].pct_change()*100

print("\n*****************************************\nRESULTADOS ANUAIS COMPLETOS\n*****************************************")

#LOOP PELOS ANOS SELECIONADOS

for ano_raw in sorted(historico['ANO'].unique()):
    ano = int(ano_raw)
    dados_por_ano = historico[historico['ANO'] == ano]

#ANÁLISE DE TENDÊNCIA(VALOR E DATA)

    maior_valor = float(dados_por_ano['High'].max())
    menor_valor = float(dados_por_ano['Low'].min())

    data_maior_valor = dados_por_ano['High'].idxmax().strftime('%d/%m/%Y')
    data_menor_valor = dados_por_ano['Low'] .idxmin().strftime('%d/%m/%Y')

    media_fechamento_anual = float(dados_por_ano['Close'].mean())

#ANÁLISE DE VOLATILIDADE(VALOR E DATA)

    retorno = dados_por_ano['DIARIO'].dropna()
    volat_anual = float(retorno.std() * np.sqrt(252))

    maior_alta = float(retorno.max())
    maior_queda = float(retorno.min())

    data_maior_alta = retorno.idxmax().strftime('%d/%m/%Y')
    data_maior_queda = retorno.idxmin().strftime('%d/%m/%Y')

#INSERINDO/ATUALIZANDO INFORMAÇÕES NO BANCO DE DADOS

    cursor.execute("""
        INSERT INTO dados_apple (
                   ano,
                   maior_valor,
                   menor_valor,
                   data_maior_valor,
                   data_menor_valor,
                   media_fechamento_anual,
                   volat_anual,
                   maior_alta,
                   maior_queda,
                   data_maior_alta,
                   data_maior_queda        
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON CONFLICT (ano) DO UPDATE SET
                   maior_valor = EXCLUDED.maior_valor,
                   menor_valor = EXCLUDED.menor_valor,
                   data_maior_valor = EXCLUDED.data_maior_valor,
                   data_menor_valor = EXCLUDED.data_menor_valor,
                   media_fechamento_anual = EXCLUDED.media_fechamento_anual,
                   volat_anual = EXCLUDED.volat_anual,
                   maior_alta = EXCLUDED.maior_alta,
                   maior_queda = EXCLUDED.maior_queda,
                   data_maior_alta = EXCLUDED.data_maior_alta,
                   data_maior_queda = EXCLUDED.data_maior_queda;       
    """, (
            ano,
            maior_valor,
            menor_valor,
            data_maior_valor,
            data_menor_valor,
            media_fechamento_anual,
            volat_anual,
            maior_alta,
            maior_queda,
            data_maior_alta,
            data_maior_queda 
    ))

    print(f"Ano {ano} processado e carregado com sucesso!")

    # MOSTRANDO OS RESULTADOS ANUAIS NA TELA
    print(f"""
        ANO: {ano}
        Maior Valor: USD {maior_valor:.2f} em {data_maior_valor}
        Menor Valor: USD {menor_valor:.2f} em {data_menor_valor}
        Média de Fechamento: USD {media_fechamento_anual:.2f}
        Volatilidade Anualizada: {volat_anual:.2f}%
        Maior Alta Diária: {maior_alta:+.2f}% em {data_maior_alta}
        Maior Queda Diária: {maior_queda:.2f}% em {data_maior_queda}
_____________________________________________________________________""")

#ENCERRANDO A CONEXÃO

conexao.commit()
cursor.close()
conexao.close()
