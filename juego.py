import pygame
import time
import random

pygame.init()
pygame.mixer.init()  # Inicializa mixer para sonido

alto = 600
ancho = 800
pantalla = pygame.display.set_mode((ancho, alto))

pygame.display.set_icon(pygame.image.load("Logo.png"))
pygame.display.set_caption("F1: DRIVE TO SURVIVE")

# Carga y escala del auto principal
ferrari = pygame.image.load("Ferrari.png")
ferrari = pygame.transform.scale(ferrari, (56, 155))
ferrari_ancho = 56

# Carga y escala de los bordes de la pista
borde1 = pygame.image.load("Borde Izquierdo.png")
borde1 = pygame.transform.scale(borde1, (175, 600))

borde2 = pygame.image.load("Borde Derecho.png")
borde2 = pygame.transform.scale(borde2, (175, 600))

# Carga y escala de la línea central de la pista
pista = pygame.image.load("Pista.png")
pista = pygame.transform.scale(pista, (12, 35))

# Fuente para mostrar mensaje de choque
fuente = pygame.font.SysFont(None, 150)
msjChocar = fuente.render("¡CHOCASTE!", True, (255, 255, 255))

# Carga y escala del humo de la explosión (150x150)
humo_original = pygame.image.load("Humo explosion.png")
humo_original = pygame.transform.scale(humo_original, (150, 150))

reloj = pygame.time.Clock()

# Lista de imágenes para obstáculos (otros autos)
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

# Carga la música de fondo
pygame.mixer.music.load("Cancion.mp3")

def auto(x, y):
    """Dibuja el auto principal en la pantalla en posición (x, y)"""
    pantalla.blit(ferrari, (x, y))

def fondo(pista_posY):
    """Dibuja el fondo de la pista, los bordes y las líneas centrales"""
    pantalla.fill((29, 29, 28))  # Fondo oscuro
    pantalla.blit(borde1, (0, 0))  # Borde izquierdo
    pantalla.blit(borde2, (625, 0))  # Borde derecho
    x_centro = (ancho - pista.get_width()) // 2  # Centro pista
    
    # Dibuja múltiples líneas para simular el movimiento
    for i in range(8):
        y = pista_posY + i * 85
        pantalla.blit(pista, (x_centro, y - 85))

def obstaculos(obstaculoX, obstaculoY, obstaculo):
    """Dibuja el obstáculo seleccionado en la posición dada"""
    pantalla.blit(obstaculo_imagenes[obstaculo], (obstaculoX, obstaculoY))

def mostrar_mensaje_choque(x_auto, y_auto, x_obstaculo, choque_tipo):
    """
    Muestra el mensaje de choque y dibuja el humo en la posición correcta
    choque_tipo puede ser:
        - 'auto': choque con otro auto
        - 'pared_izq': choque contra borde izquierdo
        - 'pared_der': choque contra borde derecho
        - 'frontal': choque frontal (por si se usa)
    """

    texto_x = ancho // 2 - msjChocar.get_width() // 2
    texto_y = 285
    
    # Dibuja un rectángulo rojo oscuro detrás del texto para destacar
    pygame.draw.rect(pantalla, (139, 0, 0), (texto_x - 10, texto_y - 10, msjChocar.get_width() + 20, msjChocar.get_height() + 20))
    
    # Determina la posición del humo según tipo de choque
    if choque_tipo == 'auto':
        # Si chocaste con otro auto:
        # Coloca la parte negra del humo sobre el lado del auto donde chocaste
        
        if x_auto < x_obstaculo:
            # Choque por la derecha (auto a la derecha)
            humo = humo_original
            humo_x = x_auto + ferrari_ancho - 50  # Ligeramente hacia la derecha del auto
        else:
            # Choque por la izquierda (auto a la izquierda)
            humo = pygame.transform.flip(humo_original, True, False)  # Voltea horizontalmente para simetría
            humo_x = x_auto - humo.get_width() + 50  # Ajusta para que quede en el lado izquierdo
        
        humo_y = y_auto + 30  # Altura del humo sobre el auto

    elif choque_tipo == 'pared_izq':
        # Choque con pared izquierda: humo aparece a la izquierda del auto
        humo = humo_original
        humo_x = x_auto - 20  # Un poco a la izquierda del auto
        humo_y = y_auto + 30

    elif choque_tipo == 'pared_der':
        # Choque con pared derecha: humo aparece a la derecha del auto, invertido
        humo = pygame.transform.flip(humo_original, True, False)
        humo_x = x_auto + ferrari_ancho - 130  # Ajuste para que quede a la derecha del auto
        humo_y = y_auto + 30

    else:  # Choque frontal u otro caso
        humo = humo_original
        humo_x = x_auto + (ferrari_ancho // 2) - (humo.get_width() // 2)  # Centrado horizontalmente
        humo_y = y_auto - 80  # Arriba del auto, simulando explosión frontal

    pantalla.blit(humo, (humo_x, humo_y))  # Dibuja el humo
    pantalla.blit(msjChocar, (texto_x, texto_y))  # Dibuja el texto de choque
    pygame.display.update()
    
    # Detiene la música al chocar
    pygame.mixer.music.stop()
    
    time.sleep(3)  # Pausa para que se vea el mensaje

def mostrar_nivel_superado(nivel):
    """Muestra mensaje cuando se supera un nivel con un fondo y bandera verde"""
    fuente_nivel = pygame.font.SysFont(None, 100)
    texto = fuente_nivel.render(f"Nivel {nivel} SUPERADO", True, (255, 255, 255))

    x_centro = ancho // 2 - texto.get_width() // 2
    y_centro = alto // 2 - texto.get_height() // 2

    # Dibuja un rectángulo verde oscuro como fondo con borde blanco
    rect_fondo = pygame.Rect(x_centro - 30, y_centro - 30, texto.get_width() + 60, texto.get_height() + 80)
    pygame.draw.rect(pantalla, (0, 100, 0), rect_fondo)
    pygame.draw.rect(pantalla, (255, 255, 255), rect_fondo, 5)

    # Dibuja una bandera verde junto al texto
    bandera_x = x_centro - 100
    bandera_y = y_centro
    palo_rect = pygame.Rect(bandera_x, bandera_y, 10, 80)
    bandera_rect = pygame.Rect(bandera_x + 10, bandera_y, 60, 40)
    pygame.draw.rect(pantalla, (139, 69, 19), palo_rect)  # Palo marrón
    pygame.draw.rect(pantalla, (0, 255, 0), bandera_rect)  # Bandera verde

    pantalla.blit(texto, (x_centro, y_centro))

    pygame.display.update()
    time.sleep(2)  # Pausa para que el jugador vea el mensaje

def reiniciar_juego():
    """Inicializa y devuelve las variables del juego para reiniciar"""
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

def tabla_puntaje(pasado, puntaje, nivel, velocidad):
    """
    Dibuja un panel oscuro semitransparente y redondeado
    con texto blanco para mostrar:
    - Autos pasados
    - Puntaje
    - Nivel
    - Velocidad
    """

    # Dimensiones y posición del panel
    ancho_panel = 250
    alto_panel = 130
    x_panel = 10
    y_panel = 10

    # Crear superficie con canal alfa para transparencia
    panel = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)
    
    # Fondo negro con 180 de alfa (transparente)
    color_fondo = (20, 20, 20, 180)
    
    # Dibujar fondo redondeado (aproximación con un rectángulo normal)
    panel.fill(color_fondo)

    # Fuente para los textos
    fuente_titulo = pygame.font.SysFont("Arial", 26, bold=True)
    fuente_valor = pygame.font.SysFont("Arial", 24)

    # Renderizar textos
    texto_pasados = fuente_titulo.render("Autos Pasados:", True, (255, 255, 255))
    valor_pasados = fuente_valor.render(str(pasado), True, (200, 200, 200))

    texto_puntaje = fuente_titulo.render("Puntaje:", True, (255, 255, 255))
    valor_puntaje = fuente_valor.render(str(puntaje), True, (200, 200, 200))

    texto_nivel = fuente_titulo.render("Nivel:", True, (255, 255, 255))
    valor_nivel = fuente_valor.render(str(nivel), True, (200, 200, 200))

    texto_velocidad = fuente_titulo.render("Velocidad:", True, (255, 255, 255))
    valor_velocidad = fuente_valor.render(str(velocidad) + "0 km/h", True, (200, 200, 200))

    # Espaciado vertical entre líneas
    separacion_vertical = 30
    margen_izquierdo = 15

    # Posicionar textos en el panel
    panel.blit(texto_pasados, (margen_izquierdo, 10))
    panel.blit(valor_pasados, (margen_izquierdo + 170, 12))

    panel.blit(texto_puntaje, (margen_izquierdo, 10 + separacion_vertical))
    panel.blit(valor_puntaje, (margen_izquierdo + 170, 12 + separacion_vertical))

    panel.blit(texto_nivel, (margen_izquierdo, 10 + separacion_vertical * 2))
    panel.blit(valor_nivel, (margen_izquierdo + 170, 12 + separacion_vertical * 2))

    panel.blit(texto_velocidad, (margen_izquierdo, 10 + separacion_vertical * 3))
    panel.blit(valor_velocidad, (margen_izquierdo + 170, 12 + separacion_vertical * 3))

    # Dibujar el panel transparente en la pantalla
    pantalla.blit(panel, (x_panel, y_panel))

def juego():
    # Inicializa variables del juego
    x, y, coordenadaX, obstaculoX, obstaculoY, obstaculo, auto_pasado, puntaje, nivel = reiniciar_juego()
    velocidadObstaculo = 10
    pista_posY = 0

    pygame.mixer.music.play(-1)

    jugando = True

    while jugando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Salir del juego y del programa
                pygame.quit()
                exit()  # termina el programa inmediatamente
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    coordenadaX = -10
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    coordenadaX = 10
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                    coordenadaX = 0

        x += coordenadaX

        if x < 175:
            mostrar_mensaje_choque(x, y, obstaculoX, 'pared_izq')
            jugando = False
            break
        if x > 625 - ferrari_ancho:
            mostrar_mensaje_choque(x, y, obstaculoX, 'pared_der')
            jugando = False
            break

        obstaculoY += velocidadObstaculo
        pista_posY += 10

        if pista_posY >= 85:
            pista_posY = 0

        if obstaculoY > alto:
            obstaculoY = -155
            obstaculoX = random.randrange(175, 625)
            obstaculo = random.randint(0, 8)
            auto_pasado += 1
            puntaje += 50

        if y < obstaculoY + 155 and y + 155 > obstaculoY:
            if x + ferrari_ancho > obstaculoX and x < obstaculoX + 56:
                mostrar_mensaje_choque(x, y, obstaculoX, 'auto')
                jugando = False
                break

        if auto_pasado == 5 * (nivel + 1):
            nivel += 1
            velocidadObstaculo += 3
            mostrar_nivel_superado(nivel)

        fondo(pista_posY)
        auto(x, y)
        obstaculos(obstaculoX, obstaculoY, obstaculo)
        tabla_puntaje(auto_pasado, puntaje, nivel, velocidadObstaculo)

        pygame.display.update()
        reloj.tick(60)

    pygame.mixer.music.stop()
    time.sleep(1)
    juego()


# Ejecutar juego
juego()
pygame.quit()
