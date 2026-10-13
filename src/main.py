import cv2
from pathlib import Path

from arquivos import ler_anotacoes


RAIZ_PROJETO = Path(__file__).resolve().parent.parent
PASTA_IMAGENS = RAIZ_PROJETO / "imagens"
PASTA_DADOS = RAIZ_PROJETO / "dados"
PASTA_RESULTADOS = RAIZ_PROJETO / "resultados"


def validar_caixas(imagem, nome_arquivo, anotacoes):
    altura, largura = imagem.shape[:2]
    for indice, deteccao in enumerate(anotacoes.deteccoes, start=1):
        if not (
            0 <= deteccao.x_min < deteccao.x_max < largura
            and 0 <= deteccao.y_min < deteccao.y_max < altura
        ):
            raise ValueError(
                f"Caixa {indice} inválida em {nome_arquivo}: "
                f"({deteccao.x_min}, {deteccao.y_min}, "
                f"{deteccao.x_max}, {deteccao.y_max}); "
                f"dimensões da imagem: {largura}x{altura}."
            )


def preparar_visualizacao(imagem_anotada, nome_arquivo):
    visualizacao = imagem_anotada.copy()
    cv2.rectangle(visualizacao, (0, 0), (visualizacao.shape[1], 62), (30, 30, 30), -1)
    cv2.putText(
        visualizacao, nome_arquivo, (12, 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA
    )
    cv2.putText(
        visualizacao, "Classe 0: verde", (12, 49),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA
    )
    cv2.putText(
        visualizacao, "Classe 1: azul", (190, 49),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA
    )
    return visualizacao


def main():
    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    try:
        anotacoes_por_imagem = ler_anotacoes(PASTA_DADOS / "anotacoes.csv")
        nomes_imagens = sorted(
            caminho.name for caminho in PASTA_IMAGENS.glob("*.jpg")
        )

        if len(nomes_imagens) != 10:
            raise ValueError(
                f"Esperadas 10 imagens JPG na pasta '{PASTA_IMAGENS}', "
                f"mas foram encontradas {len(nomes_imagens)}."
            )

        cv2.namedWindow("Visualizador de imagens anotadas", cv2.WINDOW_NORMAL)

        for nome in nomes_imagens:
            caminho_imagem = PASTA_IMAGENS / nome
            imagem_original = cv2.imread(str(caminho_imagem))
            if imagem_original is None:
                raise OSError(f"Não foi possível abrir a imagem: {caminho_imagem}")

            anotacoes = anotacoes_por_imagem.get(nome)
            if anotacoes is None:
                raise ValueError(f"Não há anotações no CSV para {nome}.")

            validar_caixas(imagem_original, nome, anotacoes)
            imagem_anotada = anotacoes.gerar_imagem_anotada(imagem_original)

            caminho_resultado = PASTA_RESULTADOS / nome
            if not cv2.imwrite(str(caminho_resultado), imagem_anotada):
                raise OSError(f"Não foi possível salvar: {caminho_resultado}")

            print(f"Imagem: {nome} | Caixas desenhadas: {len(anotacoes.deteccoes)}")

            # A janela mostra a imagem anotada; reduzir somente a cópia de exibição, se necessário.
            visualizacao = preparar_visualizacao(imagem_anotada, nome)
            limite_largura, limite_altura = 1200, 800
            altura, largura = visualizacao.shape[:2]
            escala = min(limite_largura / largura, limite_altura / altura, 1.0)
            if escala < 1.0:
                visualizacao = cv2.resize(
                    visualizacao, (int(largura * escala), int(altura * escala))
                )

            cv2.imshow("Visualizador de imagens anotadas", visualizacao)
            while True:
                tecla = cv2.waitKey(0) & 0xFF
                if tecla == ord("q"):
                    cv2.destroyAllWindows()
                    return
                if tecla == ord(" "):
                    break
                # Outras teclas mantêm a imagem atual.

        cv2.destroyAllWindows()

    except (OSError, ValueError, KeyError) as erro:
        print(f"Erro: {erro}")
        cv2.destroyAllWindows()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
