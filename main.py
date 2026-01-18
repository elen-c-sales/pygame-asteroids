"""
Asteroids 3D - Jogo com efeito de profundidade usando Pygame
Inspirado no clássico Atari com visual moderno de paralaxe
"""
import pygame
import random
from classes.star import Star
from utils.cores import COR_FUNDO


# Configurações da tela
LARGURA = 800
ALTURA = 600
FPS = 60

# Configurações do starfield
NUM_ESTRELAS = 300  # Mais estrelas para céu realista
PROF_MIN = 0.15  # Profundidade mínima (estrelas muito distantes)
PROF_MAX = 0.75  # Profundidade máxima (estrelas próximas, mas não muito para não confundir com asteroides)


def criar_estrelas():
    """Cria campo de estrelas com diferentes profundidades"""
    estrelas = []
    for _ in range(NUM_ESTRELAS):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        profundidade = random.uniform(PROF_MIN, PROF_MAX)
        estrelas.append(Star(x, y, profundidade, LARGURA, ALTURA))
    return estrelas


def main():
    """Loop principal do jogo"""
    # Inicialização
    pygame.init()
    pygame.mixer.init()  # Inicializar sistema de som
    
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Asteroids 3D - Efeito de Profundidade")
    clock = pygame.time.Clock()
    
    # Carregar sons
    try:
        som_tiro = pygame.mixer.Sound("assets/tiro2.wav")
        som_explosao_asteroide = pygame.mixer.Sound("assets/explode4.wav")
        som_explosao_nave = pygame.mixer.Sound("assets/explode1.wav")
        
        # Ajustar volumes
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
    particulas = []  # Lista de partículas de explosão
    ship_debris = []  # Lista de pedaços da nave
    
    # Criar asteroides iniciais
    def spawn_asteroide(tamanho='grande'):
        """Spawna um asteroide na borda da tela"""
        # Escolher borda aleatória
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
    intervalo_spawn = 4.0  # segundos entre spawns
    estado_jogo = 'jogando'  # 'jogando' ou 'game_over'
    pontuacao_final = 0
    
    # Sistema de dificuldade progressiva
    nivel = 1
    pontos_por_nivel = 500  # Pontos necessários para subir de nível
    
    def calcular_dificuldade():
        """Calcula o nível atual baseado na pontuação"""
        return (pontos // pontos_por_nivel) + 1
    
    def get_multiplicador_velocidade():
        """Retorna multiplicador de velocidade baseado no nível"""
        return 1.0 + (nivel - 1) * 0.15  # +15% por nível
    
    def get_intervalo_spawn():
        """Retorna intervalo de spawn baseado no nível"""
        # Diminui o intervalo, mas nunca menos que 1.5 segundos
        return max(1.5, 4.0 - (nivel - 1) * 0.3)
    
    def get_max_asteroides():
        """Retorna número máximo de asteroides baseado no nível"""
        return min(15, 8 + (nivel - 1) * 1)  # Máximo de 15 asteroides
    
    def resetar_jogo():
        """Reseta o jogo para um novo round"""
        nonlocal pontos, vidas, asteroides, projeteis, nave, tempo_spawn, estado_jogo, particulas, ship_debris, nivel
        
        pontos = 0
        vidas = 3
        tempo_spawn = 0
        estado_jogo = 'jogando'
        nivel = 1  # Resetar nível
        
        # Resetar nave
        nave.pos = pygame.math.Vector2(LARGURA // 2, ALTURA // 2)
        nave.vel = pygame.math.Vector2(0, 0)
        nave.angulo = 0
        nave.viva = True
        
        # Limpar e recriar asteroides
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
        dt = clock.tick(FPS) / 1000.0  # Delta time em segundos
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                    
                # Reiniciar jogo na tela de game over
                elif evento.key == pygame.K_RETURN and estado_jogo == 'game_over':
                    resetar_jogo()
                
                # Controles durante o jogo
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
            # Processar controles da nave
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
                    # Som de tiro
                    if sons_carregados:
                        som_tiro.play()
        
            # Atualizar
            # Atualizar estrelas com efeito paralaxe baseado na velocidade da nave
            for estrela in estrelas:
                estrela.atualizar(dt, nave.vel)
            
            nave.atualizar(dt)
            
            # Atualizar projéteis e remover mortos
            for projetil in projeteis[:]:
                projetil.atualizar(dt, LARGURA, ALTURA)
                if not projetil.vivo:
                    projeteis.remove(projetil)
            
            # Atualizar asteroides
            for asteroide in asteroides[:]:
                asteroide.atualizar(dt, LARGURA, ALTURA)
            
            # Atualizar nível baseado na pontuação
            nivel_anterior = nivel
            nivel = calcular_dificuldade()
            
            # Notificar subida de nível
            if nivel > nivel_anterior and nivel > 1:
                # Aqui poderia adicionar som ou efeito visual de level up
                pass
            
            # Spawnar novos asteroides periodicamente (com dificuldade progressiva)
            intervalo_atual = get_intervalo_spawn()
            max_asteroides_atual = get_max_asteroides()
            multiplicador_vel = get_multiplicador_velocidade()
            
            tempo_spawn += dt
            if tempo_spawn >= intervalo_atual and len(asteroides) < max_asteroides_atual:
                novo_asteroide = spawn_asteroide('grande')
                # Aplicar multiplicador de velocidade baseado no nível
                novo_asteroide.vel *= multiplicador_vel
                asteroides.append(novo_asteroide)
                tempo_spawn = 0
            
            # Colisão: Projéteis vs Asteroides
            for projetil in projeteis[:]:
                if not projetil.vivo:
                    continue
                    
                for asteroide in asteroides[:]:
                    if not asteroide.vivo:
                        continue
                    
                    if checar_colisao_circular(projetil.pos, projetil.raio, asteroide.pos, asteroide.raio_colisao):
                        # Destruir projétil e asteroide
                        projetil.vivo = False
                        asteroide.vivo = False
                        
                        # Criar explosão de partículas
                        particulas.extend(criar_explosao(
                            asteroide.pos.x, 
                            asteroide.pos.y, 
                            asteroide.cor, 
                            num_particulas=15,
                            velocidade=100
                        ))
                        
                        # Som de explosão
                        if sons_carregados:
                            som_explosao_asteroide.play()
                        
                        # Adicionar pontos baseado no tamanho e profundidade
                        if asteroide.tamanho_tipo == 'grande':
                            pontos += int(20 * asteroide.profundidade)
                        elif asteroide.tamanho_tipo == 'medio':
                            pontos += int(50 * asteroide.profundidade)
                        else:  # pequeno
                            pontos += int(100 * asteroide.profundidade)
                        
                        # Fragmentar asteroide
                        fragmentos = asteroide.fragmentar()
                        asteroides.extend(fragmentos)
                        
                        break
            
            # Colisão: Nave vs Asteroides
            if nave.viva:
                for asteroide in asteroides[:]:
                    if not asteroide.vivo:
                        continue
                    
                    if checar_colisao_circular(nave.pos, nave.raio_colisao, asteroide.pos, asteroide.raio_colisao):
                        # Nave morreu
                        nave.viva = False
                        vidas -= 1
                        
                        # Criar explosão da nave (pedaços do triângulo voando)
                        ship_debris.extend(criar_explosao_nave(nave))
                        
                        # Som de explosão da nave
                        if sons_carregados:
                            som_explosao_nave.play()
                        
                        # Verificar game over
                        if vidas <= 0:
                            estado_jogo = 'game_over'
                            pontuacao_final = pontos
                        else:
                            # Respawn
                            nave.pos = pygame.math.Vector2(LARGURA // 2, ALTURA // 2)
                            nave.vel = pygame.math.Vector2(0, 0)
                            nave.viva = True
            
            # Remover asteroides mortos
            asteroides = [a for a in asteroides if a.vivo]
            projeteis = [p for p in projeteis if p.vivo]
            
            # Atualizar partículas
            for particula in particulas[:]:
                particula.atualizar(dt)
            particulas = [p for p in particulas if p.viva]
            
            # Atualizar pedaços da nave
            for debris in ship_debris[:]:
                debris.atualizar(dt)
            ship_debris = [d for d in ship_debris if d.viva]
        else:
            # Ainda atualizar estrelas, partículas e debris no game over (efeito visual)
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
        
        # Desenhar estrelas (ordenadas por profundidade - distantes primeiro)
        estrelas_ordenadas = sorted(estrelas, key=lambda s: s.profundidade)
        for estrela in estrelas_ordenadas:
            estrela.desenhar(tela)
        
        # Desenhar thrust se estiver acelerando
        if teclas_pressionadas['cima'] and nave.viva:
            nave.desenhar_thrust(tela)
        
        # Desenhar asteroides (ordenados por profundidade - distantes primeiro)
        asteroides_ordenados = sorted(asteroides, key=lambda a: a.profundidade)
        for asteroide in asteroides_ordenados:
            asteroide.desenhar(tela)
        
        # Desenhar partículas de explosão
        for particula in particulas:
            particula.desenhar(tela)
        
        # Desenhar pedaços da nave (debris)
        for debris in ship_debris:
            debris.desenhar(tela)
        
        # Desenhar nave (só se estiver viva)
        nave.desenhar(tela)
        
        # Desenhar projéteis
        for projetil in projeteis:
            projetil.desenhar(tela)
        
        # Desenhar HUD
        fonte = pygame.font.Font(None, 28)
        fonte_grande = pygame.font.Font(None, 36)
        
        # Pontos
        pontos_text = fonte_grande.render(f"PONTOS: {pontos}", True, (255, 255, 255))
        tela.blit(pontos_text, (10, 10))
        
        # Vidas
        vidas_text = fonte.render(f"VIDAS: {vidas}", True, (255, 255, 255))
        tela.blit(vidas_text, (10, 50))
        
        # Nível
        nivel_text = fonte.render(f"NÍVEL: {nivel}", True, (255, 200, 100))
        tela.blit(nivel_text, (10, 80))
        
        # Asteroides na tela
        ast_text = fonte.render(f"Asteroides: {len(asteroides)}", True, (150, 150, 150))
        tela.blit(ast_text, (10, 110))
        
        # FPS
        fps_text = fonte.render(f"FPS: {int(clock.get_fps())}", True, (100, 100, 100))
        tela.blit(fps_text, (LARGURA - 100, 10))
        
        # Instruções
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
            # Overlay semi-transparente
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))
            
            # Fontes
            fonte_titulo = pygame.font.Font(None, 72)
            fonte_grande = pygame.font.Font(None, 48)
            fonte_media = pygame.font.Font(None, 32)
            fonte_pequena = pygame.font.Font(None, 24)
            
            # GAME OVER
            texto_gameover = fonte_titulo.render("GAME OVER", True, (255, 100, 100))
            rect_gameover = texto_gameover.get_rect(center=(LARGURA // 2, ALTURA // 2 - 100))
            tela.blit(texto_gameover, rect_gameover)
            
            # Pontuação Final
            texto_pontos = fonte_grande.render(f"PONTUAÇÃO FINAL: {pontuacao_final}", True, (255, 255, 255))
            rect_pontos = texto_pontos.get_rect(center=(LARGURA // 2, ALTURA // 2 - 20))
            tela.blit(texto_pontos, rect_pontos)
            
            # Instruções
            texto_reiniciar = fonte_media.render("Pressione ENTER para reiniciar", True, (200, 200, 200))
            rect_reiniciar = texto_reiniciar.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
            tela.blit(texto_reiniciar, rect_reiniciar)
            
            texto_sair = fonte_pequena.render("ou ESC para sair", True, (150, 150, 150))
            rect_sair = texto_sair.get_rect(center=(LARGURA // 2, ALTURA // 2 + 85))
            tela.blit(texto_sair, rect_sair)
            
            # Créditos
            texto_creditos = fonte_pequena.render("por elen-c-sales", True, (100, 150, 200))
            rect_creditos = texto_creditos.get_rect(center=(LARGURA // 2, ALTURA - 40))
            tela.blit(texto_creditos, rect_creditos)
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()
