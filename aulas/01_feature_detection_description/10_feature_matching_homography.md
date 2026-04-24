# Correspondência de Características + Homografia para Encontrar Objetos (Feature Matching + Homography to find Objects)

## Teoria
Anteriormente (feature matching), fizemos:
- Pegamos uma imagem de consulta (queryImage)
- Detectamos pontos de interesse nela
- Pegamos outra imagem (trainImage)
- Detectamos pontos nela também
- Fizemos o matching entre os pontos

Como resultado, encontramos parte de um objeto dentro de outra imagem mais complexa. Essa informação já é suficiente para localizar o objeto completo. 

Agora, vamos fazer o seguinte: 

### Ideia principal
Usamos a função: 
```python
cv.findHomography()
```
A qual recebe pontos correspondentes entre duas imagens e calcula a transformação de perspectiva. 

Depois usamos: 
```python
cv.perspectiveTransform()
```
Para projetar o objeto da primeira imagem na segunda imagem. 
**IMPORTANTE:** É preciso de pelo menos 4 pontos corretos. 

### Problema 
Quando fizemos o matching, seja com SIFT, SURF, ORB..., obtivemos pares de pontos, porém nem todos esses matches são corretos, já que, mesmo com o Ratio Test, pode haver texturas parecidas (como janelas iguais), ruído, iluminação, repetição de padrões e entre outras variáveis. Como resultado, temos matches inconsistentes (outliers). 
**O que acontece se usarmos todos os pontos?**
Se aplicarmos a Homography com pontos ruins, a transformação fica errada. 
Por exemplo, se temos 10 matches bons e 5 deles são errados. Se usarmos todos, a transformação vai tentar considerar todos, e como resultado a imagem fica distorcida. 

Diante disso, a solução encontrada foi:
- **RANSAC**
    - pega 4 pontos aleatórios
    - calcula uma homografia
    - testa TODOS os outros pontos
    - vê quantos concordam com essa transformação

    Basicamente remove outliers (RANSAC)
- Ou **LEAST_MEDIAN**

Classificação:
- Inliers: matches corretos
- Outliers: matches errados

A função retorna uma máscara indicando isso.

## Código
```python
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

img1 = cv.imread('box.png', cv.IMREAD_GRAYSCALE)
img2 = cv.imread('box_in_scene.png', cv.IMREAD_GRAYSCALE)

# Inicializa o SIFT 
sift = cv.SIFT_create()

# Detecta e descreve os keypoints 
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# Parâmetros do FLANN
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

# Inicializa o FLANN
flann = cv.FlannBasedMatcher(index_params, search_params)

# Realiza o match
matches = flann.knnMatch(des1, des2, k=2)

# Ratio Test
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

# Verifica se tem pontos suficientes
# Precisa de pelo menos 4, mas usa 10 por segurança
if len(good) > MIN_MATCH_COUNT:
    # Se tiver o mínimo: 
    # extrai coordenadas dos pontos
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

    # Calcula homografia usando RANSAC
    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

    # Define o retângulo do objeto (são 4 cantos da img 1)
    h, w = img1.shape

    pts = np.float32([[0,0],[0,h-1],[w-1,h-1],[w-1,0]]).reshape(-1,1,2)

    # Projeta na segunda imagem
    dst = cv.perspectiveTransform(pts, M)

    # Desenha o contorno
    img2 = cv.polylines(img2, [np.int32(dst)], True, 255, 3, cv.LINE_AA)

else:
    print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
    matchesMask = None

# Desenho
draw_params = dict(
    matchColor=(0,255,0),
    singlePointColor=None,
    matchesMask=mask.ravel().tolist(),
    flags=2
)

img3 = cv.drawMatches(img1, kp1, img2, kp2,
                      good, None, **draw_params)

plt.imshow(img3, 'gray')
plt.show()
```


#### Fonte: 
Link: https://docs.opencv.org/3.4/d1/de0/tutorial_py_feature_homography.html