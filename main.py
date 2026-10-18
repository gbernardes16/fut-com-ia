import json

def carregar_dados_partida():
    # Abre e lê o arquivo JSON local
    try:
        with open("partida.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados
    except FileNotFoundError:
        print("Erro: O arquivo 'partida.json' não foi encontrado na pasta.")
        return None

def processar_estatisticas():
    dados = carregar_dados_partida()
    
    if not dados:
        return

    # Navegando pelo dicionário do JSON local
    evento = dados.get("event", {})
    
    time_casa = evento.get("homeTeam", {}).get("name", "Desconhecido")
    time_fora = evento.get("awayTeam", {}).get("name", "Desconhecido")
    
    gols_casa = evento.get("homeScore", {}).get("current", 0)
    gols_fora = evento.get("awayScore", {}).get("current", 0)
    
    estadio = evento.get("venue", {}).get("name", "Estádio não informado")
    arbitro = evento.get("referee", {}).get("name", "Árbitro não informado")

    print("--- RELATÓRIO DA PARTIDA (DADOS LOCAIS) ---")
    print(f"Confronto: {time_casa} {gols_casa} x {gols_fora} {time_fora}")
    print(f"Estádio: {estadio}")
    print(f"Árbitro da partida: {arbitro}")

# Executando a função
if __name__ == "__main__":
    processar_estatisticas()