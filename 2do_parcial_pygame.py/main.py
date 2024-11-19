import pygame
import random
import sys


pygame.init()

#tamaño de pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

#Nombre del juego
pygame.display.set_caption("Batalla Naval")


rectangulo_iniciar = [250, 140, 100, 50]
rectangulo_puntos = [250, 200, 100, 50]
rectangulo_salir =  [250, 260, 100, 50]


#carga de imagenes
imagen_oceano = pygame.image.load("2do_parcial_pygame.py/imagenes/oceano.jpg")
imagen_menu = pygame.image.load("2do_parcial_pygame.py/imagenes/imagen_menu.jpg")
imagen_icono = pygame.image.load("2do_parcial_pygame.py/imagenes/imagen_icono.jpg")

imagen_menu_agrandada = pygame.transform.scale(imagen_menu, (800, 600))
imagen_oceano_agrandada = pygame.transform.scale(imagen_oceano, (800, 600))

#Icono del juego
pygame.display.set_icon(imagen_icono)

#Sonidos:
# Fondo del menu:
pygame.mixer.music.load("2do_parcial_pygame.py/sonidos/sonido_menuu.wav")
pygame.mixer.music.set_volume(0.5) # 0 - 1 -> 0.2 es el 20% del volumen
pygame.mixer.music.play(-1, 0.0)

sonido_botones = pygame.mixer.Sound("2do_parcial_pygame.py/sonidos/sonido_boton.wav")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (169, 169, 169)
COLOR_BOTONES = (25, 72, 79)

# Tamaño de la grilla
TAMANIO_CASILLA = 45
FILAS = 10
COLUMNAS = 10

# Tipos de barcos y tamaños
barcos = {
    "submarino": 1,  # 4 barcos de 1 casillero
    "destructor": 2,  # 3 barcos de 2 casilleros
    "crucero": 3,     # 2 barcos de 3 casilleros
    "acorazado": 4    # 1 barco de 4 casilleros
}

#lista de puntos
lista_puntajes = []

def dibujar_grilla():
    x_inicial = (ANCHO - COLUMNAS * TAMANIO_CASILLA) // 2
    y_inicial = (ALTO - FILAS * TAMANIO_CASILLA) // 2

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x = x_inicial + col * TAMANIO_CASILLA
            y = y_inicial + fila * TAMANIO_CASILLA
            pygame.draw.rect(pantalla, NEGRO, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA), 1)


# Función para colocar un barco aleatoriamente en la grilla sin usar all()
def colocar_barco(barco, longitud, matriz):
    colocado = False
    while not colocado:
        # Generar dirección aleatoria (horizontal o vertical)
        direccion = random.choice(["horizontal", "vertical"])
        # Seleccionar una posición inicial aleatoria
        fila = random.randint(0, FILAS - 1)
        col = random.randint(0, COLUMNAS - 1)

        if direccion == "horizontal":
            # Verificar que el barco no salga de los límites y que las celdas estén vacías
            if col + longitud <= COLUMNAS:
                ocupado = False
                for i in range(longitud):
                    if matriz[fila][col + i] != 0:  # Si alguna celda está ocupada, no se coloca el barco
                        ocupado = True
                        break
                if not ocupado:
                    for i in range(longitud):
                        matriz[fila][col + i] = 1  # Marcar las celdas como ocupadas
                    colocado = True
        elif direccion == "vertical":
            # Verificar que el barco no salga de los límites y que las celdas estén vacías
            if fila + longitud <= FILAS:
                ocupado = False
                for i in range(longitud):
                    if matriz[fila + i][col] != 0:  # Si alguna celda está ocupada, no se coloca el barco
                        ocupado = True
                        break
                if not ocupado:
                    for i in range(longitud):
                        matriz[fila + i][col] = 1  # Marcar las celdas como ocupadas
                    colocado = True

    # Retornar las coordenadas de las celdas ocupadas por el barco
    if direccion == "horizontal":
        return [(fila, col + i) for i in range(longitud)]
    else:  # direccion == "vertical"
        return [(fila + i, col) for i in range(longitud)]


def colocar_todos_los_barcos():
    matriz = [[0] * COLUMNAS for _ in range(FILAS)]  # Matriz vacía de la grilla
    barcos_colocados = {}

    # Definir explícitamente la cantidad de barcos a colocar
    cantidad_barcos = {
        "submarino": 4,    # Colocamos 4 submarinos
        "destructor": 3,   # Colocamos 3 destructores
        "crucero": 2,      # Colocamos 2 cruceros
        "acorazado": 1     # Colocamos 1 acorazado
    }
    
    # Colocar los barcos en la grilla
    for barco, cantidad in cantidad_barcos.items():
        for _ in range(cantidad):  # Colocamos el número de barcos según lo indicado
            longitud = barcos[barco]  # Obtener la longitud del barco
            celdas = colocar_barco(barco, longitud, matriz)  # Colocar un barco
            if barco in barcos_colocados:
                barcos_colocados[barco].extend(celdas)  # Añadir las celdas ocupadas por el barco
            else:
                barcos_colocados[barco] = celdas  # Si el barco no está en el diccionario, añadirlo

    return barcos_colocados

# Función para verificar si un disparo es un impacto
def disparar(filas, columnas, barcos_colocados, puntaje):
    for barco, celdas in barcos_colocados.items():
        if (filas, columnas) in celdas:
            puntaje += 5  # Impacto
            celdas.remove((filas, columnas))
            if len(celdas) == 0:
                puntaje += 10 * barcos[barco]  # Hundir el barco
            return puntaje, True
    puntaje -= 1  # Agua
    return puntaje, False

# Función para dibujar la interfaz del juego
def pantalla_juego(puntaje):
    pantalla.fill(BLANCO)
    pantalla.blit(imagen_oceano_agrandada, (0, 0))
    dibujar_grilla()

    # Mostrar puntaje
    fuente = pygame.font.Font(None, 36)
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, NEGRO)
    pantalla.blit(texto_puntaje, (600, 50))
    texto_salir = fuente.render(f"Salir", True, ROJO)
    pantalla.blit(texto_salir, [600, 550])
    pygame.display.flip()

# Menú Principal con botones
def menu_principal():
    font = pygame.font.Font(None, 50)
    texto_jugar = font.render("Jugar", True, NEGRO)
    texto_puntajes = font.render("Ver Puntajes", True, NEGRO)
    texto_salir = font.render("Salir", True, NEGRO)

    # Coordenadas de los botones
    jugar_rect = pygame.Rect(300, 150, 250, 50)
    puntajes_rect = pygame.Rect(300, 250, 250, 50)
    salir_rect = pygame.Rect(300, 350, 250, 50)





    while True:
        pantalla.fill(BLANCO)
        pantalla.blit(imagen_menu_agrandada, (0, 0))
        
        
        pygame.draw.rect(pantalla, COLOR_BOTONES, jugar_rect, width=0, border_radius=5)
        pygame.draw.rect(pantalla, COLOR_BOTONES, puntajes_rect, width=0, border_radius=5)
        pygame.draw.rect(pantalla, COLOR_BOTONES, salir_rect, width=0, border_radius=5)

        pantalla.blit(texto_jugar, (jugar_rect.x + 70, jugar_rect.y + 10))
        pantalla.blit(texto_puntajes, (puntajes_rect.x + 20, puntajes_rect.y + 10))
        pantalla.blit(texto_salir, (salir_rect.x + 80, salir_rect.y + 10))

        pygame.display.flip()

        # Verificar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                sonido_botones.play()
                if jugar_rect.collidepoint(evento.pos):
                    return "jugar"
                elif puntajes_rect.collidepoint(evento.pos):
                    return "puntajes"
                elif salir_rect.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

# Función principal
def main():
    puntaje = 0  # Definimos el puntaje aquí, fuera de la variable global
    while True:
        seleccion = menu_principal()
        if seleccion == "jugar":
            barcos_colocados = colocar_todos_los_barcos()
            juego_en_curso = True
            while juego_en_curso:
                pantalla_juego(puntaje)
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        fila = evento.pos[1] // TAMANIO_CASILLA
                        columna = evento.pos[0] // TAMANIO_CASILLA
                        puntaje, _ = disparar(fila, columna, barcos_colocados, puntaje)
        elif seleccion == "puntajes":
                pygame.display.flip()

if __name__ == "__main__":
    main()
