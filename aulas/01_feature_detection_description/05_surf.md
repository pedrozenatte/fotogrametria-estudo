# Introdução ao SURF (Speeded-Up Robust Features)

## Objetivos
- Vamos ver os conceitos básicos do SURF
- Vamos ver as funcionalidades do SURF no OpenCV

## Teoria

Anteriormente, vimos o SIF para detecção e descrição de keypoints, porém ele é lento, então surgiu a necessidade de uma versão mais rápida. 
Em 2006, Bay, Tuytelaars e Van Gool propuseram o algoritmo SURF (Speeded-Up Robust Features), que, como o nome sugere, é uma versão acelerada do SIFT.

### Ideia principal

No SIFT, usase Difference of Gaussians (DoG)como aproximação do LoG. 
No SURF, vai além e usa Box Filters para aproximar o LoG. 
A grande vantagem disso é que pode ser calculado rapidamente usando imagens integrais e permite o processamento muito mais rápido e paralelo, além de usar o determinante da matriz Hessiana para detectar pontos. 

### Orientação de um keypoint
Para definir a orientação do keypoint e, assim, deixar a estrutura invariante à rotação, usa-se respostas de wavelets nas direções horizontal e vertical (usando uma janela deslizante de 60°). 

---

Modo rápido: U-SURF
- Não calcula orientação
- Mais rápido
- Funciona bem até ±15°

No OpenCV:
```python
upright = 0 # calcula orientação
upright = 1 # não calcula (mais rápido)
```

---

### Descritor 
Após encontrar o keypoint e sua orientação, o SURF cria um vetor que descreve a região ao redor do ponto. 
Para fazer isso, é pego um quadrado ao redor do ponto, com o tamanho dependendo da escala (para ser invariante de escala).
Após isso, divide em 16 sub-regiões e, para cada região, calcula-se: 
$$
\mathbf{v} = \left( \sum dx,\; \sum dy,\; \sum |dx|,\; \sum |dy| \right)
$$

Tanto dx quando dy são respostas de wavelet:
- dx é variação horizontal 
- dy é variação vertical

OBS: Usa-se o módulo para capturar intensidade independente do sinal, pois borda clara ou borda escura vão contar como variação forte. 

Cada uma das sub 16 regiões gera 4 valores, como mostrado, e como são 16 regiões, temos um vetor concatenado ao final de 64 dimensões. Esse vetor é o nosso descritor.

### Matching de pontos
O Matching é feito com distância euclidiana também, mas aqui tem o auxilio do Laplaciano para ser mais rápido, pois com o Laplaciano é possível diferenciar blobs claros de escuros, então a comparação é feita apenas com o mesmo tipo. 

## Código
```python
# Carregando a imagem em escala cinza
img = cv.imread('fly.png', cv.IMREAD_GRAYSCALE)

# Criação do SURF
surf = cv.xfeatures2d.SURF_create(400) # 400 é qnt de pontos para detectar

# Detectar pontos + descritores
kp, des = surf.detectAndCompute(img, None)

# Ver threshold autal
print(surf.getHessianThreshold())  # 400

# Aumentando o threshold
# Podemos ajustar dinamicamente sem recriar o objeto.
surf.setHessianThreshold(50000)
kp, des = surf.detectAndCompute(img, None)
print(len(kp))  # menos pontos
# Ficou com menos pontos, pois se aumentar muito
# Só mantém pontos muito fortes

# Desenhar keypoints
img2 = cv.drawKeypoints(img, kp, None, (255,0,0), 4)
plt.imshow(img2), plt.show()
```

#### Modo U-SURF (mais rápido)
Aqui não calcula rotação, então é mais rápido, mas fica variante à rotação (se a imagem rotacionar, perdeu os pontos). 
```python
surf.setUpright(True)
kp = surf.detect(img, None)
```

#### Mudando tamanho do descritor
Modo estendido ative um descritor maior, e nisso ele tem 128 dimensões. 
```python
print(surf.descriptorSize())  # 64
surf.setExtended(True)
kp, des = surf.detectAndCompute(img, None)
print(des.shape)  # (N, 128)
```

#### Fonte: 
Link: https://docs.opencv.org/3.4/df/dd2/tutorial_py_surf_intro.html