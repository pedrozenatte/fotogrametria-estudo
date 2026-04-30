# Bibliotecas
import numpy as np
import cv2 as cv

# Importando as classes
from ex07.ex07 import PinholeCamera

class Triangulacao: 
    # Construtor 
    def __init__(self, cam1: PinholeCamera, cam2: PinholeCamera):
        self.cam1 = cam1
        self.cam2 = cam2
        
    def criar_matriz_projecao(self, camera1: PinholeCamera, camera2: PinholeCamera):
        """
        Cria a matriz de projeção das câmeras para realizar a triangulação
        """

        # Matriz de projeção (juntar rotação e translação e multiplicar por K)
        P1 = camera1.K @ np.hstack((camera1.world_R_cam, camera1.world_t_cam))
        P2 = camera2.K @ np.hstack((camera2.world_R_cam, camera2.world_t_cam))

        matriz_projecao = [P1, P2]

        return matriz_projecao

    # Essa função foi feita pensando no cv.sfm.triangulatePoints, mas infelizmente não está funcionando aqui e não é possível colocar a extensão do opencv sfm
    def juntar_pontos_2d(self, pts_cam1: np.ndarray, pts_cam2: np.ndarray): 
        """
        Pega dois pontos em 2D de duas câmeras diferentes, e junta eles
        """

        pontos2d = np.asarray([pts_cam1.T, pts_cam2.T])

        return pontos2d
    

    def fazer_triangulacao(self, pontos_cam1, pontos_cam2):
        """
        Realiza a triangulação entre dois pontos equivalentes de duas câmeras diferentes
        """

        # Garantindo que os pontos são arrays do numpy
        pontos_cam1 = np.asarray(pontos_cam1, dtype = np.float64)
        pontos_cam2 = np.asarray(pontos_cam2, dtype = np.float64)

        matriz_projecao = self.criar_matriz_projecao(self.cam1, self.cam2)
        pontos2d_2cam = self.juntar_pontos_2d(pontos_cam1, pontos_cam2)

        # Triangulação
        # pontos3D = cv.sfm.triangulatePoints(pontos2d_2cam, matriz_projecao)
        pontos3D = cv.triangulatePoints(matriz_projecao[0], matriz_projecao[1], pontos2d_2cam[0], pontos2d_2cam[1])

        # Converte as coordenadas homogêneas (dividir pela última coordenada)
        pontos3D = pontos3D[:3, :] / pontos3D[3, :]

        # Retornando no nosso modelo normal de visualização de pontos N x 3
        return pontos3D.T
    

if __name__ == '__main__':

    # Câmera
    K = np.array([
        [500,   0, 320],
        [  0, 500, 240],
        [  0,   0,   1]
    ], dtype=np.float64)

    distorcao = np.zeros(5)

    # Câmera 1 na origem
    R1 = np.eye(3)
    t1 = np.zeros((3, 1))

    # Câmera 2 deslocada para a direita
    R2 = np.eye(3)
    t2 = np.array([
        [-1],
        [ 0],
        [ 0]
    ], dtype=np.float64)

    camera1 = PinholeCamera(K, distorcao, R1, t1)
    camera2 = PinholeCamera(K, distorcao, R2, t2)

    # Ponto 3D real
    pontos_3d_reais = np.array([
        [0, 0, 5],
        [1, 0, 5],
        [0, 1, 5],
        [1, 1, 5]
    ], dtype=np.float64)

    # Projeta os pontos nas duas câmeras
    pontos_img1 = camera1.project(pontos_3d_reais)
    pontos_img2 = camera2.project(pontos_3d_reais)

    triangulacao = Triangulacao(camera1, camera2)

    pontos_3d_estimados = triangulacao.fazer_triangulacao(pontos_img1, pontos_img2)

    print("Pontos 3D reais:")
    print(pontos_3d_reais)

    print("\nPontos 3D estimados:")
    print(pontos_3d_estimados)