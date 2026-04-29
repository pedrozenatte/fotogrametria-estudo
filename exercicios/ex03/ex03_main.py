# Importando classes
from ex01.ex01 import ExtratorFeature
from ex03.ex03_class import BFMatchingFeatures

# Bibliotecas
import cv2 as cv

# Constante
TIPO_FEATURE = 'ORB'

imagem1 = cv.imread('ex03/cena1.jpeg', cv.IMREAD_GRAYSCALE)
imagem2 = cv.imread('ex03/cena2.jpeg', cv.IMREAD_GRAYSCALE)

# Extraindo características
extrator = ExtratorFeature(tipo_feature = TIPO_FEATURE)

kp1, des1 = extrator.extrair_features(imagem1)
kp2, des2 = extrator.extrair_features(imagem2)

# Realizando o matching
mt = BFMatchingFeatures(TIPO_FEATURE)
matches = mt.matching(des1 = des1, des2 = des2)

imagem_matches = cv.drawMatchesKnn(
    imagem1,
    kp1,
    imagem2,
    kp2,
    matches[:50],
    None,
    flags = cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
)

cv.imshow("Matches", imagem_matches)
cv.waitKey(0)
cv.destroyAllWindows()