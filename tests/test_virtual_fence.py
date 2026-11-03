import numpy as np
from src.virtual_fence import VirtualFence


def test_virtual_fence_inside():
    fence = VirtualFence(
        polygon=[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)],
        name="Teste Perimetro"
    )
    # Ponto no centro (50, 50) de uma imagem 100x100
    # bbox: (x1, y1, x2, y2) -> bottom_center = (50, 50)
    bbox = (40.0, 30.0, 60.0, 50.0)
    intruded, dist = fence.check_intrusion(bbox=bbox, keypoints=None, width=100, height=100)
    assert intruded is True


def test_virtual_fence_outside():
    # Poligono ocupando metade inferior
    fence = VirtualFence(
        polygon=[(0.0, 0.5), (1.0, 0.5), (1.0, 1.0), (0.0, 1.0)],
        name="Zona Sul"
    )
    # Caixa na parte superior (y2 = 20)
    bbox = (10.0, 5.0, 30.0, 20.0)
    intruded, dist = fence.check_intrusion(bbox=bbox, keypoints=None, width=100, height=100)
    assert intruded is False
