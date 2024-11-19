import pygame
import random
import sys


pygame.init()

ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

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


BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
GRIS = (169, 169, 169)
COLOR_BOTONES = (25, 72, 79)


TAMANIO_CASILLA = 45
FILAS = 10
COLUMNAS = 10


barcos = {
    "submarino": 1,  
    "destructor": 2, 
    "crucero": 3,    
    "acorazado": 4   
}


lista_puntajes = []

def dibujar_grilla():
    x_inicial = (ANCHO - COLUMNAS * TAMANIO_CASILLA) // 2
    y_inicial = (ALTO - FILAS * TAMANIO_CASILLA) // 2

    for fila in range(FILAS):
        for col in range(COLUMNAS):
            x = x_inicial + col * TAMANIO_CASILLA
            y = y_inicial + fila * TAMANIO_CASILLA
            pygame.draw.rect(pantalla, NEGRO, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA), 1)



def colocar_barco(barco, longitud, matriz):
    colocado = False
    while not colocado:
    
        direccion = random.choice(["horizontal", "vertical"])
        fila = random.randint(0, FILAS - 1)
        col = random.randint(0, COLUMNAS - 1)

        if direccion == "horizontal":
            
            if col + longitud <= COLUMNAS: # <- verifica que el barco no salga de los límites y que las celdas estén vacías
                ocupado = False
                for i in range(longitud):
                    if matriz[fila][col + i] != 0:
                        ocupado = True
                        break
                if not ocupado:
                    for i in range(longitud):
                        matriz[fila][col + i] = 1  # <- indica la celda como ocupada
                    colocado = True
        elif direccion == "vertical":
            if fila + longitud <= FILAS:
                ocupado = False
                for i in range(longitud):
                    if matriz[fila + i][col] != 0:  
                        ocupado = True
                        break
                if not ocupado:
                    for i in range(longitud):
                        matriz[fila + i][col] = 1 
                    colocado = True

    if direccion == "horizontal":
        return [(fila, col + i) for i in range(longitud)]
    else: 
        return [(fila + i, col) for i in range(longitud)]


def colocar_todos_los_barcos():
    matriz = [[0] * COLUMNAS for _ in range(FILAS)] 
    barcos_colocados = {}

  
    cantidad_barcos = {
        "submarino": 4,   
        "destructor": 3, 
        "crucero": 2,    
        "acorazado": 1    
    }
    
   
    for barco, cantidad in cantidad_barcos.items():
        for _ in range(cantidad):  
            longitud = barcos[barco] 
            celdas = colocar_barco(barco, longitud, matriz) 
            if barco in barcos_colocados:
                barcos_colocados[barco].extend(celdas) 
            else:
                barcos_colocados[barco] = celdas  

    return barcos_colocados


def disparar(filas, columnas, barcos_colocados, puntaje):
    for barco, celdas in barcos_colocados.items():
        if (filas, columnas) in celdas:
            puntaje += 5  
            celdas.remove((filas, columnas))
            if len(celdas) == 0:
                puntaje += 10 * barcos[barco]  
            return puntaje, True
    puntaje -= 1  
    return puntaje, False


def pantalla_juego(puntaje):
    pantalla.fill(BLANCO)
    pantalla.blit(imagen_oceano_agrandada, (0, 0))
    dibujar_grilla()

    # puntaje y texto "salir"
    fuente = pygame.font.Font(None, 36)
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, NEGRO)
    pantalla.blit(texto_puntaje, (600, 50))
    texto_salir = fuente.render(f"Salir", True, ROJO)
    pantalla.blit(texto_salir, [600, 550])
    pygame.display.flip()


def menu_principal():
    font = pygame.font.Font(None, 50)
    texto_jugar = font.render("Jugar", True, NEGRO)
    texto_puntajes = font.render("Ver Puntajes", True, NEGRO)
    texto_salir = font.render("Salir", True, NEGRO)


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


def main():
    puntaje = 0  
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
