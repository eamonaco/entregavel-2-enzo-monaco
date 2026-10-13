import csv
from pathlib import Path

from modelos import Deteccao, ImagemAnotada


def ler_anotacoes(caminho_csv):
    
    imagens = {}

    try:
        with Path(caminho_csv).open("r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            colunas_obrigatorias = {
                "imagem", "classe_id", "x_min", "y_min", "x_max", "y_max"
            }
            if leitor.fieldnames is None or not colunas_obrigatorias.issubset(leitor.fieldnames):
                raise ValueError("O CSV não contém todas as colunas obrigatórias.")

            for numero_linha, linha in enumerate(leitor, start=2):
                try:
                    nome = linha["imagem"].strip()
                    if not nome:
                        raise ValueError("nome da imagem vazio")
                    deteccao = Deteccao(
                        int(linha["classe_id"]),
                        int(linha["x_min"]),
                        int(linha["y_min"]),
                        int(linha["x_max"]),
                        int(linha["y_max"]),
                    )
                except (ValueError, TypeError) as erro:
                    raise ValueError(
                        f"Dados inválidos na linha {numero_linha} do CSV: {erro}"
                    ) from erro

                if nome not in imagens:
                    imagens[nome] = ImagemAnotada(nome)
                imagens[nome].adicionar_deteccao(deteccao)

    except OSError as erro:
        raise OSError(f"Não foi possível ler o CSV '{caminho_csv}': {erro}") from erro

    return imagens
