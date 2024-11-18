import pygame

pygame.init()


ANCHO_PANTALLA = 600
ALTO_PANTALLA = 400

COLOR_NEGRO = (0, 0, 0)
COLOR_BOTONES = (25, 72, 79)

rectangulo_iniciar = [250, 140, 100, 50]
rectangulo_puntos = [250, 200, 100, 50]
rectangulo_salir =  [250, 260, 100, 50]


#Tamaño de pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
#Titulo del juego
pygame.display.set_caption("Batalla Naval")




#carga de imagenes
imagen_oceano = pygame.image.load("C1_2024.py/2do_parcial_pygame.py/imagen/oceano.jpg")
imagen_menu = pygame.image.load("C1_2024.py/2do_parcial_pygame.py/imagen/imagen_menu.jpg")
imagen_icono = pygame.image.load("C1_2024.py/2do_parcial_pygame.py/imagen/imagen_icono.jpg")

#Icono del juego
pygame.display.set_icon(imagen_icono)

#Sonidos:
# Fondo del menu:
pygame.mixer.music.load("C1_2024.py/2do_parcial_pygame.py/sonidos/sonido_menuu.wav")
pygame.mixer.music.set_volume(0.5) # 0 - 1 -> 0.2 es el 20% del volumen
pygame.mixer.music.play()



corriendo = True




while corriendo == True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
   
  
    pantalla.fill(COLOR_NEGRO)
   
    
    pantalla.blit(imagen_menu, (0, 0))
    
    
    pygame.draw.rect(pantalla, COLOR_BOTONES, rectangulo_iniciar, width=5, border_radius=5)
    pygame.draw.rect(pantalla, COLOR_BOTONES, rectangulo_puntos, width=5, border_radius=5)
    pygame.draw.rect(pantalla, COLOR_BOTONES, rectangulo_salir, width=5, border_radius=5)


    pygame.display.flip()