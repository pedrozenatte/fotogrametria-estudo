# ORB (Oriented FAST and Rotated BRIEF)

## Teoria
Esse algoritmo é uma alternativa ao SIFT e SURF, considerando: 
- Custo computacional
- Desempenho de matching
- Patentes (o ORB não é patenteado)

O ORB é basicamente uma combinação de: 
- FAST: detector de keypoints
- BRIEF: descritor

Com várias melhorias. 

### Detecção de pontos
- Usa FAST para detectar pontos
- Usa Harris score para selecionar os melhores N pontos
- Usa pirâmide de imagem: multiescala

Contudo o FAST tem um **problema** de não calcular a orientação, portanto, não é invariante à rotação. 

#### Como ele faz isso? 
- Calcula o centroide ponterado por intensidade do patch. 
    - Pixels mais claros pesam mais 
    - Pixels mais escuros pesam menos
- A orientação é do centro do patch para o centroide, ou seja, pega a região circular em volta do keypoint, calcula o centróide, a direção é saindo do keypoint e chegando até o centróide. 

Uma vez que temos um vetor, podemos calcular o ângulo desse vetor, e com o ângulo conseguimos rotacionar a imagem para deixá-la invariante à rotação. 

### Descritor 
O ORB usa o BRIEF, mas com ajuste de rotação, pois é plicada a rotação no padrão de comparação baseado na orientação do keypoint.

## Código
```python
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

img = cv.imread('simple.jpg', cv.IMREAD_GRAYSCALE)

# Criar ORB
orb = cv.ORB_create()

# Detectar keypoints
kp = orb.detect(img, None)

# Calcular descritores
kp, des = orb.compute(img, kp)

# Desenhar
img2 = cv.drawKeypoints(img, kp, None, color=(0,255,0), flags=0)

plt.imshow(img2)
plt.show()
```

OBS:
```python
# Podemos fazer em uma linha:
kp, des = orb.detectAndCompute(img, None)
```