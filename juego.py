# Importación de librerías e inicialización
import pygame  # Biblioteca para crear videojuegos
pygame.init()  # Inicializa Pygame

import time  # Para manejar pausas en el juego
import random  # Para generar números aleatorios

# Configuración de la ventana del videojuego
alto = 600
ancho = 800
pantalla = pygame.display.set_mode((ancho, alto))

# Encabezado de la ventana
pygame.display.set_icon(pygame.image.load("Logo.png"))  # Ícono de la ventana
pygame.display.set_caption("F1: DRIVE TO SURVIVE")  # Título de la ventana

# Cargar el auto y ajustar su tamaño
ferrari = pygame.image.load("Ferrari.png")
ferrari = pygame.transform.scale(ferrari, (56, 155))
ferrari_ancho = 56  # Ancho del auto

# Cargar y escalar imágenes del fondo
borde1 = pygame.image.load("Borde Izquierdo.png")
borde1 = pygame.transform.scale(borde1, (175, 600))  # Borde izquierdo

borde2 = pygame.image.load("Borde Derecho.png")
borde2 = pygame.transform.scale(borde2, (175, 600))  # Borde derecho

pista = pygame.image.load("Pista.png")
pista = pygame.transform.scale(pista, (450, 600))  # Pista 

# Preparar mensaje de choque
fuente = pygame.font.SysFont(None, 150)  # Fuente para el texto
msjChocar = fuente.render("¡CHOCASTE!", True, (255, 255, 255))  # Texto blanco

# Reloj para controlar los FPS (fotogramas por segundo)
reloj = pygame.time.Clock()

# Cargar imágenes de obstáculos una sola vez al inicio en un vector.
obstaculo_imagenes = [
    pygame.transform.scale(pygame.image.load("Red Bull.png"), (56, 155)),
    pygame.transform.scale(pygame.image.load("Mercedes.png"), (56, 155)),
    pygame.transform.scale(pygame.image.load("McLaren.png"), (56, 155)),
    pygame.transform.scale(pygame.image.load("Alpine.png"), (56, 155)),
    pygame.transform.scale(pygame.image.load("Aston Martin.png"), (56, 155)),
    pygame.transform.scale(pygame.image.load("Williams.png"), (56, 155)),
    pygame.transform.scale(pygame.image.load("Haas.png"), (56, 155)),
    pygame.transform.scale(pygame.image.load("Racing Bulls.png"), (56, 155)),
    pygame.transform.scale(pygame.image.load("Kick.png"), (56, 155)),
]

# Dibuja el auto en la pantalla en las coordenadas x, y
def auto(x, y):
    pantalla.blit(ferrari, (x, y))



# Dibuja el fondo: pista y bordes
def fondo():
    pantalla.blit(borde1, (0, 0))        # Borde izquierdo
    pantalla.blit(pista, (175, 0))       # Pista centrada
    pantalla.blit(borde2, (625, 0))      # Borde derecho

# Dibuja el obstáculo ya cargado en el vector obstaculo_imagenes
def obstaculos(obstaculoX, obstaculoY, obstaculo):
    pantalla.blit(obstaculo_imagenes[obstaculo], (obstaculoX, obstaculoY))

# Muestra el mensaje de choque con fondo rojo
def mostrar_mensaje_choque():
    texto_x = ancho // 2 - msjChocar.get_width() // 2
    texto_y = 285

    # Dibuja bandera roja (con padding) detrás del texto
    pygame.draw.rect(
        pantalla,
        (139, 0, 0),
        (texto_x - 10, texto_y - 10, msjChocar.get_width() + 20, msjChocar.get_height() + 20)
    )

    pantalla.blit(msjChocar, (texto_x, texto_y))
    pygame.display.update()
    time.sleep(3)  # Pausa 3 segundos antes de continuar

# Reinicia las posiciones del auto y el obstáculo
def reiniciar_juego():
    x = 400
    y = 450
    coordenadaX = 0
    obstaculoY = -155
    obstaculoX = random.randrange(175, 625)
    obstaculo = random.randint(0, 8)
    auto_pasado = 0
    puntaje = 0
    nivel = 0
    return x, y, coordenadaX, obstaculoX, obstaculoY, obstaculo, auto_pasado, puntaje, nivel
    

# muestra de puntaje 
def tabla_puntaje(pasado, puntaje):
    fuente = pygame.font.SysFont(None,35)
    pasado = fuente.render("Passed: " + str(pasado), True, (255,255,255))
    puntaje = fuente.render("Puntaje: " + str(puntaje), True, (24,94,255))
    pantalla.blit(pasado, (0,50))
    pantalla.blit(puntaje, (0,100))


# Bucle principal del juego
def juego():
    x, y, coordenadaX, obstaculoX, obstaculoY, obstaculo, auto_pasado, puntaje, nivel = reiniciar_juego()
    velocidadObstaculo = 10
    jugando = True


    # Obstáculo
    velocidadObstaculo = 10  # Velocidad del obstáculo
    obstaculo = random.randint(0, 8)  # Tipo de obstáculo
    obstaculoX = random.randrange(175, 625)  # Posición X aleatoria
    obstaculoY = -155  # Empieza fuera de pantalla
    obstaculo_ancho = 56
    obstaculo_alto = 155
    auto_pasado = 0
    puntaje = 0
    nivel = 0 


    jugando = True

    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Si se cierra la ventana
                jugando = False

            if event.type == pygame.KEYDOWN: # Detecta teclas presionadas
                if event.key == pygame.K_LEFT:
                    coordenadaX = -5
                if event.key == pygame.K_RIGHT:
                    coordenadaX = 5
                if event.key == pygame.K_s:
                    velocidadObstaculo += 2  
                if event.key == pygame.K_b:
                    velocidadObstaculo -= 2 

            if event.type == pygame.KEYUP: # Detecta teclas soltadas
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    coordenadaX = 0

        x += coordenadaX # Mueve el auto horizontalmente

        fondo()  # Dibuja bordes y pista

        obstaculoY += velocidadObstaculo  # Mueve el obstáculo hacia abajo

        obstaculos(obstaculoX, obstaculoY, obstaculo)  # Dibuja el obstáculo

        # Cuando el obstáculo sale de la pantalla, reinicia su posición
        if obstaculoY > alto:
            obstaculoY = -155
            obstaculoX = random.randrange(175, 625)
            obstaculo = random.randint(0, 8)
            auto_pasado += 1
            puntaje = auto_pasado * 10
            if int(auto_pasado) % 10 == 0:
                nivel += 1 
                velocidadObstaculo += 2
                fuente = pygame.font.SysFont(None, 50)
                nivel_texto = fuente.render("Nivel: " + str(nivel), 1, (85, 255, 43))
                pantalla.blit(nivel_texto, (100, 200))
                pygame.display.update()
                time.sleep(3)
                

        auto(x, y)  # Dibuja el auto

        # Poniendo el puntaje en la pantalla 
        tabla_puntaje(auto_pasado, puntaje)

        # Detecta colisiones entre auto y obstáculo
        rect_auto = pygame.Rect(x, y, ferrari_ancho, 155) #Posicion y tamaño del auto
        rect_obstaculo = pygame.Rect(obstaculoX, obstaculoY, obstaculo_ancho, obstaculo_alto) #Posicion y tamaño del obstáculo

        if rect_auto.colliderect(rect_obstaculo): # Si hay colisión
            mostrar_mensaje_choque()
            x, y, coordenadaX, obstaculoX, obstaculoY, obstaculo, auto_pasado, puntaje, nivel = reiniciar_juego()
            velocidadObstaculo = 10 
        # Si el auto se sale de los límites de la pista
        if x > 660 - ferrari_ancho or x < 150:
            mostrar_mensaje_choque()
            x, y, coordenadaX, obstaculoX, obstaculoY, obstaculo, auto_pasado, puntaje, nivel = reiniciar_juego()
            velocidadObstaculo = 10 
        pygame.display.update()
        reloj.tick(60)  # 60 FPS para mejor rendimiento

    pygame.quit()

# Inicia el juego
juego()
