# Bibliotecas
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import time

# Criando a classe de extrator de features 
class ExtratorFeature: 
    # Construtor
    def __init__(self, tipo_feature: str = 'ORB', qnt_pontos: int = 1000):
        self.tipo_feature = tipo_feature.upper()
        self.qnt_pontos = qnt_pontos
        
        # Criar o detector
        self.detector = self.criar_detector() 


    # Detector 
    def criar_detector(self):
        # ORB
        if self.tipo_feature == 'ORB':
            return cv.ORB_create(nfeatures = self.qnt_pontos)
        
        # SIFT 
        elif self.tipo_feature == 'SIFT': 
            return cv.SIFT_create(nfeatures = self.qnt_pontos)
        
        # # FAST
        # elif self.tipo_feature == 'FAST':
        #     return cv.FastFeatureDetector_create(threshold = 10, 
        #                                          nonmaxSuppression = True, 
        #                                          type = cv.FAST_FEATURE_DETECTOR_TYPE_9_16)
        
        # # SURF
        # elif self.tipo_feature == 'SURF':
        #     return cv.xfeatures2d.SURF_create(400)
    
        # BRISK
        elif self.tipo_feature == "BRISK":
            return cv.BRISK_create()

        # AKAZE
        elif self.tipo_feature == "AKAZE":
            return cv.AKAZE_create()

        else: 
            raise ValueError('Tipo de detector não encontrado')
        
    
    # Extração de keypoints e criação de descritores
    def extrair_features(self, imagem): 
        """
        Detecta os keypoints e calcula os descritores 
        """
        
        kp, des = self.detector.detectAndCompute(imagem, None)

        # Como nem todos os detectores tem o parâmetro de nfeatures:
        kp = kp[: self.qnt_pontos]

        # Se tiver kp válido
        if des is not None:
            des = des[: self.qnt_pontos]

        return (kp, des)
    
    

# Main
if __name__ == '__main__':
    # Leitura da imagem
    imagem = cv.imread('ex01/simple.jpg', cv.IMREAD_GRAYSCALE)

    # Verificando se carregou corretamente
    if imagem is None:
        print('Erro ao carregar a imagem')
        exit()

    # Criando uma lista dos métodos de teste
    lista_metodos = ['ORB', 'SIFT', 'BRISK', 'AKAZE']

    ###### Testando ###### 

    for metodo in lista_metodos:
        print(f'Testando o método: {metodo}')

        # Cria o extrator
        extrator = ExtratorFeature(metodo, 1000)

        # Inicio da contagem de tempo
        ti = time.time()

        # Extraindo os kp
        kp, des = extrator.extrair_features(imagem = imagem)

        # Fim da contagem 
        tf = time.time()

        # Tempo total
        tempo_tot = tf - ti

        # Resultados: 
        print(f'Quantidade de keypoints encontrados: {len(kp)}')
        print(f'Tempo de execução: {tempo_tot}')

        img = cv.drawKeypoints(imagem, kp, None, color = (0, 255, 0), flags = cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        plt.imshow(img)
        plt.show()

