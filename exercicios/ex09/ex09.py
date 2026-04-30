# Bibliotecas
import cv2 as cv
import numpy as np

# Importação de classes
from ex07.ex07 import PinholeCamera

class ParamExtrinsecos:
    # Construtor 
    def __init__(self, cam: PinholeCamera):
        self.cam = cam

    def estimar_pose_camera(self, pontos_3d: np.ndarray, pontos_2d: np.ndarray):
        """
        Estima os parâmetros extrínsecos a partir de pontos 3D conhecidos e os pontos 2D gerados na imagem.  
        """

        # Garantindo que os pontos passados estejam no formado array numpy
        pontos_2d = np.asarray(pontos_2d, dtype = np.float64)
        pontos_3d = np.asarray(pontos_3d, dtype = np.float64)

        # Aplicando o PnP
        flag, rvec, tvec, _ = cv.solvePnPRansac(pontos_3d, pontos_2d, self.cam.K, self.cam.dist_coefs)

        if not flag: 
            print('Não foi possível capturar os parâmetros extrínsecos')

        # Em vista do formato da rotação estar diferente do comum, existe a seguinte função: 
        R, _ = cv.Rodrigues(rvec)

        return (R, tvec)
    

if __name__ == '__main__':
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

    # Pontos 3D conhecidos
    pontos_3d = np.array([
        [0, 0, 5],
        [1, 0, 5],
        [0, 1, 5],
        [1, 1, 5],
        [2, 1, 5],
        [1, 2, 5]
    ], dtype=np.float64)

    # Pegando as coordenadas em pixels
    pontos_2d = camera.project(pontos_3d)

    # Parâmetros Extrínsecos
    parametros = ParamExtrinsecos(camera)

    # Realizando a estimação
    R_estimado, t_estimado = parametros.estimar_pose_camera(pontos_3d, pontos_2d)

    print('Rotação real:')
    print(world_R_cam)
    print()
    print('Rotação estimada:')
    print(R_estimado)
    print('\n\n')
    print('Translação real:')
    print(world_t_cam)
    print()
    print('Translação estimada:')
    print(t_estimado)