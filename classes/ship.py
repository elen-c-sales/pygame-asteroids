"""
Classe Ship - Nave do jogador com física vetorial
"""
import pygame
import math


class Ship:
    def __init__(self, x, y, largura_tela, altura_tela):
        """
        Inicializa a nave do jogador
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            largura_tela: Largura da tela para screen wrapping
            altura_tela: Altura da tela para screen wrapping
        """
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.angulo = 0  # Em graus, 0 = apontando para cima
        
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        
        # Configurações de física
        self.aceleracao_thrust = 200  # pixels/s²
        self.velocidade_rotacao = 180  # graus/s
        self.friccao = 0.98  # Multiplicador de velocidade (inércia)
        self.vel_maxima = 300  # pixels/s
        
        # Configurações visuais
        self.tamanho = 15  # Raio da nave
        self.cor = (255, 255, 255)  # Branco
        self.raio_colisao = 12  # Para hitbox
        
        # Forma da nave (triângulo apontando para cima em coordenadas locais)
        self.forma_base = [
            pygame.math.Vector2(0, -self.tamanho),      # Ponta (frente)
            pygame.math.Vector2(-self.tamanho/2, self.tamanho/2),   # Base esquerda
            pygame.math.Vector2(self.tamanho/2, self.tamanho/2)     # Base direita
        ]
        
        # Estado
        self.viva = True
        self.pode_atirar = True
        self.cooldown_tiro = 0
        self.tempo_cooldown_tiro = 0.25  # segundos
    
    def rotacionar(self, direcao, dt):
        """
        Rotaciona a nave
        
        Args:
            direcao: -1 (esquerda) ou 1 (direita)
            dt: Delta time em segundos
        """
        self.angulo += self.velocidade_rotacao * direcao * dt
        self.angulo %= 360  # Manter entre 0-360
    
    def acelerar(self, dt):
        """
        Aplica thrust (aceleração) na direção que a nave está apontando
        
        Args:
            dt: Delta time em segundos
        """
        # Converter ângulo para radianos (Pygame usa 0° = direita, mas nosso 0° = cima)
        # Então ajustamos com -90°
        angulo_rad = math.radians(self.angulo - 90)
        
        # Criar vetor de aceleração baseado no ângulo
        aceleracao = pygame.math.Vector2(
            math.cos(angulo_rad) * self.aceleracao_thrust * dt,
            math.sin(angulo_rad) * self.aceleracao_thrust * dt
        )
        
        # Adicionar à velocidade
        self.vel += aceleracao
        
        # Limitar velocidade máxima
        if self.vel.length() > self.vel_maxima:
            self.vel.scale_to_length(self.vel_maxima)
    
    def atualizar(self, dt):
        """
        Atualiza posição e estado da nave
        
        Args:
            dt: Delta time em segundos
        """
        # Aplicar fricção (inércia)
        self.vel *= self.friccao
        
        # Atualizar posição
        self.pos += self.vel * dt
        
        # Screen wrapping (mundo infinito)
        self.check_bounds()
        
        # Cooldown do tiro
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= dt
            if self.cooldown_tiro <= 0:
                self.pode_atirar = True
    
    def check_bounds(self):
        """Screen wrapping - aparecer do outro lado quando sair da tela"""
        if self.pos.x > self.largura_tela:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = self.largura_tela
            
        if self.pos.y > self.altura_tela:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = self.altura_tela
    
    def get_pontos_rotacionados(self):
        """
        Retorna os pontos da nave rotacionados para desenhar
        
        Returns:
            list: Lista de pontos (x, y) para desenhar o polígono
        """
        angulo_rad = math.radians(self.angulo)
        pontos_rotacionados = []
        
        for ponto in self.forma_base:
            # Rotacionar ponto
            x_rot = ponto.x * math.cos(angulo_rad) - ponto.y * math.sin(angulo_rad)
            y_rot = ponto.x * math.sin(angulo_rad) + ponto.y * math.cos(angulo_rad)
            
            # Adicionar posição da nave
            x_final = self.pos.x + x_rot
            y_final = self.pos.y + y_rot
            
            pontos_rotacionados.append((x_final, y_final))
        
        return pontos_rotacionados
    
    def get_ponta_nave(self):
        """
        Retorna a posição da ponta da nave (para spawnar tiros)
        
        Returns:
            pygame.math.Vector2: Posição da ponta
        """
        angulo_rad = math.radians(self.angulo)
        ponta = self.forma_base[0]  # Primeiro ponto é a ponta
        
        # Rotacionar ponto
        x_rot = ponta.x * math.cos(angulo_rad) - ponta.y * math.sin(angulo_rad)
        y_rot = ponta.x * math.sin(angulo_rad) + ponta.y * math.cos(angulo_rad)
        
        return pygame.math.Vector2(self.pos.x + x_rot, self.pos.y + y_rot)
    
    def shoot(self):
        """
        Cria dados para um novo projétil
        
        Returns:
            dict ou None: Dados do projétil se pode atirar, None caso contrário
        """
        if not self.pode_atirar:
            return None
        
        # Preparar cooldown
        self.pode_atirar = False
        self.cooldown_tiro = self.tempo_cooldown_tiro
        
        # Calcular posição e velocidade do tiro
        ponta = self.get_ponta_nave()
        angulo_rad = math.radians(self.angulo - 90)
        
        velocidade_tiro = 400  # pixels/s
        vel_tiro = pygame.math.Vector2(
            math.cos(angulo_rad) * velocidade_tiro,
            math.sin(angulo_rad) * velocidade_tiro
        )
        
        # Adicionar velocidade da nave ao tiro
        vel_tiro += self.vel
        
        return {
            'pos': ponta.copy(),
            'vel': vel_tiro,
            'angulo': self.angulo
        }
    
    def desenhar(self, tela):
        """
        Desenha a nave na tela
        
        Args:
            tela: Surface do Pygame
        """
        if not self.viva:
            return
        
        pontos = self.get_pontos_rotacionados()
        
        # Desenhar nave (wireframe)
        pygame.draw.polygon(tela, self.cor, pontos, 2)
        
        # Desenhar círculo de colisão (debug - opcional)
        # pygame.draw.circle(tela, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.raio_colisao, 1)
    
    def desenhar_thrust(self, tela):
        """
        Desenha efeito visual de thrust (chama do motor)
        
        Args:
            tela: Surface do Pygame
        """
        if not self.viva:
            return
        
        angulo_rad = math.radians(self.angulo)
        
        # Pontos da base da nave (de onde sai o thrust)
        base_esquerda = self.forma_base[1]
        base_direita = self.forma_base[2]
        
        # Rotacionar e posicionar pontos da base
        pontos_base = []
        for ponto in [base_esquerda, base_direita]:
            x_rot = ponto.x * math.cos(angulo_rad) - ponto.y * math.sin(angulo_rad)
            y_rot = ponto.x * math.sin(angulo_rad) + ponto.y * math.cos(angulo_rad)
            pontos_base.append((self.pos.x + x_rot, self.pos.y + y_rot))
        
        # Ponto da chama (atrás da nave)
        comprimento_chama = self.tamanho * 0.8
        chama_offset = pygame.math.Vector2(0, comprimento_chama)
        
        x_chama = chama_offset.x * math.cos(angulo_rad) - chama_offset.y * math.sin(angulo_rad)
        y_chama = chama_offset.x * math.sin(angulo_rad) + chama_offset.y * math.cos(angulo_rad)
        
        ponto_chama = (self.pos.x + x_chama, self.pos.y + y_chama)
        
        # Desenhar triângulo da chama
        pontos_chama = [pontos_base[0], ponto_chama, pontos_base[1]]
        pygame.draw.polygon(tela, (255, 150, 0), pontos_chama, 0)  # Laranja
        pygame.draw.polygon(tela, (255, 255, 0), pontos_chama, 1)  # Contorno amarelo
