# F1: DRIVE TO SURVIVE - Todo en un solo archivo con variables originales y comentarios en español
import pygame
import sys
import time
import random

pygame.init()
pygame.mixer.init()

# Dimensiones de la pantalla
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("F1: DRIVE TO SURVIVE")

# Carga de recursos
fondo_menu = pygame.image.load("Fondo.png")
fondo_instrucciones = pygame.image.load("Fondo Instrucciones.jpg")
ferrari = pygame.transform.scale(pygame.image.load("Ferrari.png"), (56, 155))
ferrari_ancho = 56
borde1 = pygame.transform.scale(pygame.image.load("Borde Izquierdo.png"), (175, 600))
borde2 = pygame.transform.scale(pygame.image.load("Borde Derecho.png"), (175, 600))
pista = pygame.transform.scale(pygame.image.load("Pista.png"), (12, 35))
humo_original = pygame.transform.scale(pygame.image.load("Humo explosion.png"), (150, 150))
obstaculo_imagenes = [
    pygame.transform.scale(pygame.image.load(img), (56, 155)) for img in [
        "Red Bull.png", "Mercedes.png", "McLaren.png", "Alpine.png",
        "Aston Martin.png", "Williams.png", "Haas.png", "Racing Bulls.png", "Kick.png"
    ]
]
msjChocar = pygame.font.SysFont(None, 150).render("¡CHOCASTE!", True, (255, 255, 255))

# Música del menú principal
pygame.mixer.music.load("Cancion.mp3")
reloj = pygame.time.Clock()

# Función para reiniciar variables del juego
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

# Dibuja botón con texto centrado
def dibujar_boton(texto, x, y, ancho, alto, color):
    fuente = pygame.font.SysFont(None, 36)
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, color, rect)
    texto_render = fuente.render(texto, True, (255, 255, 255))
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)
    return rect

# Dibuja los elementos de fondo de la pista
def fondo(pista_posY):
    pantalla.fill((29, 29, 28))
    pantalla.blit(borde1, (0, 0))
    pantalla.blit(borde2, (625, 0))
    x_centro = (ancho - pista.get_width()) // 2
    for i in range(8):
        y = pista_posY + i * 85
        pantalla.blit(pista, (x_centro, y - 85))

# Panel de información durante el juego
def tabla_puntaje(pasado, puntaje, nivel, velocidad, velocidad_base):
    ancho_panel = 270
    alto_panel = 130
    x_panel = 10
    y_panel = 10
    panel = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)
    color_fondo = (20, 20, 20, 180)
    panel.fill(color_fondo)
    fuente_titulo = pygame.font.SysFont("Arial", 26, bold=True)
    fuente_valor = pygame.font.SysFont("Arial", 24)

    texto_pasados = fuente_titulo.render("Autos Pasados:", True, (255, 255, 255))
    valor_pasados = fuente_valor.render(str(pasado), True, (200, 200, 200))

    texto_puntaje = fuente_titulo.render("Puntaje:", True, (255, 255, 255))
    valor_puntaje = fuente_valor.render(str(puntaje), True, (200, 200, 200))

    texto_nivel = fuente_titulo.render("Nivel:", True, (255, 255, 255))
    valor_nivel = fuente_valor.render(str(nivel), True, (200, 200, 200))

    texto_velocidad = fuente_titulo.render("Velocidad:", True, (255, 255, 255))
    velocidad_mostrada = velocidad * 10
    if velocidad > velocidad_base:
        color_vel = (255, 0, 0)
    elif velocidad < velocidad_base:
        color_vel = (0, 255, 0)
    else:
        color_vel = (255, 255, 255)
    valor_velocidad = fuente_valor.render(str(velocidad_mostrada) + " KM/H", True, color_vel)

    separacion_vertical = 30
    margen_izquierdo = 15

    panel.blit(texto_pasados, (margen_izquierdo, 10))
    panel.blit(valor_pasados, (margen_izquierdo + 170, 12))

    panel.blit(texto_puntaje, (margen_izquierdo, 10 + separacion_vertical))
    panel.blit(valor_puntaje, (margen_izquierdo + 170, 12 + separacion_vertical))

    panel.blit(texto_nivel, (margen_izquierdo, 10 + separacion_vertical * 2))
    panel.blit(valor_nivel, (margen_izquierdo + 170, 12 + separacion_vertical * 2))

    panel.blit(texto_velocidad, (margen_izquierdo, 10 + separacion_vertical * 3))
    panel.blit(valor_velocidad, (margen_izquierdo + 170, 12 + separacion_vertical * 3))

    pantalla.blit(panel, (x_panel, y_panel))

# Lógica del juego principal
def juego():
    x, y, coordenadaX, obstaculoX, obstaculoY, obstaculo, auto_pasado, puntaje, nivel = reiniciar_juego()
    velocidad_base = 10
    velocidadObstaculo = velocidad_base
    pista_posY = 0
    acelerar = desacelerar = False
    contador_a = contador_d = 0
    pygame.mixer.music.play(-1)
    jugando = True

    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]: coordenadaX = -10
                if event.key in [pygame.K_RIGHT, pygame.K_d]: coordenadaX = 10
                if event.key in [pygame.K_UP, pygame.K_w]: acelerar = True
                if event.key in [pygame.K_DOWN, pygame.K_s]: desacelerar = True
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]: coordenadaX = 0
                if event.key in [pygame.K_UP, pygame.K_w]: acelerar, contador_a = False, 0
                if event.key in [pygame.K_DOWN, pygame.K_s]: desacelerar, contador_d = False, 0

        x += coordenadaX

        if acelerar:
            contador_a += 1
            if contador_a >= 4:
                velocidadObstaculo += 1
                contador_a = 0

        if desacelerar:
            contador_d += 1
            if contador_d >= 4:
                velocidadObstaculo = max(1, velocidadObstaculo - 1)
                contador_d = 0

        obstaculoY += velocidadObstaculo
        pista_posY = (pista_posY + velocidadObstaculo) % 85

        if obstaculoY > alto:
            obstaculoY = -155
            obstaculoX = random.randrange(175, 625)
            obstaculo = random.randint(0, 8)
            auto_pasado += 1
            puntaje += 15 if velocidadObstaculo > velocidad_base else 5 if velocidadObstaculo < velocidad_base else 10

        if x < 175:
            mostrar_mensaje_choque(x, y, obstaculoX, 'pared_izq')
            jugando = False
            break
        if x > 625 - ferrari_ancho:
            mostrar_mensaje_choque(x, y, obstaculoX, 'pared_der')
            jugando = False
            break
        if y < obstaculoY + 155 and y + 155 > obstaculoY:
            if x + ferrari_ancho > obstaculoX and x < obstaculoX + 56:
                mostrar_mensaje_choque(x, y, obstaculoX, 'auto')
                jugando = False
                break

        if auto_pasado == 10 * (nivel + 1):
            nivel += 1
            velocidad_base += 3
            if velocidadObstaculo < velocidad_base:
                velocidadObstaculo = velocidad_base

        fondo(pista_posY)
        pantalla.blit(ferrari, (x, y))
        pantalla.blit(obstaculo_imagenes[obstaculo], (obstaculoX, obstaculoY))
        tabla_puntaje(auto_pasado, puntaje, nivel, velocidadObstaculo, velocidad_base)
        pygame.display.update()
        reloj.tick(60)

juego()
pygame.quit()