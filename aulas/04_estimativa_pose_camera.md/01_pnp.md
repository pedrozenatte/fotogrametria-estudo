# PnP (Perspective-n-Points) - Estimativa de pose usando n pontos.

Anteriormente, fizemos a calibração da câmera para obtermos os parâmetros intrínsecos da câmera, isto é, a matriz da câmera. Nesse momento queremos a posição da câmera, ou seja, a rotação + translação. 
Sendo assim, PnP é um problema clássico de visão computacional usado para estimar a pose da câmera: 
- Posição da câmera no espaço (x, y, z)
- Orientação da câmera (rotação)

É possível obter essas informações a partir de pontos 3D conhecidos no mundo e os seus correspondentes na imagem 2D 

## Ideia Principal
A ideia principal do PnP é relativamente simples, pois o algoritmo recebe alguns pontos conhecidos no mundo real, com coordenadas 3D, e também recebe as posições desses mesmos pontos na imagem da câmera, agora representados em coordenadas 2D (pixels). A partir dessas correspondências entre mundo real e imagem, o algoritmo calcula qual deve ser a rotação e a translação da câmera para que aqueles pontos 3D sejam projetados exatamente nos pixels observados.

Imagine que conhecemos alguns pontos reais de um objeto: 
```text
Ponto A = (0,0,0)
Ponto B = (1,0,0)
Ponto C = (1,1,0)
Ponto D = (0,1,0)
```

Esses pontos estão no mundo real (3D).
Agora, a câmera olha para esse objeto e detecta onde esses pontos aparecem na imagem:
```text
A -> pixel (320,240)
B -> pixel (400,250)
C -> pixel (390,330)
D -> pixel (310,320)
```

**O problema do PnP é:**
**Qual é a posição e rotação da câmera para que esses pontos 3D projetem exatamente nesses pixels 2D?**
Sendo assim, dada uma imagem de um padrão, podemos utilizar essas informações para calcular sua pose, ou seja, como o objeto está situado no espaço, como ele está rotacionado, deslocado etc.
Basicamente o PnP busca encontrar os 6 graus de liberdade que alinham os pontos 3D do mundo com os pontos 2D observados na imagem.

---

**3 graus de translação**
Representam movimento no espaço:
- eixo X: esquerda/direita
- eixo Y: cima/baixo
- eixo Z: frente/trás

**3 graus de rotação**
Representam orientação:
- Roll: inclinação lateral
- Pitch: inclinação para frente/trás
- Yaw: rotação horizontal

---

**Cuidado:** No PnP, podemos perder graus de liberdade quando há poucos pontos, os pontos são colineares, mal distribuídos ou há ambiguidade geométrica. 


**ATENÇÃO:** A câmera deve estar calibrada, até porque um dos parâmetros da função para calcular o que queremos aqui precisa da matriz da câmera. 


## Como fazemos isso? 

Primeiro, vamos carregar a matriz da câmera e os coeficientes de distorção obtidos anteriormente:
```python
import numpy as np
import cv2 as cv
import glob

# Carrega dados salvos anteriormente
with np.load('B.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
```

Agora vamos criar uma função draw, que recebe:
- os cantos do tabuleiro (obtidos com cv.findChessboardCorners())
- os pontos do eixo para desenhar os eixos 3D

Depois, como no caso anterior, criamos:
- os critérios de parada
- os pontos do objeto (object points)
- os pontos do eixo (axis points)

Os pontos do eixo são pontos no espaço 3D usados para desenhar os eixos.
```python
criteria = (
    # refinamento para quando atingir no máximo 30 
    # iterações ou quando a melhoria ficar menor que 0.001.
    cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)

# Criação de pontos 3D conhecidos
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Eixos 3D
axis = np.float32([
    [3,0,0],
    [0,3,0],
    [0,0,-3]
]).reshape(-1,3)
```
Agora, como de costume, carregamos cada imagem.
Procuramos o padrão 7x6. Se encontrado, refinamos os cantos usando subpixels.

Depois, para calcular a rotação e a translação, usamos:
- `cv.solvePnPRansac()`

Uma vez obtidas as matrizes de transformação, usamos elas para projetar os pontos do eixo no plano da imagem.

Logo, o codigo fica: 
```python
# Percorre todas as imagens
for fname in glob.glob('left*.jpg'):

    img = cv.imread(fname)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    # Procurando cantos
    ret, corners = cv.findChessboardCorners(gray, (7,6),None)

    if ret == True:

        # Refinamento dos cantos
        corners2 = cv.cornerSubPix(
            gray,
            corners,
            (11,11),
            (-1,-1),
            criteria
        )

        # Encontra vetores de rotação e translação
        ret, rvecs, tvecs = cv.solvePnP(
            objp, # Pontos 3D conhecidos
            corners2, # Pontos 2D na imagem
            mtx, # Matriz da câmera
            dist # Coef. distorção
        ) # OBS: ret é um booleano indicando se a opreção deu certo

        # projeta pontos 3D no plano da imagem
        imgpts, jac = cv.projectPoints(
            axis,
            rvecs,
            tvecs,
            mtx,
            dist
        )

        img = draw(img,corners2,imgpts)

        cv.imshow('img',img)

        k = cv.waitKey(0) & 0xFF

        if k == ord('s'):
            cv.imwrite(fname[:6]+'.png', img)

cv.destroyAllWindows()
```
**OBS:** O desenho dos eixos é uma forma visual de validar o resultado. 
Se tudo estiver correto:
- os eixos ficam “presos” ao tabuleiro
- acompanham a perspectiva corretamente
- parecem realmente existir na cena

#### Fonte
https://docs.opencv.org/3.4/d7/d53/tutorial_py_pose.html

https://www.youtube.com/watch?v=0JGC5hZYCVE
https://www.youtube.com/watch?v=RR8WXL-kMzA

Tutorial completo de como construir uma aplicação em tempo real para estimar a pose da câmera, com o objetivo de rastrear um objeto texturizado com seis graus de liberdade, dada uma imagem 2D e seu modelo 3D texturizado: https://docs.opencv.org/3.4/dc/d2c/tutorial_real_time_pose.html
