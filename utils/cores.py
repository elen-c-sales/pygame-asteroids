"""
Utilitários para cores e interpolação
"""

# Cores do sistema de profundidade
COR_DISTANTE = (74, 95, 156)    # Azul escuro
COR_PROXIMA = (255, 255, 255)   # Branco
COR_FUNDO = (10, 10, 20)        # Azul escuro espacial


def interpolar_cor(profundidade):
    """
    Interpola cor baseada na profundidade (efeito 3D)
    
    Args:
        profundidade: float de 0.0 (distante) a 1.0 (próximo)
    
    Returns:
        tuple: (R, G, B) cor interpolada
    """
    r = int(COR_DISTANTE[0] + (COR_PROXIMA[0] - COR_DISTANTE[0]) * profundidade)
    g = int(COR_DISTANTE[1] + (COR_PROXIMA[1] - COR_DISTANTE[1]) * profundidade)
    b = int(COR_DISTANTE[2] + (COR_PROXIMA[2] - COR_DISTANTE[2]) * profundidade)
    
    return (r, g, b)
