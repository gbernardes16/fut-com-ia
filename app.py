import json
import os
import sys
from google import genai

DATA_DIR = "data"

def listar_partidas_disponiveis():
    """Lista todos os arquivos JSON de partidas disponíveis na pasta data/."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        return []
    
    arquivos = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]
    return arquivos

def carregar_dados_partida(nome_arquivo):
    """Carrega os dados da partida escolhida."""
    caminho = os.path.join(DATA_DIR, nome_arquivo)
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar o arquivo: {e}")
        return None

def executar_agente_analista(dados):
    """Envia os dados estruturados para o Agente de IA analisar."""
    client = genai.Client()

    info = dados.get("match_info", {})
    stats = dados.get("statistics", {})

    time_casa = info.get("homeTeam", {}).get("name", "Casa")
    time_fora = info.get("awayTeam", {}).get("name", "Fora")
    gols_casa = info.get("homeScore", 0)
    gols_fora = info.get("awayScore", 0)
    estadio = info.get("venue", {}).get("name", "Estádio desconhecido")
    arbitro = info.get("referee", {}).get("name", "Árbitro não informado")

    prompt_completo = f"""
    Você é um analista de desempenho tático de futebol profissional e scout sênior da Premier League. 
    Com base nos dados detalhados da partida fornecidos abaixo, elabore um relatório tático analítico, 
    elegante e profissional em Português do Brasil.

    Competição: {info.get('competition')} ({info.get('season')})
    Partida: {time_casa} {gols_casa} x {gols_fora} {time_fora}
    Estádio: {estadio}
    Árbitro: {arbitro}

    Estatísticas do Jogo:
    - Posse de Bola: {time_casa} {stats.get('possession', {}).get('home')} x {stats.get('possession', {}).get('away')} {time_fora}
    - Finalizações: {time_casa} {stats.get('shots', {}).get('home')} x {stats.get('shots', {}).get('away')} {time_fora}
    - Chutes no Alvo: {time_casa} {stats.get('shotsOnTarget', {}).get('home')} x {stats.get('shotsOnTarget', {}).get('away')} {time_fora}
    - Faltas Cometidas: {time_casa} {stats.get('fouls', {}).get('home')} x {stats.get('fouls', {}).get('fouls', {}).get('away')} {time_fora}
    - Cartões Amarelos: {time_casa} {stats.get('yellowCards', {}).get('home')} x {stats.get('yellowCards', {}).get('away')} {time_fora}

    Gere o relatório dividindo a análise entre:
    1. Resumo do Confronto e Dinâmica da Partida
    2. Análise Estatística (Posse, Finalizações e Disciplina)
    3. Impacto do Fator Casa e Arbitragem
    4. Conclusão do Scout
    """

    print("\n🤖 O Agente de IA está processando o relatório tático...")

    try:
        resposta = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt_completo,
        )

        print(f"\n==========================================")
        print(f"         RELATÓRIO TÁTICO - {time_casa} x {time_fora}         ")
        print(f"==========================================")
        print(resposta.text)
        print(f"==========================================")

    except Exception as e:
        print(f"❌ Erro ao conectar com a API do Gemini: {e}")

def main():
    print("==========================================")
    print("   SISTEMA DE ANÁLISE TÁTICA DE FUTEBOL   ")
    print("==========================================")
    
    arquivos = listar_partidas_disponiveis()
    
    if not arquivos:
        print("⚠️ Nenhuma partida encontrada na pasta 'data/'. Adicione arquivos JSON de partidas lá.")
        return

    print("\nPartidas disponíveis no banco de dados local:")
    for i, arquivo in enumerate(arquivos, 1):
        nome_amigavel = arquivo.replace(".json", "").replace("_", " ").title()
        print(f"[{i}] {nome_amigavel}")

    
    
    # Mantém apenas os números da string (ex: '1\r' vira '1')
    entrada = input("\nDigite o número da partida que deseja analisar: ").strip()

    try:
        escolha = int(entrada)
    except ValueError:
         print(f"Entrada inválida: {entrada!r}")
         return

    if 1 <= escolha <= len(arquivos):
            arquivo_selecionado = arquivos[escolha - 1]
            dados = carregar_dados_partida(arquivo_selecionado)
            if dados:
                executar_agente_analista(dados)
    else:
            print("❌ Opção inválida. Escolha um número da lista.")
        
if __name__ == "__main__":
    main()