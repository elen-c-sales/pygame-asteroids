"""
Classe Star - Estrela de fundo com efeito de profundidade
"""
import pygame
import random
from utils.cores import interpolar_cor


class Star:
    def __init__(self, x, y, profundidade, largura_tela=800, altura_tela=600):
        """
        Inicializa uma estrela com efeito de profundidade
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            profundidade: float de 0.2 a 0.8 (quanto maior, mais próxima)
            largura_tela: Largura da tela para wrap-around
            altura_tela: Altura da tela para wrap-around
        """
        self.x = x
        self.y = y
        self.profundidade = profundidade
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Tamanho baseado em profundidade
        # Estrelas distantes: 1px, Estrelas próximas: 2px
        if self.profundidade < 0.5:
            self.tamanho = 1
        else:
            self.tamanho = 2 if random.random() > 0.7 else 1
        
        # Cor interpolada (azul escuro -> branco)
        self.cor = interpolar_cor(profundidade)
        
        # Velocidade muito lenta para céu quase estático
        # Estrelas mais próximas se movem levemente mais rápido
        self.velocidade = 3 * self.profundidade  # Reduzido de 20 para 3
    
    def atualizar(self, dt, vel_nave=None):
        """
        Atualiza posição da estrela (movimento vertical e paralaxe com nave)
        
        Args:
            dt: Delta time em segundos
            vel_nave: pygame.math.Vector2 com velocidade da nave (opcional)
        """
        # Movimento base (scroll vertical lento)
        self.y += self.velocidade * dt
        
        # Efeito paralaxe baseado na velocidade da nave
        if vel_nave:
            # Estrelas se movem na direção oposta à nave
            # Quanto mais próxima (maior profundidade), mais se move
            fator_paralaxe = self.profundidade * 0.3  # 30% da velocidade da nave
            self.x -= vel_nave.x * fator_paralaxe * dt
            self.y -= vel_nave.y * fator_paralaxe * dt
        
        # Wrap-around: Se sair pela parte inferior, reaparece no topo
        if self.y > self.altura_tela:
            self.y = 0
            self.x = random.randint(0, self.largura_tela)
        elif self.y < 0:
            self.y = self.altura_tela
            self.x = random.randint(0, self.largura_tela)
        
        # Wrap horizontal (para o efeito paralaxe)
        if self.x > self.largura_tela:
            self.x = 0
        elif self.x < 0:
            self.x = self.largura_tela
    
    def desenhar(self, tela):
        """
        Desenha a estrela na tela
        
        Args:
            tela: Surface do Pygame onde desenhar
        """
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.tamanho)
