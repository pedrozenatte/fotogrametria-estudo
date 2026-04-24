# Fluxo Óptico (Optical Flow)

## Objetivos
- Vamos entender os conceitos de fluxo óptico e sua estimativa usando o método de Lucas-Kanade
- Vamos usar funções como cv.`calcOpticalFlowPyrLK()` para rastrear pontos em um vídeo
- Vamos criar um campo de fluxo óptico denso usando `cv.calcOpticalFlowFarneback()`

## Teoria
Fluxo óptico é o padrão de movimento aparente dos objetos na imagem entre dois frames consecutivos, causado pelo movimento do objeto ou da câmera.
**Como assim? Ainda não entendi.**
Basicamente queremos entender como cada ponto da imagem se move de um frame para o próximo. 
Vamos supor que temos dois frames de um vídeo: 
- Frame 1
- Frame 2

Diante disso, para CADA pixel do frame 1, o algoritmo tenta responder para onde esse pixel foi no frame 2. 
Como resultado, temos um campo vetorial em 2D, sendo que cada pixel é um vetor. 
vetor = (dx, dy) --> deslocamento do pixel. 

Esse movemnto vem do objeto se movendo, da câmera se movendo, ou de ambos. 

#### Hipóteses do Fluxo Óptico
- A intensidade dos pixels não muda entre frames
- Pixels vizinhos têm movimento semelhante

#### Equação do Fluxo Óptico: 
Para um pixel:

$$
I(x, y, t) = I(x + dx, y + dy, t + dt)
$$
Isso representa a intensidade do pixal na posição (x, y) no tempo t. 
A cada dt de tempo que passa, estamos no frame da frente. 

Após expansão de Taylor:

$$
f_x \, u + f_y \, v + f_t = 0
$$

Onde:

$$
f_x = \frac{\partial I}{\partial x}, \quad
f_y = \frac{\partial I}{\partial y}, \quad
f_t = \frac{\partial I}{\partial t}
$$

$$
u = \frac{dx}{dt}, \quad
v = \frac{dy}{dt}
$$

Perceba que:
- u = dx / dt: velocidade na horizontal (eixo x)
- v = dy / dt: velocidade na vertical (eixo y)

---

**Exemplo da equação:**

Frames: 

**Frame t**
```
I(x,y,t)

10   20   30   40
10   20   30   40
10   20   30   40
```

**Frame t+1 (imagem deslocada 1 pixel para a direita)**
```
I(x,y,t+1)

0   10   20   30
0   10   20   30
0   10   20   30
```

**Pixel analisado**

```
(x, y) = (1, 1)
```

No frame t:
```
I(1,1,t) = 20
```

No frame t+1:
```
I(1,1,t+1) = 10
```

**Movimento real**
Observando o padrão:

```
I(1,1,t) = I(2,1,t+1)
```

Logo:

```
dx = 1
dy = 0
dt = 1
```

Velocidade:

```
u = dx/dt = 1
v = dy/dt = 0
```

**Gradientes espaciais (mesmo frame t)**

```
f_x = I(2,1,t) - I(1,1,t)
f_x = 30 - 20 = 10
```

```
f_y = I(1,2,t) - I(1,1,t)
f_y = 20 - 20 = 0
```

**Gradiente temporal**

```
f_t = I(1,1,t+1) - I(1,1,t)
f_t = 10 - 20 = -10
```

**Equação do fluxo óptico**

```
f_x * u + f_y * v + f_t = 0
```

Substituindo:

```
10 * 1 + 0 * 0 + (-10) = 0
```

```
10 - 10 = 0
```

**Resultado**

```
(u, v) = (1, 0)
```

O ponto se moveu 1 pixel para a direita.
Perceba que a mudança espacial causada pelo movimento + mudança temporal = 0

---

No exemplo, a gente sabia o movimento e, com isso, aplicamos a equação. Porém, na prática, temos 1 equação e 2 incógnitas ($u$ e $v$).

### Método Lucas-Kanade
Assume que pixels vizinhos têm o mesmo movimento, isto é, em uma pequena região (patch), **todos os pixels se movem igual**
Portanto: 
- $(u, v)$ é o mesmo para todos os pixels do patch.

Dessa forma, para cada pixel do patch, temos uma equação: 
$$
f_{x_i} u + f_{y_i} v + f_{t_i} = 0
$$

Ou seja, para um patch 3x3, temos 9 equações: 
$$
\begin{cases}
f_{x1} \, u + f_{y1} \, v + f_{t1} = 0 \\
f_{x2} \, u + f_{y2} \, v + f_{t2} = 0 \\
\vdots \\
f_{x9} \, u + f_{y9} \, v + f_{t9} = 0
\end{cases}
$$

Aqui, temos um sistema superdeterminado. 

Deixando na forma matricial: 

$$
\begin{bmatrix}
u \\
v
\end{bmatrix}
\ =
\begin{bmatrix}
\sum f_x^2 & \sum f_x f_y \\
\sum f_x f_y & \sum f_y^2
\end{bmatrix}^{-1}
\begin{bmatrix}
-\sum f_x f_t \\
-\sum f_y f_t
\end{bmatrix}
$$

Resolve-se com mínimos quadrados. 

**ATENÇÃO:** Lucas-Kanade funciona bem para pequenos movimentos, então a solução é utilizar pirâmides de imagem. 

## Código
### Função Lucas-Kanade
```python
cv.calcOpticalFlowPyrLK()
```

**Exemplo em Python**
```python
import numpy as np
import cv2 as cv
import argparse

# Pega o vídeo pelo terminal
parser = argparse.ArgumentParser(description='Exemplo de Lucas-Kanade Optical Flow')
parser.add_argument('image', type=str, help='caminho para o vídeo')
args = parser.parse_args()

cap = cv.VideoCapture(args.image)

# Parâmetros Shi-Tomasi
feature_params = dict(
    maxCorners=100,
    qualityLevel=0.3,
    minDistance=7,
    blockSize=7
)

# Parâmetros Lucas-Kanade
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03)
)

# Corer aleatórias
color = np.random.randint(0, 255, (100, 3))

# Lê o primeiro frame e converte para cinza
ret, old_frame = cap.read()
old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
# Detecta pontos iniciais
p0 = cv.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# Cira uma máscara para desenhar rastros
mask = np.zeros_like(old_frame)

# A cada iteração, lê um novo frame
while True:
    ret, frame = cap.read()
    if not ret:
        print('Sem frames!')
        break

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # calcular fluxo óptico
    p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    if p1 is not None:
        good_new = p1[st == 1]
        good_old = p0[st == 1]

    # desenhar trajetórias
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
        frame = cv.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)

    img = cv.add(frame, mask)
    cv.imshow('frame', img)

    if cv.waitKey(30) & 0xff == 27:
        break

    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)

cv.destroyAllWindows()
```

### Fluxo Óptico Denso 
O de Lucas-Kanade é esparso, ou seja, pega apenas alguns pontos. Dessa forma, uma outra alternativa é o denso, pois pega todos os pixels. 

**Função Farneback**
```python
cv.calcOpticalFlowFarneback()
```

**Exemplo em Python**
```python
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(cv.samples.findFile("vtest.avi"))

ret, frame1 = cap.read()
prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)

hsv = np.zeros_like(frame1)
hsv[..., 1] = 255

while True:
    ret, frame2 = cap.read()
    if not ret:
        print('Sem frames!')
        break

    next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)

    # Calcula o fluxo óptico (farneback)
    flow = cv.calcOpticalFlowFarneback(
        prvs, next, None,
        0.5, 3, 15, 3, 5, 1.2, 0
    )

    mag, ang = cv.cartToPolar(flow[..., 0], flow[..., 1])

    hsv[..., 0] = ang * 180 / np.pi / 2
    hsv[..., 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)

    bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

    cv.imshow('frame2', bgr)

    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
    elif k == ord('s'):
        cv.imwrite('opticalfb.png', frame2)
        cv.imwrite('opticalhsv.png', bgr)

    prvs = next

cv.destroyAllWindows()
```

#### Fonte
Link: https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html