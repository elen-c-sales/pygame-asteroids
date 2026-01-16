"""
Classe ShipDebris - Pedaços da nave (debris) quando explode
"""
import pygame
import random
import math


class ShipDebris:
    def __init__(self, x, y, pontos_linha, angulo_nave):
        """
        Inicializa um pedaço (linha) da nave explodida
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            pontos_linha: Tupla com (ponto1, ponto2) - os dois vértices da linha
            angulo_nave: Ângulo da nave no momento da explosão
        """
        self.pos = pygame.math.Vector2(x, y)
        
        # Armazenar os pontos da linha em coordenadas locais
        self.ponto1 = pygame.math.Vector2(pontos_linha[0])
        self.ponto2 = pygame.math.Vector2(pontos_linha[1])
        
        # Velocidade aleatória para esse pedaço
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(80, 150)
        self.vel = pygame.math.Vector2(
            math.cos(angulo) * velocidade,
            math.sin(angulo) * velocidade
        )
        
        # Rotação do pedaço
        self.angulo = angulo_nave
        self.vel_rotacao = random.uniform(-5, 5)
        
        self.cor = (255, 255, 255)  # Branco
        self.tempo_vida_max = 1.0
        self.tempo_vida = self.tempo_vida_max
        self.viva = True
    
    def atualizar(self, dt):
        """Atualiza posição e rotação do debris"""
        self.pos += self.vel * dt
        self.angulo += self.vel_rotacao * dt
        self.vel *= 0.97  # Desacelerar
        
        self.tempo_vida -= dt
        if self.tempo_vida <= 0:
            self.viva = False
    
    def desenhar(self, tela):
        """Desenha o pedaço da nave"""
        if not self.viva:
            return
        
        # Calcular alpha para fade out
        alpha_factor = self.tempo_vida / self.tempo_vida_max
        
        # Rotacionar e transladar os pontos
        angulo_rad = math.radians(self.angulo)
        cos_a = math.cos(angulo_rad)
        sin_a = math.sin(angulo_rad)
        
        # Ponto 1 rotacionado
        x1 = self.ponto1.x * cos_a - self.ponto1.y * sin_a + self.pos.x
        y1 = self.ponto1.x * sin_a + self.ponto1.y * cos_a + self.pos.y
        
        # Ponto 2 rotacionado
        x2 = self.ponto2.x * cos_a - self.ponto2.y * sin_a + self.pos.x
        y2 = self.ponto2.x * sin_a + self.ponto2.y * cos_a + self.pos.y
        
        # Desenhar a linha com fade (ajustando cor)
        if alpha_factor < 1.0:
            cor = tuple(int(c * alpha_factor) for c in self.cor)
        else:
            cor = self.cor
        
        pygame.draw.line(tela, cor, (int(x1), int(y1)), (int(x2), int(y2)), 2)


def criar_explosao_nave(nave):
    """
    Cria os pedaços da nave explodida
    
    Args:
        nave: Objeto Ship
    
    Returns:
        list: Lista de ShipDebris
    """
    debris_list = []
    
    # Pegar os 3 pontos do triângulo da nave
    pontos = nave.forma_base
    
    # Criar 3 linhas (os 3 lados do triângulo)
    linhas = [
        (pontos[0], pontos[1]),  # Frente para base esquerda
        (pontos[1], pontos[2]),  # Base esquerda para base direita
        (pontos[2], pontos[0])   # Base direita para frente
    ]
    
    # Criar um debris para cada linha
    for linha in linhas:
        debris = ShipDebris(nave.pos.x, nave.pos.y, linha, nave.angulo)
        debris_list.append(debris)
    
    return debris_list
