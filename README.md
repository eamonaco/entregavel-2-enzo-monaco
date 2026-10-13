# Entregável 2 — Anotações de imagens com OpenCV

**Autor:** Enzo Monaco

## Objetivo
Ler anotações de bounding boxes de um CSV, organizá-las em objetos Python, desenhá-las nas imagens com OpenCV e navegar por um visualizador simples.

## Requisitos
- Python 3
- Dependência: `opencv-python`

## Instalação e execução
Na raiz do projeto, execute:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
```

No Windows, ative o ambiente virtual com `.venv\\Scripts\\activate`.

### Observações sobre a execução no WSL

Durante a execução do projeto no WSL (Ubuntu), ocorreu um erro relacionado ao plugin gráfico `xcb` do Qt, utilizado pelo OpenCV para exibir as janelas das imagens. O erro impedia a inicialização da interface gráfica.

Para investigar o problema, foram instaladas ferramentas de teste do X11 e verificou-se que o ambiente conseguia abrir janelas gráficas. Após executar novamente o programa com a variável `QT_DEBUG_PLUGINS=1`, o projeto passou a funcionar corretamente.

Esse problema estava relacionado ao ambiente gráfico e à inicialização do Qt, não à lógica de anotação das imagens.

## Controles
- **Espaço:** avança para a próxima imagem.
- **q:** encerra o programa.
- **Qualquer outra tecla:** mantém a imagem atual.

## Organização
- `src/modelos.py`: define `Deteccao`, que desenha uma caixa, e `ImagemAnotada`, que reúne as detecções de uma imagem.
- `src/arquivos.py`: lê `dados/anotacoes.csv` usando `csv` e agrupa as caixas por nome de imagem.
- `src/main.py`: valida coordenadas, percorre as imagens em ordem alfabética, exibe as anotações e salva os resultados.
- `imagens/`: imagens originais, preservadas.
- `dados/anotacoes.csv`: anotações fornecidas.
- `resultados/`: imagens anotadas produzidas pelo programa.

A classe 0 é desenhada em verde e a classe 1 em azul.