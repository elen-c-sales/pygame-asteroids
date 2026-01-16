"""
Classe Bullet - Projétil disparado pela nave
"""
import pygame


class Bullet:
    def __init__(self, pos, vel, angulo):
        """
        Inicializa um projétil
        
        Args:
            pos: pygame.math.Vector2 com posição inicial
            vel: pygame.math.Vector2 com velocidade
            angulo: Ângulo de disparo (para efeitos visuais)
        """
        self.pos = pos.copy()
        self.vel = vel.copy()
        self.angulo = angulo
        
        # Configurações
        self.raio = 2  # Raio do projétil
        self.cor = (255, 255, 255)  # Branco
        self.tempo_vida_max = 1.5  # segundos
        self.tempo_vida = self.tempo_vida_max
        self.vivo = True
    
    def atualizar(self, dt, largura_tela, altura_tela):
        """
        Atualiza posição e estado do projétil
        
        Args:
            dt: Delta time em segundos
            largura_tela: Largura da tela
            altura_tela: Altura da tela
        """
        # Atualizar posição
        self.pos += self.vel * dt
        
        # Destruir se sair da tela (sem screen wrapping, como no Asteroids clássico)
        if (self.pos.x < 0 or self.pos.x > largura_tela or 
            self.pos.y < 0 or self.pos.y > altura_tela):
            self.vivo = False
        
        # Reduzir tempo de vida
        self.tempo_vida -= dt
        if self.tempo_vida <= 0:
            self.vivo = False
    
    def desenhar(self, tela):
        """
        Desenha o projétil
        
        Args:
            tela: Surface do Pygame
        """
        if not self.vivo:
            return
        
        # Desenhar como círculo pequeno
        pygame.draw.circle(tela, self.cor, (int(self.pos.x), int(self.pos.y)), self.raio)
