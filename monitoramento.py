import requests
from requests.auth import HTTPBasicAuth
import time
import random
from prometheus_client import start_http_server, Gauge, CollectorRegistry
from config import Configuracao

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
        indicadores[0] += data[i]['sessions']
        indicadores[1] += data[ i ]['recordings']
        indicadores[2] += data[i + 1]['sessions']
        indicadores[3] += data[ i+ 1 ]['recordings']

    return indicadores

def exporta( cfg, sessao_em_uso, gravacao_em_uso, sessao_disponivel, gravacao_disponivel ):

    SESSOES_EM_USO.set(sessao_em_uso)
    GRAVACOES_EM_USO.set(gravacao_em_uso)
    SESSOES_DISPONIVEIS.set(sessao_disponivel)
    GRAVACOES_DISPONIVEIS.set(gravacao_disponivel)

    

def liga_servidor(cfg):

    if (cfg.monitorar):
        start_http_server(8001)   

def imprimir(indicadores, contadores):

    # atualização dos indicadores para print na tela
    contadores[0] += 1 # cont
    contadores[1] = indicadores[1] if indicadores[1] >  contadores[1] else  contadores[1] # contadores[1] = gravaçoes maximas
    contadores[2] += indicadores[1] #Contadores[2] = gravaçoes totais
    contadores[3] = contadores[2] // contadores[0] # contadores[3] = gravacoes media

    texto = "  {0}  {1}  |  {2}  {3}  |  ".format( indicadores[0], indicadores[1], indicadores[2], indicadores[3])
    texto += '{0}  '.format(contadores[1])
    texto += '{0}  '.format(contadores[3])
    texto += '{0}'.format(contadores[0])
    texto += '\r'

    #sys.stdout.write( texto )
    #sys.stdout.flush()
    print(texto, end='')

if __name__ == '__main__':
    
    cfg = Configuracao()
    cfg.carrega_config()
    liga_servidor(cfg)

    # Globais
    contadores = [0,0,0,0]

    if not cfg.monitorar:
        print(" -- USO --  -- DISP--   -- STATS --\n  S   G      S     G      Mx  Md  Ct")

    while True:
        indicadores = coleta_dados(cfg)
        if (cfg.monitorar):       
            exporta( cfg, *indicadores )
        else:
            imprimir(indicadores, contadores)

        time.sleep(cfg.tempo_de_atualizacao)