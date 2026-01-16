"""
Classe Asteroid - Asteroide com efeito de profundidade 3D
"""
import pygame
import random
import math
from utils.cores import interpolar_cor


class Asteroid:
    # Tamanhos base para cada tipo
    TAMANHO_GRANDE = 40
    TAMANHO_MEDIO = 25
    TAMANHO_PEQUENO = 15
    
    def __init__(self, x, y, tamanho_tipo='grande', profundidade=None, velocidade_inicial=None):
        """
        Inicializa um asteroide
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            tamanho_tipo: 'grande', 'medio' ou 'pequeno'
            profundidade: float de 0.8 a 1.0 (None = aleatório)
            velocidade_inicial: pygame.math.Vector2 (None = aleatório)
        """
        self.pos = pygame.math.Vector2(x, y)
        self.tamanho_tipo = tamanho_tipo
        
        # Definir tamanho base
        if tamanho_tipo == 'grande':
            self.tamanho_base = self.TAMANHO_GRANDE
        elif tamanho_tipo == 'medio':
            self.tamanho_base = self.TAMANHO_MEDIO
        else:  # pequeno
            self.tamanho_base = self.TAMANHO_PEQUENO
        
        # Profundidade (asteroides usam 0.8-1.0 para ficarem "acima" das estrelas)
        if profundidade is None:
            self.profundidade = random.uniform(0.8, 1.0)
        else:
            self.profundidade = profundidade
        
        # Tamanho ajustado pela profundidade
        self.tamanho = int(self.tamanho_base * self.profundidade)
        self.raio_colisao = self.tamanho * 0.9  # Hitbox um pouco menor que o visual
        
        # Cor baseada na profundidade (azul claro -> branco)
        self.cor = interpolar_cor(self.profundidade)
        
        # Velocidade
        if velocidade_inicial is None:
            # Velocidade base depende do tamanho (menores são mais rápidos)
            if tamanho_tipo == 'grande':
                vel_base = random.uniform(30, 50)
            elif tamanho_tipo == 'medio':
                vel_base = random.uniform(40, 70)
            else:  # pequeno
                vel_base = random.uniform(60, 100)
            
            # Velocidade também afetada pela profundidade (mais próximo = mais rápido)
            vel_base *= self.profundidade
            
            # Direção aleatória
            angulo = random.uniform(0, 2 * math.pi)
            self.vel = pygame.math.Vector2(
                math.cos(angulo) * vel_base,
                math.sin(angulo) * vel_base
            )
        else:
            self.vel = velocidade_inicial.copy()
        
        # Rotação
        self.rotacao = random.uniform(0, 2 * math.pi)
        self.vel_rotacao = random.uniform(-2, 2)
        
        # Gerar forma irregular
        self.pontos = self.gerar_forma_irregular()
        
        self.vivo = True
    
    def gerar_forma_irregular(self):
        """
        Gera pontos para um polígono irregular (asteroide procedural)
        
        Returns:
            list: Lista de pygame.math.Vector2 com pontos locais
        """
        num_pontos = random.randint(8, 12)
        pontos = []
        
        for i in range(num_pontos):
            angulo = (2 * math.pi / num_pontos) * i
            # Variação aleatória no raio (70% a 130% do tamanho)
            variacao = random.uniform(0.7, 1.3)
            raio = self.tamanho * variacao
            
            x = raio * math.cos(angulo)
            y = raio * math.sin(angulo)
            pontos.append(pygame.math.Vector2(x, y))
        
        return pontos
    
    def atualizar(self, dt, largura_tela, altura_tela):
        """
        Atualiza posição e rotação
        
        Args:
            dt: Delta time em segundos
            largura_tela: Largura da tela
            altura_tela: Altura da tela
        """
        # Atualizar posição
        self.pos += self.vel * dt
        
        # Atualizar rotação
        self.rotacao += self.vel_rotacao * dt
        
        # Screen wrapping
        if self.pos.x > largura_tela + self.tamanho:
            self.pos.x = -self.tamanho
        elif self.pos.x < -self.tamanho:
            self.pos.x = largura_tela + self.tamanho
            
        if self.pos.y > altura_tela + self.tamanho:
            self.pos.y = -self.tamanho
        elif self.pos.y < -self.tamanho:
            self.pos.y = altura_tela + self.tamanho
    
    def get_pontos_rotacionados(self):
        """
        Retorna pontos do asteroide rotacionados para desenhar
        
        Returns:
            list: Lista de tuplas (x, y) para pygame.draw.polygon
        """
        pontos_rotacionados = []
        
        for ponto in self.pontos:
            # Rotacionar ponto
            x_rot = ponto.x * math.cos(self.rotacao) - ponto.y * math.sin(self.rotacao)
            y_rot = ponto.x * math.sin(self.rotacao) + ponto.y * math.cos(self.rotacao)
            
            # Adicionar posição do asteroide
            x_final = self.pos.x + x_rot
            y_final = self.pos.y + y_rot
            
            pontos_rotacionados.append((x_final, y_final))
        
        return pontos_rotacionados
    
    def fragmentar(self):
        """
        Fragmenta o asteroide em pedaços menores
        
        Returns:
            list: Lista de novos Asteroids menores (ou vazia se for pequeno)
        """
        fragmentos = []
        
        if self.tamanho_tipo == 'grande':
            # Gera 2 asteroides médios
            for _ in range(2):
                # Offset aleatório da posição
                offset_x = random.uniform(-20, 20)
                offset_y = random.uniform(-20, 20)
                
                # Velocidade aleatória, mas mais rápida que o original
                angulo = random.uniform(0, 2 * math.pi)
                vel_magnitude = self.vel.length() * random.uniform(1.2, 1.5)
                nova_vel = pygame.math.Vector2(
                    math.cos(angulo) * vel_magnitude,
                    math.sin(angulo) * vel_magnitude
                )
                
                frag = Asteroid(
                    self.pos.x + offset_x,
                    self.pos.y + offset_y,
                    'medio',
                    self.profundidade,  # Mantém a mesma profundidade
                    nova_vel
                )
                fragmentos.append(frag)
                
        elif self.tamanho_tipo == 'medio':
            # Gera 2 asteroides pequenos
            for _ in range(2):
                offset_x = random.uniform(-15, 15)
                offset_y = random.uniform(-15, 15)
                
                angulo = random.uniform(0, 2 * math.pi)
                vel_magnitude = self.vel.length() * random.uniform(1.3, 1.6)
                nova_vel = pygame.math.Vector2(
                    math.cos(angulo) * vel_magnitude,
                    math.sin(angulo) * vel_magnitude
                )
                
                frag = Asteroid(
                    self.pos.x + offset_x,
                    self.pos.y + offset_y,
                    'pequeno',
                    self.profundidade,
                    nova_vel
                )
                fragmentos.append(frag)
        
        # Pequenos não fragmentam (retorna lista vazia)
        return fragmentos
    
    def desenhar(self, tela):
        """
        Desenha o asteroide
        
        Args:
            tela: Surface do Pygame
        """
        if not self.vivo:
            return
        
        pontos = self.get_pontos_rotacionados()
        
        # Desenhar polígono (wireframe)
        pygame.draw.polygon(tela, self.cor, pontos, 2)
        
        # Desenhar hitbox (debug - descomente se quiser ver)
        # pygame.draw.circle(tela, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), int(self.raio_colisao), 1)
