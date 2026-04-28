# Conceitos básicos de homografia 

## O que é a matriz de homografia?
A  homografia planar relaciona a transformação entre dois planos (até um fator de escala):

$$
s
\begin{bmatrix}
x' \\
y' \\
1
\end{bmatrix}
\ =
\begin{bmatrix}
h_{11} & h_{12} & h_{13} \\
h_{21} & h_{22} & h_{23} \\
h_{31} & h_{32} & h_{33}
\end{bmatrix}
\begin{bmatrix}
x \\
y \\
1
\end{bmatrix}
$$

A matriz de homografia é uma matriz 3x3, mas com 8 graus de liberdade (DoF), já que ela é estimada até uma escala.
Essa matriz nos descreve como os pontos de uma imagem mudam para outra, ou seja, se os pontos estão em uma superfície plana, como um tabuleiro, folha, parede, placa ou marcador, a homografia descreve como esses pontos mudam de uma imagem para outra. Estamos transformando pontos de um plano para outro plano. 

#### Fonte: 
https://docs.opencv.org/3.4/d9/dab/tutorial_homography.html

https://www.youtube.com/watch?v=MlaIWymLCD8