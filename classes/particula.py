"""
Classe Particula - Efeito de explosão
"""
import pygame
import random
import math


class Particula:
    def __init__(self, x, y, cor, velocidade_base=100):
        """
        Inicializa uma partícula de explosão
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            cor: Cor da partícula (RGB)
            velocidade_base: Velocidade base das partículas
        """
        self.pos = pygame.math.Vector2(x, y)
        
        # Direção aleatória
        angulo = random.uniform(0, 2 * math.pi)
        velocidade = random.uniform(velocidade_base * 0.5, velocidade_base * 1.5)
        
        self.vel = pygame.math.Vector2(
            math.cos(angulo) * velocidade,
            math.sin(angulo) * velocidade
        )
        
        self.cor = cor
        self.tamanho = random.randint(2, 4)
        self.tempo_vida_max = random.uniform(0.3, 0.8)
        self.tempo_vida = self.tempo_vida_max
        self.viva = True
    
    def atualizar(self, dt):
        """
        Atualiza posição e estado da partícula
        
        Args:
            dt: Delta time em segundos
        """
        # Atualizar posição
        self.pos += self.vel * dt
        
        # Desacelerar (fricção)
        self.vel *= 0.95
        
        # Reduzir tempo de vida
        self.tempo_vida -= dt
        if self.tempo_vida <= 0:
            self.viva = False
    
    def desenhar(self, tela):
        """
        Desenha a partícula com fade out
        
        Args:
            tela: Surface do Pygame
        """
        if not self.viva:
            return
        
        # Calcular alpha baseado no tempo de vida restante
        alpha = int(255 * (self.tempo_vida / self.tempo_vida_max))
        
        # Garantir que a cor tenha valores inteiros válidos
        r = int(self.cor[0])
        g = int(self.cor[1])
        b = int(self.cor[2])
        
        # Criar surface com alpha
        particula_surface = pygame.Surface((self.tamanho * 2, self.tamanho * 2), pygame.SRCALPHA)
        cor_com_alpha = (r, g, b, alpha)
        pygame.draw.circle(particula_surface, cor_com_alpha, (self.tamanho, self.tamanho), self.tamanho)
        
        tela.blit(particula_surface, (int(self.pos.x - self.tamanho), int(self.pos.y - self.tamanho)))


def criar_explosao(x, y, cor, num_particulas=20, velocidade=150):
    """
    Cria uma explosão de partículas
    
    Args:
        x: Posição X da explosão
        y: Posição Y da explosão
        cor: Cor base das partículas
        num_particulas: Número de partículas a criar
        velocidade: Velocidade base das partículas
    
    Returns:
        list: Lista de Particulas
    """
    particulas = []
    
    for _ in range(num_particulas):
        # Variação de cor para efeito mais interessante
        # Garantir que valores fiquem entre 0-255
        cor_variada = (
            max(0, min(255, int(cor[0]) + random.randint(-30, 30))),
            max(0, min(255, int(cor[1]) + random.randint(-30, 30))),
            max(0, min(255, int(cor[2]) + random.randint(-30, 30)))
        )
        particulas.append(Particula(x, y, cor_variada, velocidade))
    
    return particulas
