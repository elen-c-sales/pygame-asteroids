"""
Asteroids 3D - Jogo com efeito de profundidade usando Pygame
Inspirado no clássico Atari com visual moderno de paralaxe

VERSÃO WEB - Compilada com Pygbag para rodar no navegador
"""
import asyncio
import pygame
import random
from classes.star import Star
from utils.cores import COR_FUNDO


# Configurações da tela
LARGURA = 800
ALTURA = 600
FPS = 60

# Configurações do starfield
NUM_ESTRELAS = 300
PROF_MIN = 0.15
PROF_MAX = 0.75


def criar_estrelas():
    """Cria campo de estrelas com diferentes profundidades"""
    estrelas = []
    for _ in range(NUM_ESTRELAS):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        profundidade = random.uniform(PROF_MIN, PROF_MAX)
        estrelas.append(Star(x, y, profundidade, LARGURA, ALTURA))
    return estrelas


async def main():
    """Loop principal do jogo"""
    # Inicialização
    pygame.init()
    pygame.mixer.init()
    
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Asteroids 3D - Efeito de Profundidade")
    clock = pygame.time.Clock()
    
    # Carregar sons
    try:
        som_tiro = pygame.mixer.Sound("assets/tiro2.wav")
        som_explosao_asteroide = pygame.mixer.Sound("assets/explode4.wav")
        som_explosao_nave = pygame.mixer.Sound("assets/explode1.wav")
        
        som_tiro.set_volume(0.3)
        som_explosao_asteroide.set_volume(0.5)
        som_explosao_nave.set_volume(0.7)
        
        sons_carregados = True
    except:
        print("Aviso: Não foi possível carregar os arquivos de som.")
        sons_carregados = False
    
    # Criar campo de estrelas
    estrelas = criar_estrelas()
    
    # Criar nave do jogador
    from classes.ship import Ship
    from classes.bullet import Bullet
    from classes.asteroid import Asteroid
    from classes.particula import Particula, criar_explosao
    from classes.ship_debris import ShipDebris, criar_explosao_nave
    from utils.fisica import checar_colisao_circular
    
    nave = Ship(LARGURA // 2, ALTURA // 2, LARGURA, ALTURA)
    projeteis = []
    asteroides = []
    particulas = []
    ship_debris = []
    
    # Criar asteroides iniciais
    def spawn_asteroide(tamanho='grande'):
        """Spawna um asteroide na borda da tela"""
        borda = random.choice(['cima', 'baixo', 'esquerda', 'direita'])
        
        if borda == 'cima':
            x = random.randint(0, LARGURA)
            y = -50
        elif borda == 'baixo':
            x = random.randint(0, LARGURA)
            y = ALTURA + 50
        elif borda == 'esquerda':
            x = -50
            y = random.randint(0, ALTURA)
        else:  # direita
            x = LARGURA + 50
            y = random.randint(0, ALTURA)
        
        return Asteroid(x, y, tamanho)
    
    # Spawnar asteroides iniciais
    for _ in range(4):
        asteroides.append(spawn_asteroide('grande'))
    
    # Game state
    pontos = 0
    vidas = 3
    tempo_spawn = 0
    intervalo_spawn = 4.0
    estado_jogo = 'jogando'
    pontuacao_final = 0
    
    # Sistema de dificuldade progressiva
    nivel = 1
    pontos_por_nivel = 500
    
    def calcular_dificuldade():
        """Calcula o nível atual baseado na pontuação"""
        return (pontos // pontos_por_nivel) + 1
    
    def get_multiplicador_velocidade():
        """Retorna multiplicador de velocidade baseado no nível"""
        return 1.0 + (nivel - 1) * 0.15
    
    def get_intervalo_spawn():
        """Retorna intervalo de spawn baseado no nível"""
        return max(1.5, 4.0 - (nivel - 1) * 0.3)
    
    def get_max_asteroides():
        """Retorna número máximo de asteroides baseado no nível"""
        return min(15, 8 + (nivel - 1) * 1)
    
    def resetar_jogo():
        """Reseta o jogo para um novo round"""
        nonlocal pontos, vidas, asteroides, projeteis, nave, tempo_spawn, estado_jogo, particulas, ship_debris, nivel
        
        pontos = 0
        vidas = 3
        tempo_spawn = 0
        estado_jogo = 'jogando'
        nivel = 1
        
        nave.pos = pygame.math.Vector2(LARGURA // 2, ALTURA // 2)
        nave.vel = pygame.math.Vector2(0, 0)
        nave.angulo = 0
        nave.viva = True
        
        asteroides.clear()
        projeteis.clear()
        particulas.clear()
        ship_debris.clear()
        for _ in range(4):
            asteroides.append(spawn_asteroide('grande'))
    
    # Controles
    teclas_pressionadas = {
        'esquerda': False,
        'direita': False,
        'cima': False,
        'espaco': False
    }
    
    # Loop principal
    rodando = True
    while rodando:
        dt = clock.tick(FPS) / 1000.0
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                    
                elif evento.key == pygame.K_RETURN and estado_jogo == 'game_over':
                    resetar_jogo()
                
                elif estado_jogo == 'jogando':
                    if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                        teclas_pressionadas['esquerda'] = True
                    elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                        teclas_pressionadas['direita'] = True
                    elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                        teclas_pressionadas['cima'] = True
                    elif evento.key == pygame.K_SPACE:
                        teclas_pressionadas['espaco'] = True
                    
            elif evento.type == pygame.KEYUP and estado_jogo == 'jogando':
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas_pressionadas['esquerda'] = False
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas_pressionadas['direita'] = False
                elif evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas_pressionadas['cima'] = False
                elif evento.key == pygame.K_SPACE:
                    teclas_pressionadas['espaco'] = False
        
        # Processar apenas se estiver jogando
        if estado_jogo == 'jogando':
            if teclas_pressionadas['esquerda']:
                nave.rotacionar(-1, dt)
            if teclas_pressionadas['direita']:
                nave.rotacionar(1, dt)
            if teclas_pressionadas['cima']:
                nave.acelerar(dt)
            if teclas_pressionadas['espaco']:
                dados_tiro = nave.shoot()
                if dados_tiro:
                    projeteis.append(Bullet(dados_tiro['pos'], dados_tiro['vel'], dados_tiro['angulo']))
                    if sons_carregados:
                        som_tiro.play()
        
            for estrela in estrelas:
                estrela.atualizar(dt, nave.vel)
            
            nave.atualizar(dt)
            
            for projetil in projeteis[:]:
                projetil.atualizar(dt, LARGURA, ALTURA)
                if not projetil.vivo:
                    projeteis.remove(projetil)
            
            for asteroide in asteroides[:]:
                asteroide.atualizar(dt, LARGURA, ALTURA)
            
            nivel_anterior = nivel
            nivel = calcular_dificuldade()
            
            if nivel > nivel_anterior and nivel > 1:
                pass
            
            intervalo_atual = get_intervalo_spawn()
            max_asteroides_atual = get_max_asteroides()
            multiplicador_vel = get_multiplicador_velocidade()
            
            tempo_spawn += dt
            if tempo_spawn >= intervalo_atual and len(asteroides) < max_asteroides_atual:
                novo_asteroide = spawn_asteroide('grande')
                novo_asteroide.vel *= multiplicador_vel
                asteroides.append(novo_asteroide)
                tempo_spawn = 0
            
            for projetil in projeteis[:]:
                if not projetil.vivo:
                    continue
                    
                for asteroide in asteroides[:]:
                    if not asteroide.vivo:
                        continue
                    
                    if checar_colisao_circular(projetil.pos, projetil.raio, asteroide.pos, asteroide.raio_colisao):
                        projetil.vivo = False
                        asteroide.vivo = False
                        
                        particulas.extend(criar_explosao(
                            asteroide.pos.x, 
                            asteroide.pos.y, 
                            asteroide.cor, 
                            num_particulas=15,
                            velocidade=100
                        ))
                        
                        if sons_carregados:
                            som_explosao_asteroide.play()
                        
                        if asteroide.tamanho_tipo == 'grande':
                            pontos += int(20 * asteroide.profundidade)
                        elif asteroide.tamanho_tipo == 'medio':
                            pontos += int(50 * asteroide.profundidade)
                        else:
                            pontos += int(100 * asteroide.profundidade)
                        
                        fragmentos = asteroide.fragmentar()
                        asteroides.extend(fragmentos)
                        
                        break
            
            if nave.viva:
                for asteroide in asteroides[:]:
                    if not asteroide.vivo:
                        continue
                    
                    if checar_colisao_circular(nave.pos, nave.raio_colisao, asteroide.pos, asteroide.raio_colisao):
                        nave.viva = False
                        vidas -= 1
                        
                        ship_debris.extend(criar_explosao_nave(nave))
                        
                        if sons_carregados:
                            som_explosao_nave.play()
                        
                        if vidas <= 0:
                            estado_jogo = 'game_over'
                            pontuacao_final = pontos
                        else:
                            nave.pos = pygame.math.Vector2(LARGURA // 2, ALTURA // 2)
                            nave.vel = pygame.math.Vector2(0, 0)
                            nave.viva = True
            
            asteroides = [a for a in asteroides if a.vivo]
            projeteis = [p for p in projeteis if p.vivo]
            
            for particula in particulas[:]:
                particula.atualizar(dt)
            particulas = [p for p in particulas if p.viva]
            
            for debris in ship_debris[:]:
                debris.atualizar(dt)
            ship_debris = [d for d in ship_debris if d.viva]
        else:
            for estrela in estrelas:
                estrela.atualizar(dt, pygame.math.Vector2(0, 0))
            for particula in particulas[:]:
                particula.atualizar(dt)
            particulas = [p for p in particulas if p.viva]
            for debris in ship_debris[:]:
                debris.atualizar(dt)
            ship_debris = [d for d in ship_debris if d.viva]
        
        # Desenhar
        tela.fill(COR_FUNDO)
        
        estrelas_ordenadas = sorted(estrelas, key=lambda s: s.profundidade)
        for estrela in estrelas_ordenadas:
            estrela.desenhar(tela)
        
        if teclas_pressionadas['cima'] and nave.viva:
            nave.desenhar_thrust(tela)
        
        asteroides_ordenados = sorted(asteroides, key=lambda a: a.profundidade)
        for asteroide in asteroides_ordenados:
            asteroide.desenhar(tela)
        
        for particula in particulas:
            particula.desenhar(tela)
        
        for debris in ship_debris:
            debris.desenhar(tela)
        
        nave.desenhar(tela)
        
        for projetil in projeteis:
            projetil.desenhar(tela)
        
        # HUD
        fonte = pygame.font.Font(None, 28)
        fonte_grande = pygame.font.Font(None, 36)
        
        pontos_text = fonte_grande.render(f"PONTOS: {pontos}", True, (255, 255, 255))
        tela.blit(pontos_text, (10, 10))
        
        vidas_text = fonte.render(f"VIDAS: {vidas}", True, (255, 255, 255))
        tela.blit(vidas_text, (10, 50))
        
        nivel_text = fonte.render(f"NÍVEL: {nivel}", True, (255, 200, 100))
        tela.blit(nivel_text, (10, 80))
        
        ast_text = fonte.render(f"Asteroides: {len(asteroides)}", True, (150, 150, 150))
        tela.blit(ast_text, (10, 110))
        
        fps_text = fonte.render(f"FPS: {int(clock.get_fps())}", True, (100, 100, 100))
        tela.blit(fps_text, (LARGURA - 100, 10))
        
        instrucoes = [
            "Setas/WASD: Mover",
            "ESPAÇO: Atirar",
            "ESC: Sair"
        ]
        y_offset = ALTURA - 90
        for instrucao in instrucoes:
            texto = fonte.render(instrucao, True, (150, 150, 150))
            tela.blit(texto, (10, y_offset))
            y_offset += 25
        
        # Tela de Game Over
        if estado_jogo == 'game_over':
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))
            
            fonte_titulo = pygame.font.Font(None, 72)
            fonte_grande = pygame.font.Font(None, 48)
            fonte_media = pygame.font.Font(None, 32)
            fonte_pequena = pygame.font.Font(None, 24)
            
            texto_gameover = fonte_titulo.render("GAME OVER", True, (255, 100, 100))
            rect_gameover = texto_gameover.get_rect(center=(LARGURA // 2, ALTURA // 2 - 100))
            tela.blit(texto_gameover, rect_gameover)
            
            texto_pontos = fonte_grande.render(f"PONTUAÇÃO FINAL: {pontuacao_final}", True, (255, 255, 255))
            rect_pontos = texto_pontos.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20))
            tela.blit(texto_pontos, rect_pontos)
            
            texto_reiniciar = fonte_media.render("Pressione ENTER para reiniciar", True, (200, 200, 200))
            rect_reiniciar = texto_reiniciar.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
            tela.blit(texto_reiniciar, rect_reiniciar)
            
            texto_sair = fonte_pequena.render("ou ESC para sair", True, (150, 150, 150))
            rect_sair = texto_sair.get_rect(center=(LARGURA // 2, ALTURA // 2 + 85))
            tela.blit(texto_sair, rect_sair)
            
            texto_creditos = fonte_pequena.render("por elen-c-sales", True, (100, 150, 200))
            rect_creditos = texto_creditos.get_rect(center=(LARGURA // 2, ALTURA - 40))
            tela.blit(texto_creditos, rect_creditos)
        
        pygame.display.flip()
        
        # CRÍTICO: yield para Pygbag processar eventos do navegador
        await asyncio.sleep(0)
    
    pygame.quit()


# Entry point para Pygbag
asyncio.run(main())
