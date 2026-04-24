# Introdução 

## Objetivos

Ao final de cada tema, devemos ser capazes de responder às perguntas a seguir:

### Detecção de Características
- O que é uma característica (ou ponto chave)
- Tipos comuns de detectores de características
- O que é um descritor
- Tipos comuns de descritores de características
- API do OpenCV para detecção e correspondência de características

### Correspondência de Características
- O que é correspondência de características
- Funções principais de distância
- Tipos comuns de algoritmos de correspondência
- API do OpenCV para correspondência de características
- RANSAC

### Modelo de Câmera Pin-hole
- Como representar a câmera com equações
- Quais variáveis/parâmetros são usados para representar uma câmera e qual é o seu significado (intrínsecos, extrínsecos, projeção, distorção)
- Projetando um ponto 3D para uma imagem
- Desprojetando um ponto de imagem para um raio

### Calibração de Câmera
- Como estimar os parâmetros da câmera
- Modelos de câmeras diferentes e como eles afetam a projeção/desprojeção

### Estimativa da Posição da Câmera
- Principais algoritmos para determinar a posição da câmera a partir das observações de pontos (PnP, PnP Ransac API)

### Estimativa de Estrutura
- Como determinar a posição 3D de um conjunto de pontos, dado múltiplas estimativas de câmeras (Problema de Triangulação, Correspondência Estéreo, API DLT do OpenCV)

### Transformações de Imagem
- Homografia
- Affine


## Método de Avaliação:

### Exercícios:

**1 - Implementação de uma classe em Python para extração de pontos-chave e descritores usando a API de detecção de características do OpenCV.**

A classe deve aceitar um tipo de característica (ORB, SIFT, SURF, etc.) como parâmetro e extrair pontos-chave e descritores de uma imagem. Escolha pelo menos 4 opções de características suportadas pelo OpenCV. Compare o tempo de execução de cada extração de características e descrição para 1000 pontos na mesma imagem. (Se você estiver se sentindo ousado, tente o Korneia também).

**2 - Distribuição desigual dos pontos-chave ORB**

Verificamos que os pontos-chave ORB fornecidos pelo OpenCV não estão distribuídos uniformemente na imagem. Você pode encontrar ou propor uma maneira de tornar a distribuição dos pontos-chave mais uniforme? Implemente em Python.

**3 - Classe Python para correspondência de características**

Implemente uma classe em Python para corresponder características detectadas com a classe criada no exercício 1. A classe deve suportar a correspondência de todos os tipos de características que você criou no exercício 1.

**4 - Investigação sobre o FLANN**

Investigue por que o FLANN pode lidar rapidamente com problemas de correspondência. Além do FLANN, quais são outras maneiras de acelerar a correspondência?

**5 - Correspondência errada em PnP**

Na correspondência de pontos de características, erros de correspondência inevitavelmente ocorrerão. O que acontece se colocarmos uma correspondência errada no PnP? Que métodos você pode pensar para evitar essas correspondências erradas?

**6 - Problemas ao combinar ORB e SIFT**

Quais são os problemas que você enfrentará ao tentar combinar pontos ORB com pontos SIFT?

**7 - Classe Python PinholeCamera**

Implemente uma classe Python chamada PinholeCamera. A classe deve ter os seguintes métodos:

**Construtor**
```python
def __init__(self, K: np.ndarray, dist_coefs: np.ndarray, world_R_cam: np.ndarray, world_t_cam: np.ndarray):
    """
    Construtor que recebe os parâmetros intrínsecos e extrínsecos da câmera.
    """
```

**Projeção**
```python
def project(self, world_pts_3d: np.ndarray) -> np.ndarray:
    """
    Projeta um conjunto de pontos 3D no plano da câmera.
    """
```

**Desprojeção**
```python
def unproject(self, image_pts_2d: np.ndarray) -> np.ndarray:
    """
    Desprojeta os pontos 2D detectados da imagem como raios da câmera.
    """
```

Escreva testes (com dados que você cria) que mostrem que sua classe funciona corretamente.

**8 - Estimativa das coordenadas 3D a partir de 2 conjuntos de observações 2D**

Implemente uma classe que receba dois conjuntos de observações 2D (coordenadas de pixels) e dois conjuntos de parâmetros da câmera e estime as coordenadas 3D dos pontos observados.

**9 - Estimativa da posição da câmera**

Implemente uma classe que receba um conjunto de pontos 3D e estime a posição da câmera.

**10 - Programa de calibração da câmera**

Escreva um programa de calibração para calibrar a câmera do seu celular. Para gerar as imagens de calibração, você pode exibir um tabuleiro de xadrez no monitor do seu computador. Como você avalia a qualidade da sua estimativa?

**11 - O que é uma Matriz de Homografia?**

O que é uma matriz de homografia e como você pode usá-la?

**12 - Estimativa da posição da câmera usando homografias**

Implemente uma classe Python que estime a posição da câmera dada uma marca plana, usando homografias.


#### Fonte 
Todo o conteúdo da primeira parte está aqui: 
Link: https://docs.opencv.org/3.4/db/d27/tutorial_py_table_of_contents_feature2d.html