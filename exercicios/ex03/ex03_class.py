import cv2 as cv 

class BFMatchingFeatures: 

    # Construtor
    def __init__(self, tipo_feature: str):
        self.tipo_feature = tipo_feature.upper() 
        self.dist = self.escolher_dist()
        self.bf = cv.BFMatcher(self.dist, crossCheck = False) # Se usarmos o knnMatch, crossCheck precisa ser false

    # Distância
    def escolher_dist(self):
        """
        Selecionar o tipo de cálculo de distância do matching
        """

        if self.tipo_feature in ('ORB', 'BRISK', 'AKAZE'):
            return cv.NORM_HAMMING
        
        elif self.tipo_feature == 'SIFT':
            return cv.NORM_L2
        
        else:
            raise ValueError('Tipo de método de extração não encontrado')
    
    def matching(self, des1, des2):
        """
        Realiza o matching
        """

        # Verificando existência de valores
        if des1 is None or des2 is None:
            return []
        
        # Descritor match
        matches = self.bf.knnMatch(des1, des2, k = 2)

        # Aplica Ratio Test (remove matches ruins)
        melhores_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                melhores_matches.append([m])

        # # Ordena por distância
        # matches = sorted(matches, key=lambda x: x.distance)

        return melhores_matches
    