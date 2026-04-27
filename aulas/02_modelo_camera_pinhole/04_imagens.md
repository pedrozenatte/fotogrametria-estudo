# Imagens

Câmeras e lentes convertem a informação do mundo tridimensional em uma foto composta por pixels, que é armazenada no computador como fonte de dados para processamento posterior.
Matematicamente, uma imagem pode ser descrita como uma matriz, e ,no computador, ela ocupa um espaço contínuo de memória e pode ser representada como um array bidimensional. Assim, o programa não precisa distinguir entre uma matriz numérica e uma imagem(já que vão ser tratados como a mesma coisa).

Sendo assim, podemos considerar que uma imagem é:
- imagem = grade (grid) de pixels
- cada pixel = número (ou vetor de números)

OBS: A profundidade é guardada em outra matriz que está alinhada com a matriz de intensidade dos pixels. 

#### Operações básicas com imagens
https://docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html