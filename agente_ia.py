import json
import os
import time
from google import genai
from google.genai.errors import APIError

def carregar_dados_json():
    """Carrega os dados da partida do arquivo JSON local."""
    try:
        with open("partida.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Erro: O arquivo 'partida.json' não foi encontrado na pasta.")
        return None

def executar_agente_analista():
    client = genai.Client()

    dados = carregar_dados_json()
    if not dados:
        return

    evento = dados.get("event", {})
    
    time_casa = evento.get("homeTeam", {}).get("name", "Casa")
    time_fora = evento.get("awayTeam", {}).get("name", "Fora")
    gols_casa = evento.get("homeScore", {}).get("current", 0)
    gols_fora = evento.get("awayScore", {}).get("current", 0)
    estadio = evento.get("venue", {}).get("name", "Estádio desconhecido")
    arbitro = evento.get("referee", {}).get("name", "Árbitro não informado")

    prompt_completo = f"""
    Você é um analista de desempenho tático de futebol profissional e scout sênior. 
    Com base nos dados da partida fornecidos abaixo, elabore um relatório tático analítico, 
    elegante e profissional em Português do Brasil.

    Dados da Partida:
    - Mandante: {time_casa}
    - Visitante: {time_fora}
    - Placar Final: {time_casa} {gols_casa} x {gols_fora} {time_fora}
    - Estádio: {estadio}
    - Árbitro: {arbitro}

    Gere o relatório dividindo a análise entre:
    1. Resumo do Confronto e Dinâmica da Partida
    2. Impacto do Fator Casa e do Estádio
    3. Conclusão do Scout
    """

    print("🤖 O Agente de IA está a consultar a API do Google Gemini...")

    modelos_para_tentar = ['gemini-3.8-flash', 'gemini-flash-latest']
    sucesso = False
    tentativas_maximas = 3

    for modelo in modelos_para_tentar:
        for tentativa in range(1, tentativas_maximas + 1):
            try:
                resposta = client.models.generate_content(
                    model=modelo,
                    contents=prompt_completo,
                )

                print(f"\n==========================================")
                print(f"     RELATÓRIO TÁTICO (GEMINI - {modelo}) ")
                print(f"==========================================")
                print(resposta.text)
                print(f"==========================================")
                sucesso = True
                break

            except APIError as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    print(f"⚠️ [{tentativa}/{tentativas_maximas}] O modelo {modelo} está em alta demanda (503). Tentando novamente em 3 segundos...")
                    time.sleep(3)
                else:
                    print(f"❌ Erro na API do Gemini com {modelo}: {e}")
                    break
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
                break
        
        if sucesso:
            break

    if not sucesso:
        print("❌ Os servidores estão sob pico intenso de tráfego no momento. Tente rodar o comando novamente daqui a pouquinho.")

if __name__ == "__main__":
    executar_agente_analista()