import pygame
import sys
import time
import random

# Inicialización de Pygame y audio
pygame.init()
pygame.mixer.init()

# Dimensiones de la ventana
ancho, alto = 800, 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("F1: DRIVE TO SURVIVE")
reloj = pygame.time.Clock()

# Carga de recursos
fondo_menu = pygame.transform.scale(pygame.image.load("Fondo.png"), (ancho, alto))
fondo_instrucciones = pygame.image.load("Fondo Instrucciones.jpg")
ferrari = pygame.transform.scale(pygame.image.load("Ferrari.png"), (56, 155))
ferrari_ancho = 56
borde1 = pygame.transform.scale(pygame.image.load("Borde Izquierdo.png"), (175, 600))
borde2 = pygame.transform.scale(pygame.image.load("Borde Derecho.png"), (175, 600))
pista = pygame.transform.scale(pygame.image.load("Pista.png"), (12, 35))
humo_original = pygame.transform.scale(pygame.image.load("Humo explosion.png"), (150, 150))
obstaculo_imagenes = [pygame.transform.scale(pygame.image.load(img), (56, 155)) for img in [
    "Red Bull.png", "Mercedes.png", "McLaren.png", "Alpine.png",
    "Aston Martin.png", "Williams.png", "Haas.png", "Racing Bulls.png", "Kick.png"
]]

# Carga de sonidos
boton_sound = pygame.mixer.Sound("boton.mp3")
explosion_sound = pygame.mixer.Sound("explosion.wav")

# Selección de fuente estilo F1 simulada con SysFont más estilizada
f1_font = pygame.font.SysFont("Arial Narrow", 72, bold=True)

# Mensaje de choque
msjChocar = pygame.font.SysFont(None, 150).render("¡CHOCASTE!", True, (255, 255, 255))

# Función para mostrar nivel alcanzado
def mostrar_mensaje_nivel(nivel):
    font = pygame.font.SysFont(None, 100)
    msg = font.render(f"¡Nivel {nivel}!", True, (255, 255, 0))
    pantalla.blit(msg, ((ancho - msg.get_width()) // 2, (alto - msg.get_height()) // 2))
    pygame.display.update()
    time.sleep(2)

# Reiniciar variables del juego a nivel 0
def reiniciar_juego():
    x, y, dx = 400, 450, 0
    obsY = -155
    obsX = random.randrange(175, 625)
    obs = random.randint(0, len(current_obstaculos) - 1)
    return x, y, dx, obsX, obsY, obs, 0, 0, 0

# Dibujar botón con animación hover/click
def dibujar_boton(texto, x, y, w, h, color_base):
    fuente = pygame.font.SysFont(None, 36)
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    color = list(color_base)
    if rect.collidepoint((mx, my)):
        color = [min(255, c + 40) for c in color]
        if click:
            color = [max(0, c - 80) for c in color]
    pygame.draw.rect(pantalla, color, rect, border_radius=5)
    txt = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(txt, txt.get_rect(center=rect.center))
    return rect

# Dibuja pista y bordes
def fondo(pY):
    pantalla.fill((29, 29, 28))
    pantalla.blit(borde1, (0, 0))
    pantalla.blit(borde2, (625, 0))
    cx = (ancho - pista.get_width()) // 2
    for i in range(8):
        pantalla.blit(pista, (cx, pY + i * 85 - 85))

# Panel de estadísticas y tabla de puntajes
def tabla_puntaje(pas, pts, lvl, vel, vel_base):
    panel = pygame.Surface((270, 130), pygame.SRCALPHA)
    panel.fill((20, 20, 20, 180))
    fT = pygame.font.SysFont("Arial", 26, bold=True)
    fV = pygame.font.SysFont("Arial", 24)
    datos = [("Autos Pasados: ", pas), ("Puntaje:", pts), ("Nivel:", lvl), ("Velocidad:", f"{vel*10} KM/H")]
    for i, (label, val) in enumerate(datos):
        tL = fT.render(label, True, (255, 255, 255))
        color = (255, 255, 255)
        if i == 3:
            if vel > vel_base:
                color = (255, 0, 0)
            elif vel < vel_base:
                color = (0, 255, 0)
        tV = fV.render(str(val), True, color)
        panel.blit(tL, (15, 10 + i * 30))
        panel.blit(tV, (185, 12 + i * 30))
    pantalla.blit(panel, (10, 10))

    # Tabla de puntajes (persistente durante la ejecución)
    if not hasattr(tabla_puntaje, "puntajes"):
        tabla_puntaje.puntajes = []

    def agregar_puntaje(nombre, puntaje):
        tabla_puntaje.puntajes.append((nombre, puntaje))
        tabla_puntaje.puntajes.sort(key=lambda x: x[1], reverse=True)

    tabla_puntaje.agregar_puntaje = agregar_puntaje

    def mostrar_tabla_puntajes():
        fuente = pygame.font.SysFont(None, 36)
        for i, (nombre, puntaje) in enumerate(tabla_puntaje.puntajes[:5]):
            texto = fuente.render(f"{i+1}. {nombre}: {puntaje}", True, (255, 255, 255))
            pantalla.blit(texto, (20, 140 + i * 40))

    mostrar_tabla_puntajes()

# Mostrar choque (pausar música y reproducir solo sonido de choque)
def mostrar_mensaje_choque(x, y, obsX):
    pygame.mixer.music.pause()
    pantalla.blit(humo_original, (x - humo_original.get_width()//2,
                                   y - humo_original.get_height()//2))
    pantalla.blit(msjChocar, ((ancho-msjChocar.get_width())//2,
                               (alto-msjChocar.get_height())//2))
    explosion_sound.play()
    pygame.display.update()
    time.sleep(2)
    pygame.mixer.music.unpause()

# Pantalla de instrucciones con overlay
def mostrar_instrucciones():
    fuente = pygame.font.SysFont(None, 32)
    lineas = [
        "INSTRUCCIONES:",
        "<- / -> o A/D: Mover auto",
        "Flecha Arriba / W: Acelerar",
        "Flecha Abajo / S: Desacelerar",
        "P: Pausar/Reanudar juego",
        "Evitar choques con bordes o autos",
        "Ganar puntos al pasar autos: ",
        "15 si vas rápido, ",
        "10 velocidad normal, ",
        "5 si vas lento",
        "Esc o VOLVER: Regresar al menú"
    ]
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    btn_volver = None
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
            if e.type == pygame.MOUSEBUTTONDOWN and btn_volver and btn_volver.collidepoint(e.pos):
                return
        pantalla.blit(fondo_instrucciones, (0, 0))
        pantalla.blit(overlay, (0, 0))
        for i, text in enumerate(lineas):
            txt_surf = fuente.render(text, True, (255, 255, 255))
            txt_rect = txt_surf.get_rect(center=(ancho//2, 100 + i*40))
            pantalla.blit(txt_surf, txt_rect)
        btn_volver = dibujar_boton("Volver", (ancho-120)//2, alto-80, 120, 50, (70, 130, 180))
        pygame.display.update()
        reloj.tick(60)

# Selector de auto antes de empezar la carrera
def seleccionar_auto():
    """
    Muestra en pantalla los 10 coches disponibles y devuelve el índice elegido.
    """
    nombres = ["Ferrari", "Red Bull", "Mercedes", "McLaren", "Alpine",
               "Aston Martin", "Williams", "Haas", "Racing Bulls", "Kick"]
    imagenes = [ferrari] + obstaculo_imagenes.copy()

    thumb_w, thumb_h = 112, 155
    padding_x, padding_y = 20, 40
    cols = 5
    start_x = (ancho - (cols * thumb_w + (cols-1)*padding_x)) // 2
    start_y = (alto - (2 * thumb_h + padding_y)) // 2

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                for idx in range(len(imagenes)):
                    col = idx % cols
                    row = idx // cols
                    x0 = start_x + col * (thumb_w + padding_x)
                    y0 = start_y + row * (thumb_h + padding_y)
                    if pygame.Rect(x0, y0, thumb_w, thumb_h).collidepoint(mx, my):
                        return idx

        pantalla.fill((29,29,28))
        for idx, img in enumerate(imagenes):
            thumb = pygame.transform.scale(img, (thumb_w, thumb_h))
            col = idx % cols
            row = idx // cols
            x0 = start_x + col * (thumb_w + padding_x)
            y0 = start_y + row * (thumb_h + padding_y)
            pantalla.blit(thumb, (x0, y0))
            txt = pygame.font.SysFont(None, 24).render(nombres[idx], True, (255,255,255))
            pantalla.blit(txt, (x0 + (thumb_w - txt.get_width())//2, y0 + thumb_h + 5))

        pygame.display.update()
        reloj.tick(30)

# Menú principal con título, botones y selección de auto
def menu_principal():
    pygame.mixer.music.load("Cancion.mp3")
    pygame.mixer.music.play(-1)
    bw, bh = 200, 50
    mg = (ancho - 3*bw)//4
    y0 = alto - 100
    xs = [mg, mg+bw+mg, mg+2*(bw+mg)]
    titulo_surface = f1_font.render("F1: DRIVE TO SURVIVE", True, (255, 255, 255))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pantalla.blit(fondo_menu, (0, 0))
        pantalla.blit(titulo_surface, ((ancho - titulo_surface.get_width())//2, 30))

        b1 = dibujar_boton("Jugar", xs[0], y0, bw, bh, (0, 200, 0))
        b2 = dibujar_boton("Instrucciones", xs[1], y0, bw, bh, (0, 0, 200))
        b3 = dibujar_boton("Salir", xs[2], y0, bw, bh, (200, 0, 0))

        if b1.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            boton_sound.play()
            idx = seleccionar_auto()
            todas = [ferrari] + obstaculo_imagenes.copy()
            auto_jugador = todas[idx]
            oponentes = todas[:idx] + todas[idx+1:]
            # Guardamos la lista de oponentes en global para reiniciar correctamente
            global current_obstaculos
            current_obstaculos = oponentes
            juego(auto_jugador, oponentes)
            pygame.mixer.music.load("Cancion.mp3")
            pygame.mixer.music.play(-1)

        if b2.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            boton_sound.play()
            mostrar_instrucciones()
        if b3.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            boton_sound.play()
            pygame.quit(); sys.exit()

        pygame.display.update()
        reloj.tick(60)

# Lógica del juego con pausa y reinicio, recibiendo coche jugador y lista de oponentes
def juego(auto_jugador, obstaculos):
    pygame.mixer.music.load("carrera.mp3")
    pygame.mixer.music.play(-1)

    # Referencia global para reiniciar
    global current_obstaculos
    current_obstaculos = obstaculos

    x, y, dx, obsX, obsY, obs, autos, pts, nivel = reiniciar_juego()
    vb, vo = 10, 10
    pistaY = 0
    acel = des = False
    ca = cd = 0
    paus = False
    font_pause = pygame.font.SysFont(None, 72)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    paus = not paus
                if not paus:
                    if e.key in [pygame.K_LEFT, pygame.K_a]:
                        dx = -10
                    if e.key in [pygame.K_RIGHT, pygame.K_d]:
                        dx = 10
                    if e.key == pygame.K_UP:
                        acel = True
                    if e.key == pygame.K_DOWN:
                        des = True
                if e.key == pygame.K_ESCAPE:
                    return
            if e.type == pygame.KEYUP and not paus:
                if e.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                    dx = 0
                if e.key == pygame.K_UP:
                    acel, ca = False, 0
                if e.key == pygame.K_DOWN:
                    des, cd = False, 0

        if paus:
            pantalla.blit(font_pause.render("PAUSA", True, (255, 255, 255)), ((ancho-150)//2, (alto-100)//2))
            pygame.display.update()
            reloj.tick(5)
            continue

        x += dx
        if acel:
            ca += 1
            if ca >= 4:
                vo += 1
                ca = 0
        if des:
            cd += 1
            if cd >= 4:
                vo = max(1, vo - 1)
                cd = 0

        obsY += vo
        pistaY = (pistaY + vo) % 85

        # Colisiones
        if x < 175 or x > 625 - ferrari_ancho or (
           y < obsY + 155 and y + 155 > obsY and x + ferrari_ancho > obsX and x < obsX + 56):
            mostrar_mensaje_choque(x, y, obsX)
            x, y, dx, obsX, obsY, obs, autos, pts, nivel = reiniciar_juego()
            vb, vo = 10, 10
            pistaY = 0
            acel = des = False
            ca = cd = 0
            continue

        # Cuando pasa un obstáculo
        if obsY > alto:
            obsY = -155
            obsX = random.randrange(175, 625)
            obs = random.randint(0, len(obstaculos) - 1)
            autos += 1
            pts += 15 if vo > vb else 5 if vo < vb else 10
            if autos == 10 * (nivel + 1):
                nivel += 1
                vb += 3
                vo = max(vo, vb)
                mostrar_mensaje_nivel(nivel)

        fondo(pistaY)
        pantalla.blit(auto_jugador, (x, y))
        pantalla.blit(obstaculos[obs], (obsX, obsY))
        tabla_puntaje(autos, pts, nivel, vo, vb)

        pygame.display.update()
        reloj.tick(60)

if __name__ == "__main__":
    # Inicializamos la lista global (por si el usuario cierra sin jugar)
    current_obstaculos = obstaculo_imagenes.copy()
    menu_principal()
    pygame.quit()
