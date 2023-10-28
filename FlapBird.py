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

