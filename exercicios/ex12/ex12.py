# Bibliotecas 
import cv2 as cv
import numpy as np

# Importando classes
from ex07.ex07 import PinholeCamera


class ParamExtrinsecosHomografia: 
    # Construtor
    def __init__(self, cam: PinholeCamera, pontos_2d, pontos_3d_2d):
        self.cam = cam
        self.pontos_2d = pontos_2d
        self.pontos_3d_2d = pontos_3d_2d
        

    def calcular_homografia(self):
        """
        Calcula a homografia entre os pontos 2D e os pontos 3D que se fingem de 2D
        """

        homografia, _ = cv.findHomography(self.pontos_2d, self.pontos_3d_2d, cv.RANSAC, 5.0)
        
        return homografia
    

    def estimar_pose_homografia(self):
        """
        Estima a pose da câmera utilizando homografia
        """

        # Calcula a homografia
        homografia = self.calcular_homografia()

        # Decompões a homografia para obter a rotação e a translação
        num_solucoes, rotacao, translacao, _ = cv.decomposeHomographyMat(homografia, self.cam.K)

        return (rotacao, translacao, num_solucoes)
    

if __name__ == '__main__':
    # Definindo pontos 2D da imagem
    pontos_2d = np.array([
        [200, 200],  
        [400, 200],  
        [400, 400],  
        [200, 400]   
    ], dtype=np.float32)

    # Definindo os pontos 2D do marcador no plano (coordenadas no sistema do marcador)
    pontos_3d_2d = np.array([
        [0, 0],  
        [1, 0],  
        [1, 1],  
        [0, 1]   
    ], dtype=np.float32)

    # Câmera
    K = np.array([
        [500,   0, 320],
        [  0, 500, 240],
        [  0,   0,   1]
    ], dtype=np.float64)

    # Valores reais da câmera
    dist_coefs = np.zeros(5)

    world_R_cam = np.eye(3)

    world_t_cam = np.zeros((3, 1))

    camera = PinholeCamera(K, dist_coefs, world_R_cam, world_t_cam)

    # Parâmetros Extrínsecos
    parametros = ParamExtrinsecosHomografia(camera, pontos_2d, pontos_3d_2d)

    # Realizando a estimação
    R_estimado, t_estimado, num_solucoes = parametros.estimar_pose_homografia()

    print(f'Número de soluções encontradas: {num_solucoes}\n')
    print('Rotação real:')
    print(world_R_cam)
    print()
    for i in range(num_solucoes):
        print('Rotação estimada:')
        print(R_estimado[i])
        print()
    
    print('\n\n')

    print('Translação real:')
    print(world_t_cam)
    print()
    for i in range(num_solucoes):
        print('Translação estimada:')
        print(t_estimado[i])
        print()