# Guia de Deployment Web - Pygbag + GitHub Pages

Este guia explica como compilar e fazer deploy da versão web do Asteroids 3D usando Pygbag e GitHub Pages.

## Pré-requisitos

```bash
pip install pygbag
```

## Importante: main.py vs main_web.py

O Pygbag **exige** que o arquivo principal se chame `main.py`. Temos duas opções:

### Opção 1: Renomear Temporariamente (Recomendado)

```bash
# Fazer backup da versão desktop
move main.py main_desktop.py

# Renomear versão web para main.py
move main_web.py main.py

# Compilar
pygbag . --build --output docs

# Restaurar nomes originais
move main.py main_web.py
move main_desktop.py main.py
```

### Opção 2: Build Permanente (Mais Simples)

Use o diretório atual diretamente:

```bash
# Copiar main_web.py como main.py
copy main_web.py main.py

# Compilar (Pygbag vai usar o main.py do diretório)
pygbag . --build --output docs

# Opcional: Deletar o main.py copiado se já tiver commitado main_web.py
del main.py
```

## Passos para Deploy

### 1. Compilar com Pygbag

Escolha uma das opções acima. O comando base é:

```bash
pygbag . --build --output docs
```

Este comando irá:
- Compilar o código Python para WebAssembly
- Copiar todos os assets necessários
- Gerar `index.html` e arquivos JS/WASM
- Salvar tudo no diretório `docs/`

### 2. Testar Localmente

Antes de fazer deploy, teste localmente:

```bash
python -m http.server 8000 --directory docs
```

Acesse `http://localhost:8000` no navegador para testar o jogo.

### 3. Commit e Push

```bash
git add docs/
git commit -m "Build: Versão web compilada com Pygbag"
git push origin main
```

### 4. Configurar GitHub Pages

1. Vá para **Settings** do repositório no GitHub
2. Navegue até **Pages** (menu lateral)
3. Em **Source**, selecione:
   - Branch: `main`
   - Folder: `/docs`
4. Clique em **Save**

### 5. Aguardar Deploy

GitHub Pages pode levar 2-5 minutos para fazer o primeiro deploy.

Seu jogo estará disponível em:
```
https://<seu-usuario>.github.io/pygame-asteroids/
```

Substitua `<seu-usuario>` pelo seu username do GitHub.

## Atualizações Futuras

Sempre que modificar o código:

1. Recompilar:
   ```bash
   pygbag main_web.py --build --output docs
   ```

2. Commit e Push:
   ```bash
   git add docs/
   git commit -m "Update: [descrição da mudança]"
   git push
   ```

3. GitHub Pages atualizará automaticamente em ~2 minutos

## Solução de Problemas

### Erro: "Module not found"

Certifique-se de que todos os arquivos `.py` estão no caminho correto:
```
/classes/
/utils/
/assets/
```

### Sons não funcionam

Navegadores têm restrições de audio autoplay. O usuário pode precisar clicar na tela primeiro.

### Performance baixa

- Reduza `NUM_ESTRELAS` em `main_web.py`
- Diminua número máximo de asteroides
- WebAssembly é ~50-70% da performance nativa

### Página em branco

Verifique o console do navegador (F12) para erros. Geralmente é problema de path nos assets.

## Diferenças: Desktop vs Web

### Desktop (main.py)
- Performance total
- Sem limitações de audio
- Instalação de dependências necessária

### Web (main_web.py)
- Roda no navegador (sem instalação)
- Performance ligeiramente inferior
- Possíveis limitações de audio
- Requer `await asyncio.sleep(0)` no loop

## Estrutura de Arquivos após Build

```
docs/
├── index.html          # Página principal
├── main.js             # JavaScript gerado
├── pygame.wasm         # Python compilado
├── python.wasm         # Runtime Python
├── assets/             # Recursos copiados
│   ├── tiro2.wav
│   ├── explode4.wav
│   └── explode1.wav
└── [outros arquivos do Pygbag]
```

## Badge do GitHub Pages (Opcional)

Adicione ao README para mostrar o status do deployment:

```markdown
[![GitHub Pages](https://img.shields.io/badge/demo-online-green.svg)](https://<seu-usuario>.github.io/pygame-asteroids/)
```

Substitua `<seu-usuario>` pelo seu username do GitHub.

## Recursos Adicionais

- [Documentação Pygbag](https://pygame-web.github.io/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)
- [Pygame na Web](https://pygame-web.github.io/showroom/)
