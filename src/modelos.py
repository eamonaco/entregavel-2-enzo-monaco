import cv2


CORES_POR_CLASSE = {
    0: (0, 255, 0),    # Verde em BGR
    1: (255, 0, 0),    # Azul em BGR
}


class Deteccao:

    def __init__(self, classe_id, x_min, y_min, x_max, y_max):
        self.classe_id = int(classe_id)
        self.x_min = int(x_min)
        self.y_min = int(y_min)
        self.x_max = int(x_max)
        self.y_max = int(y_max)

    def desenhar(self, imagem):
        cor = CORES_POR_CLASSE.get(self.classe_id, (0, 255, 255))
        cv2.rectangle(
            imagem,
            (self.x_min, self.y_min),
            (self.x_max, self.y_max),
            cor,
            2,
        )


class ImagemAnotada:

    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.deteccoes = []

    def adicionar_deteccao(self, deteccao):
        self.deteccoes.append(deteccao)

    def gerar_imagem_anotada(self, imagem_original):
        imagem_anotada = imagem_original.copy()
        for deteccao in self.deteccoes:
            deteccao.desenhar(imagem_anotada)
        return imagem_anotada
