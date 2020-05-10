import requests
from requests.auth import HTTPBasicAuth
import time
import random
from prometheus_client import start_http_server, Gauge, CollectorRegistry

# Resposta da API. O número de servidores é variável
#[
#    {"target":"In Usage  - SRV01","sessions":131,"recordings":5},
#    {"target":"Available - SRV01","sessions":189,"recordings":7},
#    {"target":"In Usage  - SRV02","sessions":149,"recordings":7},
#    {"target":"Available - SRV02","sessions":171,"recordings":5}
#]

#Parâmetros da API
url = "https://api.videoconferencia.soluti.com.br/monitor?q=global"

tempo_de_atualizacao = 5 #tempo em segundos

#Gauges para o exporter
SESSOES_EM_USO = Gauge('MONITOR_sessoes_em_uso', 'Total de sessões em uso')
GRAVACOES_EM_USO  = Gauge('MONITOR_gravacoes_em_uso', 'Total de slots de gravação em uso')
SESSOES_DISPONIVEIS = Gauge('MONITOR_sessoes_disponiveis', 'Total de slots disponíveis')
GRAVACOES_DISPONIVEIS  = Gauge('MONITOR_gravacoes_disponiveis', 'Total de slots de gravação disponíveis')

#Autenticação
usuario = 'soluti'
senha = 'Soluti@2020!'

# Indica se irá ou não ligado o exporter. False quando em debug
monitorar = True

def coleta_dados():
    
    req = requests.get(url, auth = HTTPBasicAuth(usuario, senha))
    data = req.json()
    
    indicadores = [0,0,0,0]

    for i in range(0, len( data), 2):
        serv1 = i * 2
        serv2 = serv1 + 2

        indicadores[0] += data[i]['sessions']
        indicadores[1] += data[ i ]['recordings']
        indicadores[2] += data[i + 1]['sessions']
        indicadores[3] += data[ i+ 1 ]['recordings']

    exporta( *indicadores )

    time.sleep(tempo_de_atualizacao)


def exporta( sessao_em_uso, gravacao_em_uso, sessao_disponivel, gravacao_disponivel ):

    if (monitorar):
        SESSOES_EM_USO.set(sessao_em_uso)
        GRAVACOES_EM_USO.set(gravacao_em_uso)
        SESSOES_DISPONIVEIS.set(sessao_disponivel)
        GRAVACOES_DISPONIVEIS.set(gravacao_disponivel)

    else:
        print( sessao_em_uso, gravacao_em_uso, sessao_disponivel, gravacao_disponivel)
    

def liga_servidor():
    if (monitorar):
        start_http_server(8001)

if __name__ == '__main__':
    
    liga_servidor()

    while True:
       coleta_dados()