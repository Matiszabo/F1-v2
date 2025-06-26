import pygame
import sys
import time
import random

# Inicialización de Pygame y del sistema de audio
pygame.init()
pygame.mixer.init()

# -----------------------------------------------------------------------------
# Configuración de la ventana principal
# -----------------------------------------------------------------------------
ancho_ventana, alto_ventana = 800, 600  # Dimensiones de la ventana
pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))  # Superficie principal
pygame.display.set_caption("F1: DRIVE TO SURVIVE") # Título de la ventana
reloj = pygame.time.Clock()  # Control de frames por segundo

# -----------------------------------------------------------------------------
# Carga de recursos visuales
# -----------------------------------------------------------------------------
fondo_menu = pygame.transform.scale(pygame.image.load("Fondo.png"), (ancho_ventana, alto_ventana))
fondo_instrucciones = pygame.image.load("Fondo Instrucciones.jpg")
imagen_ferrari = pygame.transform.scale(pygame.image.load("Ferrari.png"), (56, 155))
ancho_auto = 56
imagen_borde_izquierdo = pygame.transform.scale(pygame.image.load("Borde Izquierdo.png"), (175, 600))
imagen_borde_derecho = pygame.transform.scale(pygame.image.load("Borde Derecho.png"), (175, 600))
imagen_pista = pygame.transform.scale(pygame.image.load("Pista.png"), (12, 35))
imagen_humo_explosion = pygame.transform.scale(pygame.image.load("Humo explosion.png"), (150, 150))
nombres_archivos_obstaculos = ["Red Bull.png", "Mercedes.png", "McLaren.png", "Alpine.png", "Aston Martin.png", "Williams.png", "Haas.png", "Racing Bulls.png", "Kick.png"]
imagenes_obstaculos = [pygame.transform.scale(pygame.image.load(nombre), (56, 155)) for nombre in nombres_archivos_obstaculos]

# -----------------------------------------------------------------------------
# Carga de audio
# -----------------------------------------------------------------------------
sonido_boton = pygame.mixer.Sound("boton.mp3")
sonido_explosion = pygame.mixer.Sound("explosion.wav")

# -----------------------------------------------------------------------------
# Fuentes de texto
# -----------------------------------------------------------------------------
fuente_titulo = pygame.font.SysFont("Arial Narrow", 72, bold=True)
fuente_mensaje = pygame.font.SysFont(None, 150)
texto_mensaje_choque = fuente_mensaje.render("¡CHOCASTE!", True, (255, 255, 255))

# -----------------------------------------------------------------------------
# Función: mostrar_mensaje_nivel
# -----------------------------------------------------------------------------
def mostrar_mensaje_nivel(nivel):
    fuente = pygame.font.SysFont(None, 100)
    texto = fuente.render(f"¡Nivel {nivel}!", True, (255, 255, 0))
    x = (ancho_ventana - texto.get_width()) // 2
    y = (alto_ventana - texto.get_height()) // 2
    pantalla.blit(texto, (x, y))
    pygame.display.update()
    time.sleep(2)

# -----------------------------------------------------------------------------
# Función: reiniciar_juego
# -----------------------------------------------------------------------------
def reiniciar_juego():
    pos_x = 400; pos_y = 450; vel_x = 0
    obs_x = random.randrange(175, 625); obs_y = -155
    idx_obs = random.randint(0, len(current_obstaculos) - 1)
    autos_pas = 0; pts = 0; niv = 0
    return pos_x, pos_y, vel_x, obs_x, obs_y, idx_obs, autos_pas, pts, niv

# -----------------------------------------------------------------------------
# Función: dibujar_boton
# -----------------------------------------------------------------------------
def dibujar_boton(texto, x, y, ancho, alto, color_base):
    fuente = pygame.font.SysFont(None, 36)
    rect_boton = pygame.Rect(x, y, ancho, alto)
    mx, my = pygame.mouse.get_pos(); click = pygame.mouse.get_pressed()[0]
    color = list(color_base)
    if rect_boton.collidepoint(mx, my):
        color = [min(255, c + 40) for c in color]
        if click: color = [max(0, c - 80) for c in color]
    pygame.draw.rect(pantalla, color, rect_boton, border_radius=5)
    txt = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(txt, txt.get_rect(center=rect_boton.center))
    return rect_boton

# -----------------------------------------------------------------------------
# Función: dibujar_fondo
# -----------------------------------------------------------------------------
def dibujar_fondo(dy):
    pantalla.fill((29, 29, 28))
    pantalla.blit(imagen_borde_izquierdo, (0, 0))
    pantalla.blit(imagen_borde_derecho, (625, 0))
    x_linea = (ancho_ventana - imagen_pista.get_width()) // 2
    for i in range(8): pantalla.blit(imagen_pista, (x_linea, dy + i * 85 - 85))

# -----------------------------------------------------------------------------
# Función: panel_estadisticas
# -----------------------------------------------------------------------------
def panel_estadisticas(autos_pas, pts, niv, vel, vel_base):
    # Ajuste de dimensiones del panel
    ancho_panel = 200
    alto_panel = 150
    margen = 10
    espacio_y = 10

    # Crear superficie del panel
    panel = pygame.Surface((ancho_panel, alto_panel), pygame.SRCALPHA)
    panel.fill((20, 20, 20, 200))  # Fondo semitransparente

    # Fuentes para etiquetas y valores
    fuente_label = pygame.font.SysFont("Arial", 22, bold=True)
    fuente_valor = pygame.font.SysFont("Arial", 22)

    # Datos a mostrar: (etiqueta, valor, color valor)
    datos = [
        ("Autos Pasados", autos_pas, (255, 255, 255)),
        ("Puntaje", pts, (255, 255, 255)),
        ("Nivel", niv, (255, 255, 255)),
        ("Velocidad", f"{vel*10} KM/H", (255, 0, 0) if vel > vel_base else (0, 255, 0) if vel < vel_base else (255, 255, 255))
    ]

    # Renderizado de cada línea
    for idx, (etiqueta, valor, color_val) in enumerate(datos):
        y = margen + idx * (fuente_label.get_height() + espacio_y)
        # Texto de etiqueta a la izquierda
        surf_etq = fuente_label.render(etiqueta + ":", True, (255, 255, 255))
        panel.blit(surf_etq, (margen, y))
        # Texto de valor alineado a la derecha
        surf_val = fuente_valor.render(str(valor), True, color_val)
        x_val = ancho_panel - margen - surf_val.get_width()
        panel.blit(surf_val, (x_val, y))

    # Mostrar panel en pantalla
    pantalla.blit(panel, (10, 10))

# -----------------------------------------------------------------------------
# Función: mostrar_choque
# -----------------------------------------------------------------------------
def mostrar_choque(px,py):
    pygame.mixer.music.pause(); pantalla.blit(imagen_humo_explosion,(px-imagen_humo_explosion.get_width()//2,py-imagen_humo_explosion.get_height()//2))
    x=(ancho_ventana-texto_mensaje_choque.get_width())//2; y=(alto_ventana-texto_mensaje_choque.get_height())//2
    pantalla.blit(texto_mensaje_choque,(x,y)); sonido_explosion.play(); pygame.display.update(); time.sleep(2)
    pygame.mixer.music.unpause()

# -----------------------------------------------------------------------------
# Función: mostrar_instrucciones
# -----------------------------------------------------------------------------
def mostrar_instrucciones():
    fuente=pygame.font.SysFont(None,32); lineas=["INSTRUCCIONES:","<- / -> o A/D: Mover auto","Arriba / W: Acelerar","Abajo / S: Desacelerar","P: Pausa/Reanuda","Evitar choques","Puntos por pasar autos","Esc o Volver: Menú"]
    overlay=pygame.Surface((ancho_ventana,alto_ventana),pygame.SRCALPHA); overlay.fill((0,0,0,180)); btn=None
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: return
            if e.type==pygame.MOUSEBUTTONDOWN and btn and btn.collidepoint(e.pos): return
        pantalla.blit(fondo_instrucciones,(0,0)); pantalla.blit(overlay,(0,0))
        for i,tx in enumerate(lineas): pantalla.blit(fuente.render(tx,True,(255,255,255)),((ancho_ventana-fuente.size(tx)[0])//2,100+i*40))
        btn=dibujar_boton("Volver",(ancho_ventana-120)//2,alto_ventana-80,120,50,(70,130,180))
        pygame.display.update(); reloj.tick(60)

def seleccionar_auto():
    nombres = ["Ferrari","Red Bull","Mercedes","McLaren","Alpine",
               "Aston Martin","Williams","Haas","Racing Bulls","Kick"]
    colores_principales = [
        (220, 0, 0),    # Ferrari: rojo
        (30, 50, 150),  # Red Bull: azul oscuro
        (0, 210, 190),  # Mercedes: verde azulado
        (255, 140, 0),  # McLaren: naranja brillante
        (0, 110, 255),  # Alpine: azul claro
        (0, 100, 150),  # Aston Martin: azul verdoso/azul marino
        (0, 0, 255),    # Williams: azul
        (150, 150, 150),# Haas: gris
        (0, 0, 0),      # Racing Bulls: negro
        (0, 255, 0)     # Kick: verde
    ]
    lista_autos = [imagen_ferrari] + imagenes_obstaculos.copy()
    w, h = 56, 155; pad_x, pad_y = 40, 40; cols = 5
    inicio_x = (ancho_ventana - (cols * w + (cols-1)*pad_x)) // 2
    inicio_y = (alto_ventana - (2*h + pad_y)) // 2
    fuente_n = pygame.font.SysFont(None,24)
    fuente_t = pygame.font.SysFont(None,36,bold=True)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                for i in range(len(lista_autos)):
                    x = inicio_x + (i % cols) * (w + pad_x)
                    y = inicio_y + (i // cols) * (h + pad_y)
                    if pygame.Rect(x, y, w, h).collidepoint(mx, my):
                        return i

        pantalla.fill((29,29,28))
        # Título con color principal de la escudería seleccionada por defecto (Ferrari)
        titulo_color = colores_principales[0]
        txt_sel = fuente_t.render("Selecciona tu escuderia", True, titulo_color)
        pantalla.blit(txt_sel, ((ancho_ventana - txt_sel.get_width())//2, 20))

        mx, my = pygame.mouse.get_pos()
        for i, coche in enumerate(lista_autos):
            x = inicio_x + (i % cols) * (w + pad_x)
            y = inicio_y + (i // cols) * (h + pad_y)
            rect_coche = pygame.Rect(x, y, w, h)

            # Color principal de esta escudería y su variante clara
            color = colores_principales[i]
            color_claro = tuple(min(255, c+80) for c in color)

            # Si hover, dibuja borde con color_claro y cambia título al color de la escudería
            if rect_coche.collidepoint(mx, my):
                pygame.draw.rect(pantalla, color_claro, rect_coche.inflate(4,4), border_radius=6)
                titulo_color = color
                txt_sel = fuente_t.render("Selecciona tu escuderia", True, titulo_color)
                pantalla.blit(txt_sel, ((ancho_ventana - txt_sel.get_width())//2, 20))

            pantalla.blit(coche, (x, y))
            etiqueta = fuente_n.render(nombres[i], True, (255,255,255))
            pantalla.blit(etiqueta, (x + (w - etiqueta.get_width())//2, y + h + 5))

        pygame.display.update()
        reloj.tick(30)

# -----------------------------------------------------------------------------
# Función: menu_principal
# Muestra el menú con botones Jugar, Instrucciones y Salir
# -----------------------------------------------------------------------------
def menu_principal():
    pygame.mixer.music.load("Cancion.mp3")
    pygame.mixer.music.play(-1)

    ancho_boton, alto_boton = 200, 50
    margen_g = (ancho_ventana - 3*ancho_boton)//4
    y_bots = alto_ventana - 100
    posiciones_x = [margen_g, margen_g+ancho_boton+margen_g, margen_g+2*(ancho_boton+margen_g)]

    titulo = fuente_titulo.render("F1: DRIVE TO SURVIVE", True, (255,255,255))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pantalla.blit(fondo_menu, (0,0))
        pantalla.blit(titulo, ((ancho_ventana-titulo.get_width())//2, 30))

        bot_jugar = dibujar_boton("Jugar", posiciones_x[0], y_bots, ancho_boton, alto_boton, (0,200,0))
        bot_instr = dibujar_boton("Instrucciones", posiciones_x[1], y_bots, ancho_boton, alto_boton, (0,0,200))
        bot_salir = dibujar_boton("Salir", posiciones_x[2], y_bots, ancho_boton, alto_boton, (200,0,0))

        if bot_jugar.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            sonido_boton.play()
            idx = seleccionar_auto()
            lista_todos = [imagen_ferrari] + imagenes_obstaculos.copy()
            auto_jugador = lista_todos[idx]
            obstaculos_juego = lista_todos[:idx] + lista_todos[idx+1:]
            global current_obstaculos
            current_obstaculos = obstaculos_juego
            juego(auto_jugador, obstaculos_juego)
            pygame.mixer.music.load("Cancion.mp3")
            pygame.mixer.music.play(-1)

        if bot_instr.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            sonido_boton.play()
            mostrar_instrucciones()

        if bot_salir.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            sonido_boton.play()
            pygame.quit(); sys.exit()

        pygame.display.update()
        reloj.tick(60)

# -----------------------------------------------------------------------------
# Función: juego
# Lógica principal de la carrera: movimiento, colisiones, puntajes, niveles
# -----------------------------------------------------------------------------
def juego(auto_jugador, lista_obstaculos):
    pygame.mixer.music.load("carrera.mp3")
    pygame.mixer.music.play(-1)

    global current_obstaculos
    current_obstaculos = lista_obstaculos

    # Variables iniciales del juego
    pos_x, pos_y, vel_x, obs_x, obs_y, idx_obs, autos_pas, pts, niv = reiniciar_juego()
    velocidad_base, velocidad_obs = 10, 10
    desplaz_y = 0
    acelerar, desacelerar = False, False
    contador_acel, contador_desc = 0, 0
    en_pausa = False
    fuente_pausa = pygame.font.SysFont(None, 72)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    en_pausa = not en_pausa
                if not en_pausa:
                    if evento.key in (pygame.K_LEFT, pygame.K_a): vel_x = -10
                    if evento.key in (pygame.K_RIGHT, pygame.K_d): vel_x = 10
                    if evento.key == pygame.K_UP or evento.key == pygame.K_w: acelerar = True
                    if evento.key == pygame.K_DOWN or evento.key == pygame.K_s: desacelerar = True
                if evento.key == pygame.K_ESCAPE:
                    return  # Regresa al menú principal
            if evento.type == pygame.KEYUP and not en_pausa:
                if evento.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d): vel_x = 0
                if evento.key == pygame.K_UP or evento.key == pygame.K_w: acelerar, contador_acel = False, 0
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s: desacelerar, contador_desc = False, 0

        if en_pausa:
            texto_pausa = fuente_pausa.render("PAUSA", True, (255,255,255))
            pantalla.blit(texto_pausa, ((ancho_ventana-150)//2,(alto_ventana-100)//2))
            pygame.display.update()
            reloj.tick(5)
            continue

        # Movimiento del jugador
        pos_x += vel_x
        # Acelerar y desacelerar gradualmente
        if acelerar:
            contador_acel += 1
            if contador_acel >= 4:
                velocidad_obs += 1
                contador_acel = 0
        if desacelerar:
            contador_desc += 1
            if contador_desc >= 4:
                velocidad_obs = max(1, velocidad_obs - 1)
                contador_desc = 0

        # Movimiento del obstáculo y fondo de pista
        obs_y += velocidad_obs
        desplaz_y = (desplaz_y + velocidad_obs) % 85

        # Detectar colisión con bordes o autos
        if (pos_x < 175 or pos_x > 625 - ancho_auto or
            (pos_y < obs_y + 155 and pos_y + 155 > obs_y and
             pos_x + ancho_auto > obs_x and pos_x < obs_x + 56)):
            mostrar_choque(pos_x, pos_y)
            # Reiniciar niveles y variables
            pos_x, pos_y, vel_x, obs_x, obs_y, idx_obs, autos_pas, pts, niv = reiniciar_juego()
            velocidad_base, velocidad_obs = 10, 10
            desplaz_y = 0
            acelerar, desacelerar = False, False
            contador_acel, contador_desc = 0, 0
            continue

        # Cuando un obstáculo sale de pantalla (pasa)
        if obs_y > alto_ventana:
            obs_y = -155
            obs_x = random.randrange(175, 625)
            idx_obs = random.randint(0, len(lista_obstaculos)-1)
            autos_pas += 1
            # Puntos según velocidad relativa
            if velocidad_obs > velocidad_base: pts += 15
            elif velocidad_obs < velocidad_base: pts += 5
            else: pts += 10
            # Subir nivel cada 10 autos pasados
            if autos_pas == 10 * (niv + 1):
                niv += 1
                velocidad_base += 3
                velocidad_obs = max(velocidad_obs, velocidad_base)
                mostrar_mensaje_nivel(niv)

        # Dibujar escena
        dibujar_fondo(desplaz_y)
        pantalla.blit(auto_jugador, (pos_x, pos_y))
        pantalla.blit(lista_obstaculos[idx_obs], (obs_x, obs_y))
        panel_estadisticas(autos_pas, pts, niv, velocidad_obs, velocidad_base)

        pygame.display.update()
        reloj.tick(60)

# -----------------------------------------------------------------------------
# Punto de entrada principal
def main():
    global current_obstaculos
    current_obstaculos = imagenes_obstaculos.copy()
    menu_principal()
    pygame.quit()

if __name__ == "__main__":
    main()
