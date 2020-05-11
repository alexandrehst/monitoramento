import requests
from requests.auth import HTTPBasicAuth
import time
import random
from prometheus_client import start_http_server, Gauge, CollectorRegistry
from config import Configuracao

# Resposta da API. O número de servidores é variável
#[
#    {"target":"In Usage  - SRV01","sessions":131,"recordings":5},
#    {"target":"Available - SRV01","sessions":189,"recordings":7},
#    {"target":"In Usage  - SRV02","sessions":149,"recordings":7},
#    {"target":"Available - SRV02","sessions":171,"recordings":5}
#]

# url = "https://api.videoconferencia.soluti.com.br/monitor?q=global"

#Gauges para o exporter
SESSOES_EM_USO = Gauge('MONITOR_sessoes_em_uso', 'Total de sessões em uso')
GRAVACOES_EM_USO  = Gauge('MONITOR_gravacoes_em_uso', 'Total de slots de gravação em uso')
SESSOES_DISPONIVEIS = Gauge('MONITOR_sessoes_disponiveis', 'Total de slots disponíveis')
GRAVACOES_DISPONIVEIS  = Gauge('MONITOR_gravacoes_disponiveis', 'Total de slots de gravação disponíveis')

def coleta_dados(cfg):

    req = requests.get(cfg.url, auth = HTTPBasicAuth(cfg.usuario, cfg.senha))
    data = req.json()
    
    indicadores = [0,0,0,0]

    for i in range(0, len( data), 2):
        serv1 = i * 2
        serv2 = serv1 + 2

        indicadores[0] += data[i]['sessions']
        indicadores[1] += data[ i ]['recordings']
        indicadores[2] += data[i + 1]['sessions']
        indicadores[3] += data[ i+ 1 ]['recordings']

    exporta( cfg, *indicadores )

    time.sleep(cfg.tempo_de_atualizacao)


def exporta( cfg, sessao_em_uso, gravacao_em_uso, sessao_disponivel, gravacao_disponivel ):

    if (cfg.monitorar):
        SESSOES_EM_USO.set(sessao_em_uso)
        GRAVACOES_EM_USO.set(gravacao_em_uso)
        SESSOES_DISPONIVEIS.set(sessao_disponivel)
        GRAVACOES_DISPONIVEIS.set(gravacao_disponivel)

    else:
        print( sessao_em_uso, gravacao_em_uso, sessao_disponivel, gravacao_disponivel)
    

def liga_servidor(cfg):

    if (cfg.monitorar):
        start_http_server(8001)   


if __name__ == '__main__':
    
    cfg = Configuracao()
    cfg.carrega_config()
    liga_servidor(cfg)

    while True:
       coleta_dados(cfg)