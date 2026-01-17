# Asteroids 3D - Edição Efeito de Profundidade

Uma interpretação moderna do clássico jogo Asteroids da Atari, apresentando um sistema visual único de profundidade 3D através de interpolação de cores e rolagem paralaxe.

https://github.com/user-attachments/assets/177578a6-48f4-482b-a9ea-5046822ac80f


## História de Origem

Este projeto nasceu de uma troca criativa no LinkedIn. Após ver meu jogo [Dino Run - Vecna Edition](https://github.com/elen-c-sales/dino-run-vecna-edition), Rafaela Catharina Pechtoll Pereira se inspirou e criou uma visualização de campo estelar usando Pygame - uma exibição hipnotizante de estrelas em três cores, controladas pelo movimento do mouse.

Seu trabalho me lembrou do icônico [jogo de arcade Asteroids da Atari](https://youtube.com/shorts/aSPW2Ri_cts?si=zTWiRLaXZfYhm-FH), e eu decidi desenvolver minha própria versão, incorporando efeitos visuais modernos enquanto preservava a estética wireframe clássica e a física baseada em vetores.

## Funcionalidades

### Sistema de Profundidade Visual
- Percepção de profundidade baseada em cor: objetos distantes aparecem azuis, objetos próximos aparecem brancos
- Profundidade baseada em tamanho: objetos escalam proporcionalmente à sua distância
- Rolagem paralaxe: estrelas de fundo se movem em velocidades diferentes baseadas na profundidade
- Campo estelar dinâmico respondendo ao movimento da nave

### Gameplay Clássico do Asteroids
- Física baseada em vetores com inércia
- Tela infinita (espaço infinito)
- Sistema de fragmentação de asteroides (Grande → 2 Médios → 2 Pequenos)
- Explosão autêntica da nave com destroços triangulares
- Detecção de colisão consciente da profundidade

### Sistema de Pontuação
Pontos são calculados baseados tanto no tamanho quanto na profundidade do asteroide:
- Asteroides grandes: 20 × multiplicador de profundidade
- Asteroides médios: 50 × multiplicador de profundidade
- Asteroides pequenos: 100 × multiplicador de profundidade

Asteroides mais próximos (mais brancos) valem mais pontos, incentivando jogabilidade estratégica.

### Áudio
- Efeitos sonoros de disparo de arma
- Áudio de destruição de asteroides
- Som de explosão da nave
- Mixagem de áudio com volume balanceado

## Controles

- **Setas** ou **WASD**: Rotacionar e acelerar
- **Barra de Espaço**: Atirar
- **Enter**: Reiniciar jogo (ao perder)
- **Escape**: Sair do jogo

## Instalação

### Requisitos
- Python 3.7+
- Pygame 2.0+

### Configuração

```bash
# Clone o repositório
git clone https://github.com/elen-c-sales/pygame-asteroids.git
cd pygame-asteroids

# Instale as dependências
pip install pygame

# Execute o jogo
python main.py
```

## Estrutura do Projeto

```
asteroids_3d/
├── main.py                 # Loop principal do jogo
├── classes/
│   ├── star.py            # Campo estelar com paralaxe
│   ├── asteroid.py        # Asteroides gerados proceduralmente
│   ├── ship.py            # Nave do jogador com física vetorial
│   ├── bullet.py          # Sistema de projéteis
│   ├── particula.py       # Efeitos de partículas de explosão
│   └── ship_debris.py     # Destroços da nave na destruição
├── utils/
│   ├── cores.py           # Utilitários de interpolação de cor
│   └── fisica.py          # Detecção de colisão
└── assets/
    └── sounds/            # Arquivos de áudio
```

## Documentação Técnica

Para informações técnicas detalhadas sobre a implementação, incluindo o sistema de renderização de profundidade, cálculos de física e decisões de arquitetura, consulte [TECHNICAL.md](TECHNICAL.md).

## Créditos

**Desenvolvedora**: Elen Camila Sales  
**GitHub**: [@elen-c-sales](https://github.com/elen-c-sales/)

**Inspiração**: Visualização de campo estelar de Rafaela Catharina Pechtoll Pereira  
**Jogo Original**: Asteroids da Atari (1979)

## Licença

Este projeto é de código aberto e está disponível sob a [Licença MIT](LICENSE).

## Agradecimentos

Agradecimentos especiais à comunidade Pygame pela excelente documentação e exemplos que tornaram o desenvolvimento de jogos baseados em vetores acessível e prazeroso.
