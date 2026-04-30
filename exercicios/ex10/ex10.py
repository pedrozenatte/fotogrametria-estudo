# Bibliotecas
import cv2 as cv
import numpy as np
import glob
import os


class Calibrador:
    # Construtor
    def __init__(self, caminho_pasta: str, padrao_checkerboard = (7, 7)):
        # OBS: O padrão é de acordo com o tabuleiro (cantos internos horizontais, cantos internos verticais)
        self.caminho_pasta = caminho_pasta
        self.padrao_checkerboard = padrao_checkerboard
        
        # Critério de parada
        self.criterio = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Pontos 3D no tabuleiro
        self.objp = self.criar_pontos_3d() 

        # Pontos
        self.objpoints = []
        self.imgpoints = []

        # Parâmetros
        self.K = None
        self.dist_coef = None
        self.rvecs = None 
        self.tvecs = None
        

    
    def criar_pontos_3d(self):
        """
        Criação das coordenadas em 3D correspondentes ao padrão do tabuleiro de xadrez
        """

        # Vamos criar uma matriz de 3 colunas com o total de cantos internos, porque são as coordenadas em 3D desses cantos
        objp = np.zeros((self.padrao_checkerboard[0] * self.padrao_checkerboard[1], 3), np.float32)
        
        # Passar no formato de grade de coordenadas
        objp[:, :2] = np.mgrid[0: self.padrao_checkerboard[0], 0: self.padrao_checkerboard[1]].T.reshape(-1, 2)
        
        return objp
    
    def carregar_imagens(self):
        """
        Carrega as imagens da pasta especificada
        """
        imagens_jpeg = glob.glob(os.path.join(self.caminho_pasta, "*.jpeg"))

        return imagens_jpeg
    

    def detectar_cantos(self, mostrar_cantos_imagem = True):
        """
        Detectar os cantos das imagens selecionadas
        """

        # Colocando as imagens na memória
        imagens = self.carregar_imagens()

        if len(imagens) == 0:
            print('Problema no carregamento das imagens')
        
        tamanho_imagem = None

        for nome_imagem in imagens:
            imagem = cv.imread(nome_imagem)

            if imagem is None: 
                print(f'Erro ao carregar a imagem: {nome_imagem}')
            
            cinza = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
            tamanho_imagem = cinza.shape[::-1]

            # Detectando cantos
            flag, cantos = cv.findChessboardCorners(cinza, self.padrao_checkerboard, flags=cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK)
            # OBS: O parâmetro 'flags =...' é para melhorar a precisão, pois as fotos ficaram ruins

            if flag: 
                self.objpoints.append(self.objp)

                cantos_refinados = cv.cornerSubPix(cinza, cantos, (11, 11), (-1, -1), self.criterio)

                self.imgpoints.append(cantos_refinados)

                # Desenhando a imagem com os cantos
                if mostrar_cantos_imagem:
                    cv.drawChessboardCorners(
                        imagem,
                        self.padrao_checkerboard,
                        cantos_refinados,
                        flag
                    )

                    cv.imshow("Cantos detectados", imagem)
                    cv.waitKey(300)

            else:
                print(f"Cantos não encontrados em: {nome_imagem}")

        cv.destroyAllWindows()

        return tamanho_imagem


    def calibrar(self, mostrar_imagem = True):
        tamanho_imagem = self.detectar_cantos(mostrar_cantos_imagem = mostrar_imagem)
        
        if len(self.objpoints) == 0:
            # Não tem pontos 3D
            print('Erro, não existem pontos 3D')

        # Calibrando
        flag, self.K, self.dist_coef, self.rvecs, self.tvecs = cv.calibrateCamera(self.objpoints, self.imgpoints, tamanho_imagem, None, None)

        if flag: 
            erro = self.cal_erro()
            return self.K, self.dist_coef, erro
        
        else: 
            print('Erro durante a calibração')
            return 0


    def cal_erro(self):
        erro_medio = 0

        for i in range(len(self.objpoints)):
            imgpoints2, _ = cv.projectPoints(self.objpoints[i], self.rvecs[i], self.tvecs[i], self.K, self.dist_coef)

            # Calculando o erro
            erro = cv.norm(self.imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
            erro_medio += erro

            return erro


if __name__ == '__main__':
    calibrador = Calibrador(caminho_pasta = 'ex10/imagens_calibracao_reais', padrao_checkerboard = (7, 7))

    K, dist_coef, erro = calibrador.calibrar(mostrar_imagem = True)

    print("Matriz dos parâmetros intrínsecos da câmera:")
    print(K)

    print("\nCoeficientes de distorção:")
    print(dist_coef)

    print("\nErro médio de reprojeção:")
    print(erro)