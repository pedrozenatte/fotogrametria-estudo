# Bibliotecas 
import cv2 as cv 
from matplotlib import pyplot as plt

# Importanto a classe extratora
from ex01.ex01 import ExtratorFeature

# Constantes
QNT_PONTOS = 1000
LINHAS = 4
COLUNAS = 4

# Carregando a imagem 
imagem = cv.imread('../exercicios/ex01/simple.jpg', cv.IMREAD_GRAYSCALE)

if imagem is None:
    print('Erro ao carregar a imagem')
    exit()

# Lógica das peças do "quebra cabeça"
qnt_pecas = LINHAS * COLUNAS
pontos_por_celula = QNT_PONTOS // qnt_pecas

altura, largura = imagem.shape[:2]
altura_peca = altura // LINHAS
largura_peca = largura // COLUNAS

tot_kp = [] # Total de keypoints
tot_des = [] # Total de descritores

# Vamos percorrer a "matriz":
for linha in range(LINHAS):
    for coluna in range(COLUNAS):

        y_inicial = linha * altura_peca
        x_inicial = coluna * largura_peca

        # Calculando aonde estamos na imagem (eixo y)
        if linha == LINHAS - 1:
            y_final = altura

        else: 
            y_final = y_inicial + altura_peca
        
        # Calculando aonde estamos na imagem (eixo x)
        if coluna == COLUNAS - 1:
            x_final = largura
        
        else:
            x_final = x_inicial + largura_peca

        # Vamos pegar o pedaço da imagem que extrairemos os kp
        peca = imagem[y_inicial : y_final, x_inicial : x_final]

        # Construindo o extrator
        extrator = ExtratorFeature(qnt_pontos = pontos_por_celula)

        # Extraindo as features de cada peça em questão 
        kp, des = extrator.extrair_features(peca)

        # Deslocando o ponto de acordo com a imagem original
        for keypoint in kp:

            keypoint.pt = (keypoint.pt[0] + x_inicial, keypoint.pt[1] + y_inicial)
            tot_kp.append(keypoint)

        if des is not None:
            for descritor in des:
                tot_des.append(descritor)

        
print(f"Quantidade total de keypoints: {len(tot_kp)}")
# img = cv.drawKeypoints(imagem, tot_kp, None, color=(0,255,0), flags=0)

# plt.imshow(img)
# plt.show()

imagem_com_keypoints = cv.drawKeypoints(
    imagem,
    tot_kp,
    None,
    flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)

cv.imshow("ORB com distribuicao uniforme", imagem_com_keypoints)
cv.waitKey(0)
cv.destroyAllWindows()