import pygame
import os #Função os ajuda a importar arquivos ,,,,,,,,,,,,,,

import random

TELA_LARGURA = 500 # Largura da tela
TELA_ALTURA = 800 # altura da tela

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))  #Importa a imagem para o jogo
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),#Importa as imagens do passaro que serao modificadas em foram de lista
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png'))),
]

pygame.font.init() #texto que define a pontuação no jogo
FONTE_PONTOS = pygame.font.SysFont('arial',50) #define a fonte e o tamanho que ira entrar no texto



class Passaro: #criando classes para cada objeto
    IMGS = IMAGENS_PASSARO
    # animações de rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMCAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0 #começa zerado
        self.altura = sef.y # a altura do passaro sera a posição dele no eixo Y
        self.tempo = 0
        self.contagem_imagem = 0 # para saber qual imagem do passaro sera usada
        self.imagem = self.IMGS[0]

    def pular(self): #Movimentos de pulo
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y #a altura que ele esta  é posição y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2 ) + self.velocidade * self.tempo #formula do sorvetao para fazaer o movimento de queda S = so+vot+at²/2x'

        # Retringir o deslocamento
        if deslocamento > 16: #16 pixels
            deslocamento = 16 #deslocamento maximo a ser feito é de 16
        elif deslocamento < 0:
            deslocamento -= 2 #ira dar um ganho extra no pulo do passaro
        self.y += deslocamento # Movimentar o passaro

        #o angulo do passaro
        if deslocamento < 0 or self.y < (self.altura * 50): #Ira manter a animação do passaro ao pular
             if self.angulo < self.ROTACAO_MAXIMA:
                 self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > - 90:
                self.angulo -= self.VELOCIDADE_ROTACAO
    def desenhar(self, tela):
        #Definir qual imagem do passaro vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMCAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMCAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMCAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMCAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMCAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o passaro tiver caindo eu nao vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMCAO*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo) # Ira fazer a rotação do passaro
        pos_centro_imagem = self.imagem.get_rect(toplef=(self.x, self.y)).center # ira posicionar a imagem no centro
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem) # ira fazer um retangulo em volta da imagem para fazer o movimento de rotação
        tela.blit(imagem_rotacionada, retangulo.topleft) # ira desenhar o retangulo na posição em que vc deseja

    def get_mask(self): #ira pegar o o retangulo e subdividir em varios retangulos menores
        pygame.mask.from_surface(self.imagem) #ira avaliar se no micro rentangulo existem img do passaro e do cano



class Cano:
    DISTANCIA = 200 # 200 PIXELS
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x # qual posição do eixo x ele vai estar
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True) # ira inverter a imagem do cano no eixo Y pois esta como True
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False # definir se o passaro passou pelo cano ou nao
        self.definir_altura() #ira definir em que altura os canos serao gerados

    def definir_altura(self):
        self.altura = random.randrange(50, 450) # Ira randomizar a posição da altura do cano em um range de 50 a 450
        self.pos_base = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE # para mover o cano em direção ao passarox

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mas = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(base_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)  #função para verificar se existe alguma colisao entre os pixels  do passaro e do cano

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    pass
