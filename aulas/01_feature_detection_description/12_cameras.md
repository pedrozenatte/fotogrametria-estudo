# O que as Câmeras realmente medem?
As câmeras não capturam diretamente o mundo em 3D, elas registram uma projeção 2D desse mundo.

Dessa forma, o que uma câmera realmente mede é a intensidade da luz que chega até ela.

No interior da câmera existe um sensor, que é um chip sensível à luz. Esse chip é responsável por medir a quantidade de luz recebida ao longo de um determinado intervalo de tempo. Ele é dividido em milhares (ou milhões) de pequenas regiões chamadas pixels.
Cada pixel funciona como um sensor individual que mede a luz localmente. Em termos físicos, isso pode ser entendido como uma contagem de fótons (as menores unidades de luz) que atingem aquela região do sensor. Portanto, o sensor da câmera não fornece uma única medida, mas sim um grande conjunto de medições distribuídas espacialmente — uma para cada pixel.
Assim, ao capturar uma imagem, a câmera está essencialmente registrando quantos fótons atingem cada pixel do sensor.
Quando adicionamos uma lente (ou consideramos o modelo pinhole), a luz proveniente de diferentes direções no espaço é direcionada para pontos específicos do sensor. Isso faz com que cada pixel passe a corresponder a uma direção no espaço.
Dessa forma, a imagem formada é resultado da seguinte ideia:
- cada pixel mede a intensidade da luz que chega de uma determinada direção.

Em resumo, uma câmera gera imagens ao mapear direções do espaço para pixels e medir a intensidade da luz em cada um deles. 

# Medições geométricas usando câmeras
Nosso objetivo é utilizar câmeras para realizar medições geométricas do ambiente.
Para isso, exploramos o comportamento da luz: uma fonte ilumina a cena, os objetos refletem essa luz e parte dela chega até a câmera. Essa luz refletida é direcionada para o sensor, atingindo posições específicas do chip. Como consequência, determinados pixels registram maior intensidade.

O ponto central é entender o seguinte:
qual ponto do ambiente corresponde a qual pixel na imagem.
Essa relação é o que permite extrair informação geométrica a partir de imagens.

Mas como identificar esses pontos na prática?
Utilizamos técnicas de visão computacional para detectar keypoints (pontos-chave) e features na imagem. Esses pontos são regiões visualmente distintas, como:
- cantos
- bordas
- áreas com forte variação de intensidade

Esses elementos são mais fáceis de localizar e rastrear entre imagens, sendo fundamentais para reconstruir a geometria da cena.
Algumas técnicas já vimos para extrair e descrever os pontos.

#### Fonte: 
Link: https://www.youtube.com/watch?v=ViCqs7J2yi0&list=PLgnQpQtFTOGRYjqjdZxTEQPZuFHQa7O7Y&index=2