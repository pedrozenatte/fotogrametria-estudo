# Detecção de Cantos Harris

## Objetivo 
- Vamos entender os conceitos por trás da Detecção de Cantos Harris.
- Vamos ver as seguintes funções: cv.cornerHarris(), cv.cornerSubPix().

## Teoria
Sabemos que os cantos são regiões na imagem com grande variação de intensidade em todas as direções, mas é necessário saber encontrá-los de forma computacional. Uma tentativa inicial para encontrar esses cantos foi feita por Chris Harris e Mike Stephens. 

### Função intensidade acumulada: 
Basicamente, é encontrada a diferença de intensidade para um deslocamento de (u,v) em todas as direções em torno de um ponto específico.

$$
E(u,v) = \sum_{x,y} w(x,y)[I(x+u,y+v) - I(x,y)]^2
$$

- **$E(u,v)$:** Este é o valor de intensidade acumulada para um deslocamento $(u,v)$ em relação a um ponto de interesse na imagem.
- **$\sum_{x,y}$:** O somatório é uma soma sobre todos os pixels de uma janela ao redor de um ponto $(x,y)$. Isso quer dizer que, para cada ponto de interesse, você vai calcular a diferença de intensidade não apenas em um ponto isolado, mas em todos os pixels da vizinhança do ponto em questão.
- **$w(x,y)$:** Esta é uma função de janela, ou seja, ela é uma função que aplica pesos aos pixels dentro da janela. O objetivo da função de janela é suavizar a imagem, ou seja, dar mais peso aos pixels mais próximos do ponto central e menos peso para os pixels distantes. Em muitas implementações, uma função Gaussiana é usada, pois ela dá mais importância aos pixels ao redor do ponto central.
- **$I(x,y)$:** Esta é a intensidade da imagem no ponto $(x,y)$. A intensidade é simplesmente o valor de cor do pixel na imagem, que pode ser, por exemplo, a intensidade de brilho em uma imagem em escala de cinza.
- **$I(x+u,y+v)−I(x,y)$:** Essa parte da equação mede a diferença de intensidade entre dois pontos da imagem. O primeiro ponto é $(x,y)$, enquanto o segundo ponto é deslocado por $(u,v)$, que é um vetor de deslocamento. Esse deslocamento pode ser para a direita, esquerda, cima ou baixo da imagem. A ideia é medir como a intensidade muda quando você se desloca a partir de um ponto.

OBS: O somatório sobre x,y significa que, para cada ponto de interesse, não estamos apenas analisando um único valor de intensidade, mas sim a variação de intensidade em toda uma janela de pixels ao redor do ponto. Isso é importante porque os cantos (corners) não são pontos isolados, mas sim regiões da imagem onde há uma mudança significativa de intensidade em várias direções ao redor de um ponto.

Como os cantos possuem uma alta variação, precisamos de uma grande variação de intensidade em várias direções. Portanto, o objetivo é maximizar essa função $E(u,v)$, para encontrar pontos em que a intensidade varia significativamente em várias direções ao redor do ponto.

### Facilitando o cálculo
Para facilitar o cálculo e encontrar uma forma mais simples de expressar a função E(u,v), expansão de Taylor é aplicada. A expansão de Taylor é uma aproximação matemática usada para aproximar funções não lineares em torno de um ponto. Ela nos ajuda a linearizar a função de variação de intensidade em termos das suas derivadas.

$$
E(u,v) \approx \begin{bmatrix} u \\ v \end{bmatrix}^T M \begin{bmatrix} u \\ v \end{bmatrix}
$$

Em que:

- $u$ e $v$ são os deslocamentos que medem a variação de intensidade na direção $x$ e $y$ da imagem, respectivamente.
- $M$ é uma matriz que contém as informações de como a intensidade da imagem varia localmente, baseada nas derivadas $I_x$ (derivada no eixo $x$) e $I_y$ (derivada no eixo $y$).

### Matriz $M$

A matriz $M$ é a matriz de autovalores que captura a variação local da intensidade da imagem. Ela é dada por:

$$
M = \sum_{x,y} w(x,y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}
$$

Em que:

- $w(x,y)$ é a função de janela (geralmente uma gaussiana) que aplica pesos aos pixels ao redor do ponto central, ajudando a suavizar a imagem.
- $I_x$ e $I_y$ são as derivadas da imagem nas direções $x$ e $y$, respectivamente. Essas derivadas capturam como a intensidade da imagem muda nas direções horizontal e vertical.

### O Critério de Canto - $R$

Depois de calcular a matriz $M$, a detecção de cantos utiliza um critério de pontuação chamado $R$, que é uma combinação dos autovalores da matriz $M$.

O valor $R$ é calculado como:

$$
R = \text{det}(M) - k \cdot (\text{trace}(M))^2
$$

---
$\lambda_1$ e $\lambda_2$ são os autovalores de $M$.

- $\text{det}(M) = \lambda_1 \lambda_2$
- $\text{tr}(M) = \lambda_1 + \lambda_2$

--- 

Em que:

- $\text{det}(M)$ é o determinante da matriz $M$, que nos dá uma medida da variação de intensidade em todas as direções.
- $\text{trace}(M)$ é o traço da matriz $M$, que é a soma dos autovalores, e nos dá uma medida da variação média da intensidade.
- $k$ é uma constante empiricamente definida (geralmente entre 0.04 e 0.06), que controla a sensibilidade do detector de cantos.



#### Como $R$ Funciona

- Quando $|R|$ é pequeno, e $\lambda_1$ e $\lambda_2$ são pequenos, a região é **plana**.
  
- Quando $R < 0$, e $\lambda_1 \gg \lambda_2$ ou $\lambda_2 \gg \lambda_1$, a região é **uma borda**.

- Quando $R$ é grande, e $\lambda_1$ e $\lambda_2$ são grandes, com $\lambda_1 \approx \lambda_2$, a região é **um canto**.

## Implementação prática

### Detector de Cantos Harris no OpenCV
O OpenCV possui a função `cv.cornerHarris()` para esse propósito. Seus argumentos são:

- `img` - Imagem de entrada. Deve ser em escala de cinza e tipo float32.
- `blockSize` - Tamanho do vizinho (tamanho da janela) considerado para a detecção de cantos, dado em pixels.
- `ksize` - Parâmetro de abertura da derivada Sobel utilizada, ou seja, o tamanho da janela de convolução para calcular as variações de intensidade nas direções x e y. .
- `k` - Parâmetro livre do detector Harris na equação.

**Exemplo:**
```python
import numpy as np
import cv2 as cv

filename = 'chessboard.png' # Nome da imagem
img = cv.imread(filename) # Faz a leitura da imagem
# Converte a imagem para a escala cinza
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)  

# Converte para o tipo float32, pois a função cv.cornerHarris()
# requer que a imagem de entrada esteja no tipo de dado float32
gray = np.float32(gray)

# Detecção de cantos com conerHarris()
dst = cv.cornerHarris(gray, 2, 3, 0.04)
# OBS: dst é destination

#result is dilated for marking the corners, not important
dst = cv.dilate(dst,None)
# OBS: Essa função foi usada para aumentar a área dos pontos
# de canto detectados, fazendo com que eles fiquem mais visíveis.

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

# Exibição da imagem
cv.imshow('dst',img)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()
```

### Canto com Precisão Subpixel
Às vezes, podemos precisar encontrar os cantos com máxima precisão. O OpenCV vem com uma função chamada `cv.cornerSubPix()` que refina ainda mais os cantos detectados com precisão subpixel.
Primeiro precisamos encontrar os cantos Harris, em seguida, passamos os centróides desses cantos (pode haver vários pixels em um canto, pegamos o centróide deles) para refiná-los. Os cantos Harris são marcados com pixels vermelhos e os cantos refinados são marcados com pixels verdes. Sendo assim, para essa função, precisamos definir o critério para quando parar a iteração.
Quando paramos?
Paramos depois de um número especificado de iterações ou quando uma certa precisão é atingida, o que ocorrer primeiro. Também precisamos definir o tamanho da vizinhança que ele procura pelos cantos.

**Exemplo:**
```python
import numpy as np
import cv2 as cv

filename = 'chessboard2.jpg'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# find Harris corners
gray = np.float32(gray)
dst = cv.cornerHarris(gray,2,3,0.04)
dst = cv.dilate(dst,None)
# Limiarização
ret, dst = cv.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

# Now draw them
res = np.hstack((centroids,corners))
res = np.int0(res)
img[res[:,1],res[:,0]]=[0,0,255]
img[res[:,3],res[:,2]] = [0,255,0]

cv.imwrite('subpixel5.png',img)
```

## Perguntas
**1) Por que a escala cinza é melhor?**
Por possuir menos informação, pois assim, além de aumentarmos a eficiência computacional, teremos melhores padrões de intensidade (ao invés de analisar 3 canais RGB, analisaremos apenas 1 canal B) e menos ruído. 

#### Fonte: 
Link: https://docs.opencv.org/3.4/dc/d0d/tutorial_py_features_harris.html