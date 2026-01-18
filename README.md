# Asteroids 3D - Edição Efeito de Profundidade

Uma interpretação moderna do clássico jogo Asteroids da Atari, apresentando um sistema visual único de profundidade 3D através de interpolação de cores e rolagem paralaxe.

## 🎮 Jogar Agora

**[▶️ JOGAR NO NAVEGADOR](https://elen-c-sales.github.io/pygame-asteroids/)**

Ou baixe para jogar na versão desktop com melhor performance.

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

### Dificuldade Progressiva
O jogo apresenta um sistema de dificuldade adaptativo que aumenta o desafio conforme você progride:

- **Sistema de Níveis**: Avance um nível a cada 500 pontos conquistados
- **Escalonamento de Velocidade**: Velocidade dos asteroides aumenta 15% por nível
- **Taxa de Spawn**: Tempo entre aparições de asteroides diminui (mínimo 1.5 segundos)
- **Quantidade**: Máximo de asteroides simultâneos aumenta de 8 para 15

Isso cria uma curva envolvente onde os níveis iniciais são acessíveis enquanto os níveis avançados proporcionam desafio intenso para jogadores experientes.

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

Este jogo está disponível em duas versões:

### Versão Web (Recomendada para teste rápido)

Jogue diretamente no navegador sem instalação:
**[elen-c-sales.github.io/pygame-asteroids](https://elen-c-sales.github.io/pygame-asteroids/)**

### 💻 Versão Desktop (Melhor performance)

**Requisitos:**
- Python 3.7+
- Pygame 2.0+

**Instalação:**

```bash
# Clone o repositório
git clone https://github.com/elen-c-sales/pygame-asteroids.git
cd pygame-asteroids

# Instale as dependências
pip install pygame

# Execute o jogo
python main.py
```

## Deploy Web (Para Desenvolvedores)

Se você quer rodar sua própria versão web:

```bash
# Instalar Pygbag
pip install pygbag

# Copiar versão web como main.py (Pygbag exige esse nome)
copy main_web.py main.py

# Compilar para web
pygbag . --build --output docs

# Testar localmente
python -m http.server 8000 --directory docs

# Limpar main.py copiado (opcional)
del main.py
```

Para instruções completas de deployment no GitHub Pages, consulte [DEPLOY.md](DEPLOY.md).

## Estrutura do Projeto

```
pygame-asteroids/
├── main.py                 # 💻 Versão Desktop - Loop principal
├── main_web.py             # 🌐 Versão Web - Com async/await para Pygbag
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
├── assets/
│   └── sounds/            # Arquivos de áudio
├── docs/                  # 📦 Build da versão web (gerado por Pygbag)
├── README.md
├── TECHNICAL.md           # Documentação técnica detalhada
├── DEPLOY.md              # Guia de deployment web
└── LICENSE
```

## Diferenças: Desktop vs Web

| Aspecto | Desktop (main.py) | Web (main_web.py) |
|---------|-------------------|-------------------|
| **Execução** | Python nativo | WebAssembly via Pygbag |
| **Performance** | 100% | ~70% (limitação do navegador) |
| **Instalação** | Requer Python + Pygame | Zero instalação |
| **Áudio** | Sem restrições | Pode ter latência inicial |
| **Código** | Loop síncrono | Loop assíncrono (`async/await`) |
| **Distribuição** | Download necessário | Link direto |

Ambas as versões compartilham 95% do código. A versão web apenas adiciona `async/await` para compatibilidade com navegadores.

## Documentação Técnica

Para informações técnicas detalhadas sobre a implementação, incluindo o sistema de renderização de profundidade, cálculos de física e decisões de arquitetura, consulte [TECHNICAL.md](TECHNICAL.md).

## Créditos

**Desenvolvedora**: Elen Camila Sales  
**GitHub**: [@elen-c-sales](https://github.com/elen-c-sales/)

**Inspiração**: Visualização de campo estelar de Rafaela Catharina Pechtoll Pereira  
**Jogo Original**: Asteroids da Atari (1979)  
**Efeitos Sonoros**: Gerados com [Bfxr](https://www.bfxr.net/)

## Licença

Este projeto é de código aberto e está disponível sob a [Licença MIT](LICENSE).

## Agradecimentos

Agradecimentos especiais à comunidade Pygame pela excelente documentação e exemplos que tornaram o desenvolvimento de jogos baseados em vetores acessível e prazeroso.
