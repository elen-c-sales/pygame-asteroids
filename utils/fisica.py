"""
Utilitários para física e colisões
"""
import pygame


def checar_colisao_circular(obj1_pos, obj1_raio, obj2_pos, obj2_raio):
    """
    Verifica colisão entre dois objetos circulares
    
    Args:
        obj1_pos: pygame.math.Vector2 - posição do objeto 1
        obj1_raio: float - raio do objeto 1
        obj2_pos: pygame.math.Vector2 - posição do objeto 2
        obj2_raio: float - raio do objeto 2
    
    Returns:
        bool: True se houve colisão, False caso contrário
    """
    distancia = obj1_pos.distance_to(obj2_pos)
    return distancia < (obj1_raio + obj2_raio)
