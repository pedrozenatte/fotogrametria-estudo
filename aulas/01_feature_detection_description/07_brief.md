# BRIEF (Binary Robust Independent Elementary Features)

# Teoria 
Sabemos que o SIFT usa um vetor de 128 dimensões para descritores. Como utiliza números de ponto flutuante, isso ocupa cerca de 512 bytes.
Da mesma forma, o SURF usa no mínimo 256 bytes (para 64 dimensões).
Criar esses vetores para milhares de características consome muita memória, o que não é viável para aplicações com recursos limitados, especialmente sistemas embarcados. Além disso, quanto maior o descritor, maior o tempo de matching.

---

**Ideia de otimização**
Nem todas essas dimensões são necessárias, então podemos comprimir usando:
- PCA
- LDA
- Hashing (LSH - Locality Sensitive Hashing)

Isso transforma descritores em strings binárias, o que permite usar distância de Hamming, que é muito rápida (XOR + contagem de bits).
Contudo, ainda precisamos calcular o descritor primeiro. 

OBS: Lembrando distância de Hamming: 
Mede a diferença entre duas strings (ou sequências binárias) de MESMO comprimento. Ela conta o número mínimo de posições em que os caracteres correspondentes diferem, correspondendo ao número de substituições necessárias para transformar uma string na outra.
Quanto maior a distância, mais diferentes elas são. 

---

Tendo em vista o calculo do descritor, a ideia do BRIEF é gerar descritores binários desde o início. 
Dessa forma, é feito:
1 - Pega um patch suavizado da imagem.
2 - Seleciona pares de pontos $(p, q)$.
3 - Compara intensidades:
- se $I(p) < I(q) \rightarrow 1$  
- senão $\rightarrow 0$  

Basicamente o algoritmo está perguntando se um ponto é mais escuro que o outro.
Repete isso para vários pares.

Resultado: uma string binária.
**Exemplo com 8 comparações:**
1 0 1 1 0 0 1 0
Isso virá o descritor. 

**ATENÇÃO:** O BRIEF **NÃO** detecta pontos, ele é apenas um descritor, então é necessário usar outro detector, como o FAST, SURF, SIFT, e depois aplicar ele. 


## Código
```python
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Leitura da imagem
img = cv.imread('simple.jpg', cv.IMREAD_GRAYSCALE)

# Detector (STAR)
star = cv.xfeatures2d.StarDetector_create()

# Descritor (BRIEF)
brief = cv.xfeatures2d.BriefDescriptorExtractor_create()

# Detecta keypoints
kp = star.detect(img, None)

# Calcula descritores
kp, des = brief.compute(img, kp)

print(brief.descriptorSize())
print(des.shape)
```