# Bibliotecas
import numpy as np

class PinholeCamera:
    # Cosntrutor 
    def __init__(self, K: np.ndarray, dist_coefs: np.ndarray, world_R_cam: np.ndarray, world_t_cam: np.ndarray): 
        self.K = K
        self.dist_coefs = dist_coefs
        self.world_R_cam = world_R_cam
        self.world_t_cam = world_t_cam.reshape(3, 1) # Para multiplicação matricial, por isso o reshape
        self.K_inv = np.linalg.inv(K) # Inversa
    

    def project(self, world_pts_3d: np.ndarray) -> np.ndarray:
        """
        Pega os pontos 3D do mundo e descobrir onde eles aparecem na imagem
        """

        # Garantindo que os pontos estejam no formato N x 3 com array numpy
        world_pts_3d = np.asarray(world_pts_3d, dtype = np.float64)

        # Transformando de N x 3 para 3 X N por conta de algelin
        world_pts_3d = world_pts_3d.T

        # Convertendo os pontos 3D do mundo em pontos 2D da imagem
        pontos_imagem = self.K @ ((self.world_R_cam @ world_pts_3d) + self.world_t_cam)

        # Lembrando que esse pontos estão em coordenada homogêneas, o que significa que precisamos voltar para coordenadas comuns dividindo pela coordenada Z
        u = pontos_imagem[0, :] / pontos_imagem[2, :]
        v = pontos_imagem[1, :] / pontos_imagem[2, :]

        # OBS: u e v são os pontos da imagem no formato de pixel já

        # Retorna pontos 2D
        pontos_2d = np.vstack((u, v)).T # Estamos "empilhando" verticalmente

        return pontos_2d
    

    def unproject(self, image_pts_2d : np.ndarray) -> np.ndarray:
        """
        Pega pontos 2D da imagem e transformar em raios saindo da câmera

        Basicamente vamos saber de onde veio a luz do pixel
        """

        # Garantindo que seja um array
        image_pts_2d = np.asarray(image_pts_2d, dtype = np.float64)

        # Transformando os pontos 2D em coordenadas homogêneas
        u = image_pts_2d[:, 0]
        v = image_pts_2d[:, 1]
        
        image_pts_2d = np.vstack((u, v, np.ones_like(u))) 
        # OBS: ones_like é para garantir que o vetor de 1s terá o mesmo tamanho e formato do vetor u

        # Aplicando a inversa da matriz K para gerar as direções da luz que fizeram os pixels na câmera
        raios_camera_mundo = self.K_inv @ image_pts_2d

        # Como perdemos a noção de profundidade, essa direção pode indicar infinitos valores, então vamos normalizar para lidar com valores pequenos
        normas = np.linalg.norm(raios_camera_mundo, axis = 0)
        raios_camera_mundo = raios_camera_mundo / normas

        # Retorno em N x 3
        return raios_camera_mundo.T
    





if __name__ == "__main__":

    # Câmera
    K = np.array([
        [500,   0, 320],
        [  0, 500, 240],
        [  0,   0,   1]
    ], dtype=np.float64)

    dist_coefs = np.zeros(5)

    world_R_cam = np.eye(3)

    world_t_cam = np.zeros((3, 1))

    camera = PinholeCamera(
        K,
        dist_coefs,
        world_R_cam,
        world_t_cam
    )
    
    # Teste project
    pontos_3d = np.array([
    [0, 0, 5],
    [1, 0, 5],
    [0, 1, 5],
    [1, 1, 5]
    ], dtype=np.float64)

    pontos_2d = camera.project(pontos_3d)
    print('Project')
    print(pontos_2d)
    print()

    # Teste unproject
    vetores_direcao = camera.unproject(pontos_2d)
    print('Unproject')
    print(vetores_direcao)



