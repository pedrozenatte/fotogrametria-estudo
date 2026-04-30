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
    

if __name__ == "__main__":
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

    pontos_3d = np.array([
    [0, 0, 5],
    [1, 0, 5],
    [0, 1, 5],
    [1, 1, 5]
    ], dtype=np.float64)

    pontos_2d = camera.project(pontos_3d)

    print(pontos_2d)

    