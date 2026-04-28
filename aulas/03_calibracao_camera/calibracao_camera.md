# Calibração de Câmera

## Objetivo 
Vamos entender: 
- tipos de distorção causados por câmeras
- como encontrar os parâmetros intrínsecos e extrínsecos
- como remover a distorção das imagens usando esses parâmetros

## Fundamentos
Como já vimos anteriormente, algumas câmeras do tipo pinhole introduzem distorções significativas nas imagens.
As duas principais distorções são: 
- distorção radial
- distorção tangencial

**Distorção radial**
A distorção radial faz com que linhas retas pareçam curvas. Essa distorção aumenta quanto mais os pontos estão afastados do centro da imagem.

$$
x_d = x \left(1 + k_1 r^2 + k_2 r^4 + k_3 r^6 \right)
$$

$$
y_d = y \left(1 + k_1 r^2 + k_2 r^4 + k_3 r^6 \right)
$$

**Distorção tangencial**
A distorção tangencial ocorre porque a lente da câmera não está perfeitamente paralela ao plano de imagem. Assim, algumas regiões da imagem podem parecer mais próximas do que o esperado.

$$
x_d = x + 2 p_1 x y + p_2 (r^2 + 2x^2)
$$

$$
y_d = y + p_1 (r^2 + 2y^2) + 2 p_2 x y
$$

Dessa forma, precisamos encontrar cinco parâmetros, conhecidos como coeficientes de distorção:

Distortion coefficients: $(k_1, k_2, p_1, p_2, k_3)$

Além disso, precisamos de outras informações, como os **parâmetros intrínsecos e extrínsecos** da câmera.
Os parâmetros intrínsecos são específicos de cada câmera. 
- Eles incluem informações como distância focal (fx, fy) e centro óptico (cx, cy). 

Além disso, esses parâmetros podem ser usados para criar a matriz da câmera, que serve para remover a distorção causada pela lente. Essa matriz é única para cada câmera e, uma vez calculada, pode ser reutilizada em outras imagens capturadas pela mesma câmera.

Camera matrix:

$$
K =
\begin{bmatrix}
f_x & 0 & c_x \\
0 & f_y & c_y \\
0 & 0 & 1
\end{bmatrix}
$$

Os parâmetros extrínsecos correspondem aos vetores de rotação e translação que transformam as coordenadas de um ponto 3D para o sistema de coordenadas da câmera.

Para aplicações estéreo, essas distorções precisam ser corrigidas primeiro. 

#### Encontro dos parâmetros
Para encontrar esses parâmetros, devemos fornecer imagens de um padrão bem definido, por exemplo, um tabuleiro de xadrez. Identificamos pontos específicos cujas posições relativas já conhecemos, como os cantos dos quadrados. Sabemos as coordenadas desses pontos no mundo real e também na imagem, então podemos resolver os coeficientes de distorção. Para melhores resultados, precisamos de **pelo menos 10 padrões de teste.**

## Código
O OpenCV fornece algumas imagens de um tabuleiro de xadrez (em samples/data/left01.jpg até left14.jpg), então vamos utilizá-las.
Para calibrar a câmera, precisamos de:

- pontos 3D do mundo real
- pontos 2D correspondentes na imagem

Os pontos 2D (image points) podem ser obtidos diretamente da imagem (são os cantos onde quadrados pretos se encontram).
Já os pontos 3D (object points) são posições relativas do que está sendo detectado. 
**Como assim?**
Basicamente não precisamos saber exatamente como é a d istância de um quadrado do tabuleiro até outro, o que importa saber é a estrutura, isto é, são IGUALMENTE espaçados, então podemos inventar pontos, desde que eles estejam igualmente espaçados. 

#### Configuração
Para encontrar o padrão do tabuleiro, usamos:
```python
cv.findChessboardCorners()
```

Devemos informar o tamanho do padrão (por exemplo, 7×6). Essa função retorna:

- os cantos encontrados
- um valor booleano (True se encontrou o padrão)

Os pontos são ordenados da esquerda para a direita, de cima para baixo.

---
**Observação:**
Essa função pode não funcionar em todas as imagens. Uma boa abordagem é:

- capturar frames da câmera  
- procurar o padrão em cada frame  
- quando encontrar, salvar os pontos  
- repetir até ter padrões suficientes  

Também é possível usar um padrão circular com:

`cv.findCirclesGrid()`

Esse método requer menos imagens.

Depois de encontrar os cantos, podemos melhorar a precisão com:

`cv.cornerSubPix()`

E desenhar com:

`cv.drawChessboardCorners()`

---

**Código:**
```python
import numpy as np
import cv2 as cv
import glob

# Critério de parada
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Criação de pontos 3D no tabuleiro
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

objpoints = []
imgpoints = []

images = glob.glob('*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, corners = cv.findChessboardCorners(gray, (7,6), None)

    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        cv.drawChessboardCorners(img,(7,6),corners2,ret)
        cv.imshow('img',img)
        cv.waitKey(500)

cv.destroyAllWindows()
```

**Calibração:**
```python
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)
```
Isso retorna:
- matriz da câmera
- coeficientes de distorção
- vetores de rotação
- vetores de translação


**Remoção de distorção:**
```python
cv.getOptimalNewCameraMatrix()
```
- alpha = 0: remove bordas ruins
- alpha = 1: mantém todos os pixels

Exemplo: 
```python
img = cv.imread('left12.jpg')
h, w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
```

1) Método 1: cv.undistort()
```python
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

cv.imwrite('calibresult.png', dst)
```

2) Método 2: Remapeamento
```python
mapx, mapy = cv.initUndistortRectifyMap(
    mtx, dist, None, newcameramtx, (w,h), 5)

dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

x, y, w, h = roi
dst = dst[y:y+h, x:x+w]

cv.imwrite('calibresult.png', dst)
```

**Erro de Reprojeção:**
Esse erro mede a precisão dos parâmetros encontrados.

Quanto mais próximo de zero, melhor.
```python
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(
        objpoints[i], rvecs[i], tvecs[i], mtx, dist)

    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2) / len(imgpoints2)
    mean_error += error

print("total error: {}".format(mean_error/len(objpoints)))
```



#### Fonte
Link: 
https://docs.opencv.org/3.4/dc/dbb/tutorial_py_calibration.html

https://www.youtube.com/watch?v=26nV4oDLiqc&list=PLgnQpQtFTOGTPQhKBOGgjTgX-mzpsOGOX&index=17
https://www.youtube.com/watch?v=_-BTKiamRTg
https://www.youtube.com/watch?v=Hz8kz5aeQ44

https://programmer.group/opencv-notes-10-camera-model-and-calibration.html
