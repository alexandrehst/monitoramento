import yaml

class Configuracao:

    def __init__(self):        
        self.url = ''
        self.tempo_de_atualizacao = 0
        self.usuario = ''
        self.senha = ''
        self.monitorar = True

    def carrega_config(self):
        with open("config.yaml") as ymlfile:
            cfg = yaml.load(ymlfile)

            self.url = cfg['api']['url']
            self.tempo_de_atualizacao = cfg['atualizacao']
            self.usuario = cfg['usuario']
            self.senha = cfg['senha']
            self.monitorar = cfg['monitorar']