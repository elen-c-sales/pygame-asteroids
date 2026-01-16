# Documentação Técnica

## Visão Geral da Arquitetura

Esta implementação do Asteroids usa uma arquitetura orientada a objetos com uma clara separação entre entidades do jogo, utilitários e o loop principal. A inovação central é o sistema de renderização baseado em profundidade que cria um efeito visual pseudo-3D em um jogo 2D.

## Sistema de Renderização de Profundidade

### Interpolação de Cor

O efeito de profundidade é alcançado através de interpolação linear de cor entre dois pontos extremos:

```python
COR_DISTANTE = (74, 95, 156)    # Azul (longe)
COR_PROXIMA = (255, 255, 255)   # Branco (perto)

def interpolar_cor(profundidade):
    """
    profundidade: 0.0 (distante) a 1.0 (próximo)
    retorna: (R, G, B)
    """
    r = int(COR_DISTANTE[0] + (COR_PROXIMA[0] - COR_DISTANTE[0]) * profundidade)
    g = int(COR_DISTANTE[1] + (COR_PROXIMA[1] - COR_DISTANTE[1]) * profundidade)
    b = int(COR_DISTANTE[2] + (COR_PROXIMA[2] - COR_DISTANTE[2]) * profundidade)
    return (r, g, b)
```

### Camadas de Profundidade

O jogo usa faixas de profundidade distintas para diferentes tipos de objetos:

| Camada | Faixa de Profundidade | Objetos | Propósito |
|--------|----------------------|---------|-----------|
| Fundo | 0.15 - 0.75 | Estrelas | Ambiente espacial |
| Primeiro plano | 0.8 - 1.0 | Asteroides | Objetos de jogabilidade |
| Ativo | 1.0 | Nave, Projéteis | Elementos controlados pelo jogador |

### Rolagem Paralaxe

Estrelas se movem em resposta à velocidade da nave, criando um efeito de paralaxe:

```python
fator_paralaxe = estrela.profundidade * 0.3
estrela.x -= nave.vel.x * fator_paralaxe * dt
estrela.y -= nave.vel.y * fator_paralaxe * dt
```

Estrelas mais próximas (valor de profundidade maior) se movem mais rápido, criando a ilusão de espaço 3D.

## Sistema de Física

### Movimento Baseado em Vetores

Todas as entidades usam `pygame.math.Vector2` para posição e velocidade:

```python
self.pos = pygame.math.Vector2(x, y)
self.vel = pygame.math.Vector2(0, 0)
```

### Física da Nave

A nave implementa física espacial realista:

1. **Propulsão**: Aceleração na direção que a nave está apontando
2. **Inércia**: Velocidade persiste quando a propulsão é liberada
3. **Fricção**: Desaceleração gradual (vel *= 0.98)
4. **Rotação**: Independente da direção de movimento

```python
def acelerar(self, dt):
    angulo_rad = math.radians(self.angulo - 90)
    aceleracao = pygame.math.Vector2(
        math.cos(angulo_rad) * self.aceleracao_thrust * dt,
        math.sin(angulo_rad) * self.aceleracao_thrust * dt
    )
    self.vel += aceleracao
    
    if self.vel.length() > self.vel_maxima:
        self.vel.scale_to_length(self.vel_maxima)
```

### Herança de Velocidade do Projétil

Projéteis herdam a velocidade da nave, mantendo o momentum:

```python
vel_tiro = vetor_direcao * 400  # Velocidade base
vel_tiro += self.vel  # Adiciona velocidade da nave
```

## Detecção de Colisão

Usa colisão circular com hitbox para eficiência:

```python
def checar_colisao_circular(obj1_pos, obj1_raio, obj2_pos, obj2_raio):
    distancia = obj1_pos.distance_to(obj2_pos)
    return distancia < (obj1_raio + obj2_raio)
```

Cada objeto mantém um raio de colisão ligeiramente menor que sua representação visual para melhor sensação de jogabilidade.

## Geração de Asteroides

### Formas Procedurais

Asteroides são gerados como polígonos irregulares:

```python
def gerar_forma_irregular(self):
    num_pontos = random.randint(8, 12)
    pontos = []
    
    for i in range(num_pontos):
        angulo = (2 * math.pi / num_pontos) * i
        variacao = random.uniform(0.7, 1.3)
        raio = self.tamanho * variacao
        
        x = raio * math.cos(angulo)
        y = raio * math.sin(angulo)
        pontos.append(pygame.math.Vector2(x, y))
    
    return pontos
```

Isso cria formas únicas e poligonais para cada asteroide.

### Sistema de Fragmentação

Quando destruídos, asteroides se fragmentam em pedaços menores:

- **Grande** → 2 asteroides Médios
- **Médio** → 2 asteroides Pequenos
- **Pequeno** → Destruído (sem fragmentos)

Fragmentos herdam o valor de profundidade do pai e recebem velocidades aleatórias.

## Pipeline de Renderização

Objetos são renderizados em ordem de profundidade para criar oclusão apropriada:

```python
# 1. Estrelas de fundo (ordenadas por profundidade)
estrelas_ordenadas = sorted(estrelas, key=lambda s: s.profundidade)
for estrela in estrelas_ordenadas:
    estrela.desenhar(tela)

# 2. Asteroides (ordenados por profundidade)
asteroides_ordenados = sorted(asteroides, key=lambda a: a.profundidade)
for asteroide in asteroides_ordenados:
    asteroide.desenhar(tela)

# 3. Efeitos (partículas, destroços)
for particula in particulas:
    particula.desenhar(tela)

# 4. Nave e projéteis (sempre no topo)
nave.desenhar(tela)
for projetil in projeteis:
    projetil.desenhar(tela)
```

## Sistemas de Partículas

### Explosões de Asteroides

A cor da partícula corresponde à cor baseada em profundidade do asteroide:

```python
particulas.extend(criar_explosao(
    asteroide.pos.x, 
    asteroide.pos.y, 
    asteroide.cor,  # Cor baseada em profundidade
    num_particulas=15,
    velocidade=100
))
```

### Destroços da Nave

Explosão autêntica estilo Atari onde o triângulo da nave se quebra em três segmentos de linha:

```python
def criar_explosao_nave(nave):
    debris_list = []
    pontos = nave.forma_base  # Vértices do triângulo
    
    # Criar destroço para cada borda
    linhas = [
        (pontos[0], pontos[1]),  # Frente para esquerda
        (pontos[1], pontos[2]),  # Esquerda para direita
        (pontos[2], pontos[0])   # Direita para frente
    ]
    
    for linha in linhas:
        debris = ShipDebris(nave.pos.x, nave.pos.y, linha, nave.angulo)
        debris_list.append(debris)
    
    return debris_list
```

Cada pedaço de destroço:
- Retém informações de rotação e posição
- Voa em uma direção aleatória
- Gira independentemente
- Desaparece gradualmente ao longo do tempo

## Gerenciamento de Estado do Jogo

O jogo opera em dois estados:

1. **Jogando**: Gameplay ativo com física completa
2. **Game Over**: Estado pausado com overlay, continuando efeitos visuais

Transições de estado ocorrem baseadas nas vidas do jogador:

```python
if vidas <= 0:
    estado_jogo = 'game_over'
    pontuacao_final = pontos
```

## Considerações de Performance

### Pooling de Objetos

Objetos mortos são removidos das listas imediatamente:

```python
asteroides = [a for a in asteroides if a.vivo]
projeteis = [p for p in projeteis if p.vivo]
particulas = [p for p in particulas if p.viva]
```

### Gerenciamento de Taxa de Quadros

Timestep fixo com delta time para física consistente:

```python
dt = clock.tick(60) / 1000.0  # 60 FPS, dt em segundos
```

### Limitação de Spawn

Máximo de asteroides simultâneos para prevenir degradação de performance:

```python
if tempo_spawn >= intervalo_spawn and len(asteroides) < 8:
    asteroides.append(spawn_asteroide('grande'))
```

## Sistema de Áudio

Efeitos sonoros são carregados uma vez e tocados através do mixer do Pygame:

```python
pygame.mixer.init()
som_tiro = pygame.mixer.Sound("assets/tiro2.wav")
som_tiro.set_volume(0.3)  # Controle de volume
```

Volumes são balanceados para prevenir fadiga auditiva:
- Disparo: 30%
- Explosão de asteroide: 50%
- Explosão da nave: 70%

## Constantes de Configuração

Parâmetros chave de jogabilidade definidos em nível de módulo:

```python
LARGURA = 800
ALTURA = 600
FPS = 60
NUM_ESTRELAS = 300
```

Isso permite ajuste fácil de balanceamento sem modificar a lógica central.

## Oportunidades de Melhorias Futuras

1. **Power-ups**: Escudo, tiro rápido, tiro múltiplo
2. **Sistema de ondas**: Dificuldade crescente ao longo do tempo
3. **Persistência de high score**: Sistema de salvamento baseado em JSON
4. **Multiplayer**: Modo cooperativo baseado em rede
5. **Efeitos de profundidade avançados**: Névoa, escalonamento de sprites baseado em distância
6. **Controles móveis**: Manipulação de entrada baseada em toque

## Dependências

- **Python**: 3.7+
- **Pygame**: 2.0+ (usa `pygame.math.Vector2`, `pygame.mixer`)

Nenhuma dependência adicional necessária.
