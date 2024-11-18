import pygame
import random

# Definiciones de las naves (en tamaño de casillas)
naves = {
    'submarino': 1,   # 4 submarinos de 1 casillero
    'destructor': 2,   # 3 destructores de 2 casilleros
    'crucero': 3,      # 2 cruceros de 3 casilleros
    'acorazado': 4     # 1 acorazado de 4 casilleros
}

# Inicializar Pygame
pygame.init()

# Tamaño de la ventana y colores
ANCHO = 500
ALTO = 500
TAMANIO_CELDA = 50  # tamaño de cada casilla
TAMANIO_MATRIZ = 10  # tamaño de la matriz (10x10)

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Crear la pantalla
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Batalla Naval')

# Crear la matriz de juego (10x10)
matriz = [['agua' for _ in range(TAMANIO_MATRIZ)] for _ in range(TAMANIO_MATRIZ)]

# Función para dibujar el tablero
def dibujar_tablero():
    screen.fill(BLANCO)
    for i in range(TAMANIO_MATRIZ):
        for j in range(TAMANIO_MATRIZ):
            rect = pygame.Rect(j * TAMANIO_CELDA, i * TAMANIO_CELDA, TAMANIO_CELDA, TAMANIO_CELDA)
            if matriz[i][j] == 'agua':
                pygame.draw.rect(screen, AZUL, rect)
            elif matriz[i][j] == 'barco':
                pygame.draw.rect(screen, VERDE, rect)
            elif matriz[i][j] == 'golpe':
                pygame.draw.rect(screen, ROJO, rect)
            pygame.draw.rect(screen, NEGRO, rect, 2)  # borde de la celda
    pygame.display.update()

# Función para generar una nave aleatoria
# Función para colocar una nave de tamaño 'tamano' en la matriz
def colocar_nave(tamano):
    colocado = False
    while not colocado:
        # Elegir una orientación aleatoria (horizontal o vertical)
        orientacion = random.choice(['horizontal', 'vertical'])
        
        if orientacion == 'horizontal':
            fila = random.randint(0, TAMANIO_MATRIZ - 1)
            columna = random.randint(0, TAMANIO_MATRIZ - tamano)
            
            # Comprobar si las casillas están libres (sin usar 'all()')
            espacio_libre = True
            for i in range(tamano):
                if matriz[fila][columna + i] != 'agua':  # Si hay alguna casilla ocupada
                    espacio_libre = False
                    break  # Romper el bucle si encontramos una casilla ocupada
            
            if espacio_libre:
                # Colocar la nave
                for i in range(tamano):
                    matriz[fila][columna + i] = 'barco'
                colocado = True  # Si todo está libre, se coloca la nave

        else:  # Si es vertical
            fila = random.randint(0, TAMANIO_MATRIZ - tamano)
            columna = random.randint(0, TAMANIO_MATRIZ - 1)
            
            # Comprobar si las casillas están libres (sin usar 'all()')
            espacio_libre = True
            for i in range(tamano):
                if matriz[fila + i][columna] != 'agua':  # Si hay alguna casilla ocupada
                    espacio_libre = False
                    break  # Romper el bucle si encontramos una casilla ocupada
            
            if espacio_libre:
                # Colocar la nave
                for i in range(tamano):
                    matriz[fila + i][columna] = 'barco'
                colocado = True  # Si todo está libre, se coloca la nave


# Función para colocar todas las naves
def colocar_todas_las_naves():
    # Colocar submarinos (4 barcos de 1 casillero)
    for _ in range(4):
        colocar_nave(1)
    # Colocar destructores (3 barcos de 2 casilleros)
    for _ in range(3):
        colocar_nave(2)
    # Colocar cruceros (2 barcos de 3 casilleros)
    for _ in range(2):
        colocar_nave(3)
    # Colocar acorazado (1 barco de 4 casilleros)
    colocar_nave(4)

# Función principal del juego
def juego():
    colocar_todas_las_naves()  # Colocamos las naves al inicio

    # Bucle principal del juego
    ejecutando = True
    while ejecutando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtener las coordenadas del click
                x, y = event.pos
                fila = y // TAMANIO_CELDA
                columna = x // TAMANIO_CELDA
                if matriz[fila][columna] == 'barco':
                    matriz[fila][columna] = 'golpe'
                elif matriz[fila][columna] == 'agua':
                    matriz[fila][columna] = 'agua'

        # Dibujar el tablero
        dibujar_tablero()

    pygame.quit()

if __name__ == "__main__":
    juego()
