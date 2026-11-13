import pygame
import cenario
import random
import math
import mini

pygame.init()

tela = pygame.display.set_mode((cenario.LARGURA, cenario.ALTURA))
pygame.display.set_caption("Bunny's Farm")

relogio = pygame.time.Clock()

# --- FONTES PARA O MENU E COORDENADAS ---
fonte_menu = pygame.font.Font("PressStart2P-Regular.ttf", 25)
fonte_titulo = pygame.font.Font("PressStart2P-Regular.ttf", 50)
fonte_coord = pygame.font.Font(None, 24)

# --- FUNÇÃO PARA DESENHAR TEXTO COM CONTORNO ---
def renderizar_texto_com_contorno(texto, fonte, cor_texto, cor_contorno, largura_contorno=4):
    superficie_texto = fonte.render(texto, True, cor_texto)
    largura = superficie_texto.get_width() + 2 * largura_contorno
    altura = superficie_texto.get_height() + 2 * largura_contorno
    
    superficie_com_contorno = pygame.Surface((largura, altura), pygame.SRCALPHA)
    
    # Desenha o contorno em deslocamentos ao redor do texto
    for dx in range(-largura_contorno, largura_contorno + 1):
        for dy in range(-largura_contorno, largura_contorno + 1):
            if dx != 0 or dy != 0:
                texto_contorno = fonte.render(texto, True, cor_contorno)
                superficie_com_contorno.blit(texto_contorno, (dx + largura_contorno, dy + largura_contorno))
                
    # Desenha o texto principal por cima
    superficie_com_contorno.blit(superficie_texto, (largura_contorno, largura_contorno))
    return superficie_com_contorno

# configuração imagem de fundo do menu
fundo_menu = pygame.image.load("fundo_menu.jpg")
fundo_menu = pygame.transform.scale(fundo_menu, (cenario.LARGURA, cenario.ALTURA))

# Configuração do Botão Play
largura_botao, altura_botao = 160, 60
pos_botao_x = (cenario.LARGURA - largura_botao) // 2
pos_botao_y = (cenario.ALTURA - altura_botao) // 2
rect_botao_play = pygame.Rect(pos_botao_x, pos_botao_y, largura_botao, altura_botao)

# --- IMAGEM PERSONAGEM ---
imagem_original = pygame.image.load("bunny.png").convert_alpha()
imagem_jogador = pygame.transform.scale(imagem_original, (80, 80))

imagem_mascara_jogador = pygame.transform.scale(imagem_original, (40, 40))
mascara_jogador = pygame.mask.from_surface(imagem_mascara_jogador)

# --- ÁRVORES ---
largura_arvore, altura_arvore = 80, 110
imagem_arvore_original = pygame.image.load("tree.png").convert_alpha()
imagem_arvore = pygame.transform.scale(imagem_arvore_original, (largura_arvore, altura_arvore))

# minigame celeiro
area_minigame_celeiro = pygame.Rect(195, 424, 20, 20)

# --- PEDRINHAS ---
largura_pedrinha, altura_pedrinha = 18, 14
imagem_pedrinha_original = pygame.image.load("pedra.png").convert_alpha()
imagem_pedrinha = pygame.transform.scale(imagem_pedrinha_original, (largura_pedrinha, altura_pedrinha))

posicoes_pedrinhas = [
    (120, 220), (300, 150), (450, 320), (600, 180),
    (250, 400), (500, 480), (110, 100)
]

# --- MATOS, GRAMAS E ARBUSTOS ---
largura_grama, altura_grama = 30, 20
imagem_grama_original = pygame.image.load("grama.png").convert_alpha()
imagem_grama = pygame.transform.scale(imagem_grama_original, (largura_grama, altura_grama))

posicoes_gramas = [
    (80, 180), (220, 280), (380, 120), (520, 220),
    (150, 380), (400, 420), (580, 100), (680, 300),
    (130, 140), (320, 220), (470, 160), (200, 320), (550, 380)
]

largura_arbusto, altura_arbusto = 50, 40
imagem_arbusto_original = pygame.image.load("arbusto.png").convert_alpha()
imagem_arbusto = pygame.transform.scale(imagem_arbusto_original, (largura_arbusto, altura_arbusto))

posicoes_arbustos = [
    (260, 80), (500, 340), (80, 420), (580, 460),
    (180, 240), (420, 260), (350, 440)
]

# --- CONFIGURAÇÃO/IMAGEM - CASA --- 
imagem_casa_original = pygame.image.load("casa.png").convert_alpha()
imagem_casa = pygame.transform.scale(imagem_casa_original, (120, 120))

imagem_interior_casa_original = pygame.image.load("casa_interior.png").convert()
imagem_interior_casa = pygame.transform.scale(imagem_interior_casa_original, (cenario.LARGURA, cenario.ALTURA))

imagem_colisao_casa_original = pygame.image.load("casa_colisao.png").convert_alpha()
imagem_colisao_casa = pygame.transform.scale(imagem_colisao_casa_original, (cenario.LARGURA, cenario.ALTURA))
mascara_casa = pygame.mask.from_surface(imagem_colisao_casa)

# --- IMAGEM - CARTA pós evento
imagem_carta = pygame.image.load("carta.png").convert_alpha()
imagem_carta_grande = pygame.transform.scale(imagem_carta, (420, 520))

# --- CONFIGURAÇÃO/IMAGEM - CELEIRO & SILO ---
largura_celeiro, altura_celeiro = 180, 180
imagem_celeiro_original = pygame.image.load("celeiro.png").convert_alpha()
imagem_celeiro = pygame.transform.scale(imagem_celeiro_original, (largura_celeiro, altura_celeiro))

pos_celeiro = (cenario.LARGURA - largura_celeiro - 10, cenario.ALTURA - altura_celeiro - 10)

colisao_base_celeiro = pygame.Rect(
    pos_celeiro[0] + 15,
    pos_celeiro[1] + altura_celeiro - 50,
    largura_celeiro - 30,
    40
)

largura_silo, altura_silo = 130, 95
imagem_silo_original = pygame.image.load("silo.png").convert_alpha()
imagem_silo = pygame.transform.scale(imagem_silo_original, (largura_silo, altura_silo))

imagem_interior_celeiro_original = pygame.image.load("celeiro_interior.png").convert()
imagem_interior_celeiro = pygame.transform.scale(imagem_interior_celeiro_original, (cenario.LARGURA, cenario.ALTURA))

imagem_colisao_celeiro_original = pygame.image.load("celeiro_colisao.png").convert_alpha()
imagem_colisao_celeiro = pygame.transform.scale(imagem_colisao_celeiro_original, (cenario.LARGURA, cenario.ALTURA))
mascara_celeiro = pygame.mask.from_surface(imagem_colisao_celeiro)

# --- CONFIGURAÇÃO/IMAGEM - PLANTAÇÃO ---
imagem_plantacao_original = pygame.image.load("plantacao.png").convert_alpha()
imagem_plantacao = pygame.transform.scale(imagem_plantacao_original, (150, 130))

# --- CONFIGURAÇÃO/IMAGEM - CATAVENTO ---
largura_catavento, altura_catavento = 150, 160
imagem_catavento_original = pygame.image.load("cata-vento.png").convert_alpha()
imagem_catavento = pygame.transform.scale(imagem_catavento_original, (largura_catavento, altura_catavento))

# --- CONFIGURAÇÃO/IMAGEM - BURACO ---
largura_buraco, altura_buraco = 70, 70
imagem_buraco_original = pygame.image.load("buraco.png").convert_alpha()
imagem_buraco = pygame.transform.scale(imagem_buraco_original, (largura_buraco, altura_buraco))

# --- CONFIGURAÇÃO/IMAGEM - CHÃO ---
imagem_bloco = pygame.image.load("chao.png").convert()
largura_bloco = 32
altura_bloco = 32
imagem_bloco = pygame.transform.scale(imagem_bloco, (largura_bloco, altura_bloco))

# --- CONFIGURAÇÃO/IMAGEM - CHAVE ---
imagem_chave_original = pygame.image.load("chave.png").convert_alpha()
imagem_chave = pygame.transform.scale(imagem_chave_original, (25, 25))
imagem_chave_inventario = pygame.transform.scale(imagem_chave_original, (40, 40))

rect_chave = pygame.Rect(200, 150, 25, 25)
chave_coletada = False

# --- CONFIGURAÇÃO/IMAGEM - bandeja ---
imagem_bandeja_original = pygame.image.load("bandeja.png").convert_alpha()
imagem_bandeja = pygame.transform.scale(imagem_bandeja_original, (120, 70))

# --- imagem fogo
largura_fogo = cenario.LARGURA + 100
altura_fogo = 90  # Ajuste a altura (70) se preferir maior ou menor
imagem_fogo_original = pygame.image.load("fogo.png").convert_alpha()
imagem_fogo = pygame.transform.scale(imagem_fogo_original, (largura_fogo, altura_fogo))

# --- CONFIGURAÇÃO - BAÚ (NO CELEIRO) ---
largura_bau, altura_bau = 65, 50

imagem_bau_fechado_original = pygame.image.load("bau_fechado.png").convert_alpha()
imagem_bau_fechado = pygame.transform.scale(imagem_bau_fechado_original, (largura_bau, altura_bau))

imagem_bau_aberto_original = pygame.image.load("bau_aberto.png").convert_alpha()
imagem_bau_aberto = pygame.transform.scale(imagem_bau_aberto_original, (largura_bau, altura_bau))

pos_bau_x = 674
pos_bau_y = 135
rect_bau = pygame.Rect(pos_bau_x, pos_bau_y, largura_bau, altura_bau)
bau_aberto = False
buraco_liberado = False
noite_ativada = False
carta_coletada = False  
carta_aberta = False
tempo_abertura_carta = 0

# --- CONFIGURAÇÃO DO INVENTÁRIO ---
inventario_aberto = False
itens_inventario = [None, None, None]

# --- CONFIGURAÇÃO DO MINIGAME cookies ---
imagem_fundo_minigame_original = pygame.image.load("fundo_minigame.png").convert()
imagem_fundo_minigame = pygame.transform.scale(imagem_fundo_minigame_original, (cenario.LARGURA, cenario.ALTURA))

imagem_cookie_original = pygame.image.load("cookie.png").convert_alpha()
imagem_cookie = pygame.transform.scale(imagem_cookie_original, (60, 60))

area_minigame = pygame.Rect(710, 192, 20, 20)
cesta_x = cenario.LARGURA // 2
cesta_y = cenario.ALTURA - 124
cesta_largura = 70
cesta_altura = 10
cesta_velocidade = 9

cookies = []
pontos_minigame = 0

def resetar_minigame():
    global cesta_x, cookies, pontos_minigame
    cesta_x = cenario.LARGURA // 2
    pontos_minigame = 0
    cookies = []
    for _ in range(6):
        cookies.append({
            'rect': pygame.Rect(random.randint(20, cenario.LARGURA - 40), random.randint(-400, -30), 30, 30),
            'vel': random.randint(2, 4)
        })

# --- CONFIGURAÇÃO DO MINIGAME PLANTAÇÃO (ADUBO) ---
imagem_cenoura_original = pygame.image.load("cenoura.png").convert_alpha()
imagem_cenoura = pygame.transform.scale(imagem_cenoura_original, (35, 35))

imagem_fundo_plantacao_original = pygame.image.load("chao.png").convert()
imagem_fundo_plantacao = pygame.transform.scale(imagem_fundo_plantacao_original, (cenario.LARGURA, cenario.ALTURA))

linhas_plantacao = 8
colunas_plantacao = 8
largura_slot = 90
altura_slot = 70
offset_x = (cenario.LARGURA - (colunas_plantacao * largura_slot)) // 2
offset_y = (cenario.ALTURA - (linhas_plantacao * altura_slot)) // 2

grid_plantacao = []

def resetar_minigame_plantacao():
    global grid_plantacao
    grid_plantacao = []
    for l in range(linhas_plantacao):
        linha = []
        for c in range(colunas_plantacao):
            rect_slot = pygame.Rect(
                offset_x + c * largura_slot,
                offset_y + l * altura_slot,
                largura_slot,
                altura_slot
            )
            linha.append({'rect': rect_slot, 'adubado': False})
        grid_plantacao.append(linha)

# --- Variáveis de Estado Geral do Jogo ---
estado_jogo = "menu"
estado_cenario = "fora"

jogador = pygame.Rect(20, 164, 30, 30)
velocidade = 4

pos_casa = (20, 20)
pos_silo = (580, 415)

pos_plantacao = (cenario.LARGURA - 160, 10)
pos_catavento = (pos_plantacao[0] - 80, 7)
pos_buraco = (5, cenario.ALTURA - altura_buraco - 5)

area_casa = pygame.Rect(55, 55, 50, 50)
area_celeiro = pygame.Rect(cenario.LARGURA - largura_celeiro + 40, cenario.ALTURA - altura_celeiro + 60, 60, 60)
area_buraco = pygame.Rect(pos_buraco[0] + 15, pos_buraco[1] + 15, 40, 40)

# --- ÁREA DE TELETRANSPORTE REDUZIDA DA PLANTAÇÃO ---
area_plantacao = pygame.Rect(
    pos_plantacao[0] + 45,
    pos_plantacao[1] + 40,
    60,
    50
)

area_saida_casa = pygame.Rect(cenario.LARGURA // 2 - 20, cenario.ALTURA - 50, 40, 40)
area_saida_celeiro = pygame.Rect(20, cenario.ALTURA // 2 - 20, 40, 40)
area_saida_buraco = pygame.Rect(cenario.LARGURA // 2 - 20, cenario.ALTURA - 50, 40, 40)

posicoes_arvores = [
    (150, 100), (550, 120), (200, 450), (680, 336),
    (100, 300), (400, 80), (680, 200), (300, 500),
    (230, 200), (480, 280), (450, 480), (320, 320), 
    (520, 40),  (350, 20),  (80, 480),  (600, 500),
    (50, 150),  (380, 180), (280, 350), (620, 80),  (180, 380),
    (580, 238), (241, 49)
]

colisoes_arvores = [pygame.Rect(x + 20, y + 80, 40, 25) for x, y in posicoes_arvores]

rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado_jogo == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if rect_botao_play.collidepoint(evento.pos):
                    estado_jogo = "jogo"

        elif estado_jogo == "jogo":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e:
                    if estado_cenario not in ("minigame_food_drop", "minigame_plantacao"):
                        inventario_aberto = not inventario_aberto

                # --- VOLTAR PARA O MENU COM A TECLA M ---
                if evento.key == pygame.K_m:
                    estado_jogo = "menu"
                    estado_cenario = "fora"

                # Interação com o Baú no celeiro
                if evento.key == pygame.K_y:
                    if estado_cenario == "dentro_celeiro":
                        area_interacao_bau = rect_bau.inflate(100, 60)
                        if jogador.colliderect(area_interacao_bau):
                            if not bau_aberto and imagem_chave_inventario in itens_inventario:
                                bau_aberto = True
                                buraco_liberado = True
                                indice_chave = itens_inventario.index(imagem_chave_inventario)
                                itens_inventario[indice_chave] = None

                    elif estado_cenario == "dentro_casa":
                        if noite_ativada and not carta_coletada:
                            area_carta = pygame.Rect(cenario.LARGURA // 2 - 20, cenario.ALTURA // 2 - 20, 40, 40)
                            if jogador.colliderect(area_carta) and not carta_aberta:
                                carta_aberta = True
                                carta_coletada = True
                                tempo_abertura_carta = pygame.time.get_ticks()          

                # Sair dos minigames
                if evento.key == pygame.K_ESCAPE:
                    if estado_cenario == "minigame_food_drop":
                        estado_cenario = "dentro_casa"
                        # Posiciona o jogador centralizado na casa
                        jogador.x = cenario.LARGURA // 2 - jogador.width // 2
                        jogador.y = cenario.ALTURA // 2 - jogador.height // 2
                    elif estado_cenario == "minigame_plantacao":
                        estado_cenario = "fora"
                        jogador.x = pos_plantacao[0] - 50

    # ================= TELAS DE JOGO =================
    if estado_jogo == "menu":
        tela.blit(fundo_menu, (0, 0))

        # 1. Cálculo do tempo e fator de escala
        tempo = pygame.time.get_ticks() / 300
        fator_escala = 1.0 + 0.08 * math.sin(tempo)

        # 2. Renderização do texto com contorno preto
        texto_base = renderizar_texto_com_contorno(
            "Bunny's Farm", 
            fonte_titulo, 
            cor_texto=(255, 255, 255), 
            cor_contorno=(0, 0, 0), 
            largura_contorno=4
        )

        # 3. Redimensionamento da imagem usando a escala
        largura_animada = int(texto_base.get_width() * fator_escala)
        altura_animada = int(texto_base.get_height() * fator_escala)
        texto_titulo = pygame.transform.scale(texto_base, (largura_animada, altura_animada))

        # 4. Centralização dinâmica da imagem modificada
        rect_titulo = texto_titulo.get_rect(center=(cenario.LARGURA // 2, pos_botao_y - 80))
        tela.blit(texto_titulo, rect_titulo)

        # Botão Play
        pos_mouse = pygame.mouse.get_pos()
        cor_botao = (70, 160, 70) if rect_botao_play.collidepoint(pos_mouse) else (50, 120, 50)

        pygame.draw.rect(tela, cor_botao, rect_botao_play, border_radius=12)
        pygame.draw.rect(tela, (200, 250, 200), rect_botao_play, width=3, border_radius=12)

        texto_play = fonte_menu.render("PLAY", True, (255, 255, 255))
        texto_x = pos_botao_x + (largura_botao - texto_play.get_width()) // 2
        texto_y = pos_botao_y + (altura_botao - texto_play.get_height()) // 2
        tela.blit(texto_play, (texto_x, texto_y))

    elif estado_jogo == "jogo":
        teclas = pygame.key.get_pressed()

        if not inventario_aberto and estado_cenario != "minigame_food_drop":
            # Movimentação Horizontal
            if teclas[pygame.K_a]:
                jogador.x -= velocidade
                if estado_cenario == "fora":
                    for tronco in colisoes_arvores:
                        if jogador.colliderect(tronco):
                            jogador.x = tronco.right
                    if jogador.colliderect(colisao_base_celeiro):
                        jogador.x = colisao_base_celeiro.right
                elif estado_cenario == "dentro_casa":
                    offset_y = -10
                    if mascara_casa.overlap(mascara_jogador, (jogador.x, jogador.y)):
                        jogador.x += velocidade
                elif estado_cenario == "dentro_celeiro":
                    offset_y = - 27
                    if mascara_celeiro.overlap(mascara_jogador, (jogador.x, jogador.y + offset_y)):
                        jogador.x += velocidade

            if teclas[pygame.K_d]:
                jogador.x += velocidade
                if estado_cenario == "fora":
                    for tronco in colisoes_arvores:
                        if jogador.colliderect(tronco):
                            jogador.x = tronco.left - jogador.width
                    if jogador.colliderect(colisao_base_celeiro):
                        jogador.x = colisao_base_celeiro.left - jogador.width
                elif estado_cenario == "dentro_casa":
                    if mascara_casa.overlap(mascara_jogador, (jogador.x, jogador.y)):
                        jogador.x -= velocidade
                elif estado_cenario == "dentro_celeiro":
                    offset_y = - 27
                    if mascara_celeiro.overlap(mascara_jogador, (jogador.x, jogador.y + offset_y)):
                        jogador.x -= velocidade

            # Movimentação Vertical
            if teclas[pygame.K_w]:
                jogador.y -= velocidade
                if estado_cenario == "fora":
                    for tronco in colisoes_arvores:
                        if jogador.colliderect(tronco):
                            jogador.y = tronco.bottom
                    if jogador.colliderect(colisao_base_celeiro):
                        jogador.y = colisao_base_celeiro.bottom
                elif estado_cenario == "dentro_casa":
                    if mascara_casa.overlap(mascara_jogador, (jogador.x, jogador.y)):
                        jogador.y += velocidade
                elif estado_cenario == "dentro_celeiro":
                    offset_y = - 27
                    if mascara_celeiro.overlap(mascara_jogador, (jogador.x, jogador.y + offset_y)):
                        jogador.y += velocidade

            if teclas[pygame.K_s]:
                jogador.y += velocidade
                if estado_cenario == "fora":
                    for tronco in colisoes_arvores:
                        if jogador.colliderect(tronco):
                            jogador.y = tronco.top - jogador.height
                    if jogador.colliderect(colisao_base_celeiro):
                        jogador.y = colisao_base_celeiro.top - jogador.height
                elif estado_cenario == "dentro_casa":
                    if mascara_casa.overlap(mascara_jogador, (jogador.x, jogador.y)):
                        jogador.y -= velocidade
                elif estado_cenario == "dentro_celeiro":
                    offset_y = - 27
                    if mascara_celeiro.overlap(mascara_jogador, (jogador.x, jogador.y + offset_y)):
                        jogador.y -= velocidade

            jogador.clamp_ip(tela.get_rect())

        # Coleta da chave dentro da casa
        if estado_cenario == "dentro_casa" and not chave_coletada:
            if jogador.colliderect(rect_chave):
                chave_coletada = True
                for i in range(len(itens_inventario)):
                    if itens_inventario[i] is None:
                        itens_inventario[i] = imagem_chave_inventario
                        break

        # Verificação de transição de cenários
        if estado_cenario == "fora":
            if jogador.colliderect(area_casa):
                estado_cenario = "dentro_casa"
                jogador.x = cenario.LARGURA // 2 - 20
                jogador.y = cenario.ALTURA // 2 - 20
            elif jogador.colliderect(area_celeiro):
                estado_cenario = "dentro_celeiro"
                jogador.x = 60
                jogador.y = cenario.ALTURA // 2 - 20
            elif buraco_liberado and jogador.colliderect(area_buraco):
                estado_cenario = "dentro_buraco"
                noite_ativada = True
                jogador.x = cenario.LARGURA // 2 - 20
                jogador.y = cenario.ALTURA // 2 - 20
            elif jogador.colliderect(area_plantacao):
                if not noite_ativada:
                    resetar_minigame_plantacao()
                    estado_cenario = "minigame_plantacao"
                    jogador.x = cenario.LARGURA // 2
                    jogador.y = cenario.ALTURA // 2

        elif estado_cenario == "dentro_casa":
            if jogador.colliderect(area_saida_casa):
                estado_cenario = "fora"
                jogador.x = 60
                jogador.y = 150
            elif jogador.colliderect(area_minigame):
                if not noite_ativada:
                    resetar_minigame()
                    estado_cenario = "minigame_food_drop"
            
        elif estado_cenario == "dentro_celeiro":
            if jogador.colliderect(area_saida_celeiro):
                estado_cenario = "fora"
                jogador.x = cenario.LARGURA - largura_celeiro + 20
                jogador.y = cenario.ALTURA - altura_celeiro - 30
           
        elif estado_cenario == "dentro_buraco":
            if jogador.colliderect(area_saida_buraco):
                estado_cenario = "fora"
                jogador.x = pos_buraco[0] + 80
                jogador.y = pos_buraco[1] - 10

        pos_desenho_x = jogador.x - 20
        pos_desenho_y = jogador.y - 20

        if estado_cenario == "fora":
            for x in range(0, cenario.LARGURA, largura_bloco):
                for y in range(0, cenario.ALTURA, altura_bloco):
                    tela.blit(imagem_bloco, (x, y))

            tela.blit(imagem_casa, pos_casa)
            tela.blit(imagem_silo, pos_silo)
            tela.blit(imagem_plantacao, pos_plantacao)

            if buraco_liberado:
                tela.blit(imagem_buraco, pos_buraco)

            elementos_jogo = []

            elementos_jogo.append({
                'y_base': jogador.y + 40,
                'imagem': imagem_jogador,
                'pos': (pos_desenho_x, pos_desenho_y)
            })

            elementos_jogo.append({
                'y_base': pos_celeiro[1] + altura_celeiro,
                'imagem': imagem_celeiro,
                'pos': pos_celeiro
            })

            elementos_jogo.append({
                'y_base': pos_catavento[1] + altura_catavento,
                'imagem': imagem_catavento,
                'pos': pos_catavento
            })

            for pos in posicoes_arvores:
                elementos_jogo.append({
                    'y_base': pos[1] + altura_arvore,
                    'imagem': imagem_arvore,
                    'pos': pos
                })

            for pos in posicoes_pedrinhas:
                elementos_jogo.append({
                    'y_base': pos[1] + altura_pedrinha,
                    'imagem': imagem_pedrinha,
                    'pos': pos
                })

            for pos in posicoes_gramas:
                elementos_jogo.append({
                    'y_base': pos[1] + altura_grama,
                    'imagem': imagem_grama,
                    'pos': pos
                })

            for pos in posicoes_arbustos:
                elementos_jogo.append({
                    'y_base': pos[1] + altura_arbusto - 15,
                    'imagem': imagem_arbusto,
                    'pos': pos
                })

            elementos_jogo.sort(key=lambda elem: elem['y_base'])

            for elem in elementos_jogo:
                tela.blit(elem['imagem'], elem['pos'])

        elif estado_cenario == "dentro_casa":
            tela.blit(imagem_interior_casa, (0, 0))

            if not chave_coletada:
                tela.blit(imagem_chave, (rect_chave.x, rect_chave.y))

            # --- DESENHA A CARTA NO CHÃO DA CASA ---
            if noite_ativada and not carta_coletada:
                area_carta = pygame.Rect(cenario.LARGURA // 2 - 20, cenario.ALTURA // 2 - 20, 40, 40)
                carta_pequena = pygame.transform.scale(imagem_carta, (40, 40))
                tela.blit(carta_pequena, (area_carta.x, area_carta.y))

            pygame.draw.ellipse(tela, (255, 215, 0), area_minigame, width=2)

            ponto1 = (area_saida_casa.x + 5, area_saida_casa.y + 5)
            ponto2 = (area_saida_casa.x + 35, area_saida_casa.y + 5)
            ponto3 = (area_saida_casa.x + 20, area_saida_casa.y + 35)
            pygame.draw.polygon(tela, (255, 50, 50), [ponto1, ponto2, ponto3])
            tela.blit(imagem_jogador, (pos_desenho_x, pos_desenho_y))

        elif estado_cenario == "dentro_celeiro":
            tela.blit(imagem_interior_celeiro, (0, 0))

            pygame.draw.circle(tela, (255, 255, 0), area_minigame_celeiro.center, 10, 2)

            if jogador.colliderect(area_minigame_celeiro):
                if not noite_ativada:
                    if not minigame_aberto:
                        minigame_aberto = True
                        mini.jogar(tela)

            else:
                minigame_aberto = False

            if bau_aberto:
                tela.blit(imagem_bau_aberto, (pos_bau_x, pos_bau_y))
            else:
                tela.blit(imagem_bau_fechado, (pos_bau_x, pos_bau_y))

            tela.blit(imagem_jogador, (pos_desenho_x, pos_desenho_y))

        elif estado_cenario == "dentro_buraco":
            tela.fill((40, 30, 30))
            ponto_seta1 = (area_saida_buraco.x + 5, area_saida_buraco.y + 5)
            ponto_seta2 = (area_saida_buraco.x + 35, area_saida_buraco.y + 5)
            ponto_seta3 = (area_saida_buraco.x + 20, area_saida_buraco.y + 35)
            pygame.draw.polygon(tela, (255, 50, 50), [ponto_seta1, ponto_seta2, ponto_seta3])
            tela.blit(imagem_jogador, (pos_desenho_x, pos_desenho_y))

        # --- LÓGICA DO MINIGAME PLANTAÇÃO ---
        elif estado_cenario == "minigame_plantacao":
            for x in range(0, cenario.LARGURA, largura_bloco):
                for y in range(0, cenario.ALTURA, altura_bloco):
                    tela.blit(imagem_bloco, (x, y))
                

            total_slots = linhas_plantacao * colunas_plantacao
            slots_adubados = 0

            centro_jogador = pygame.Rect(jogador.x + 10, jogador.y + 10, 20, 20)

            for linha in grid_plantacao:
                for slot in linha:
                    if centro_jogador.colliderect(slot['rect']):
                        slot['adubado'] = True

                    if slot['adubado']:
                        slots_adubados += 1
                        cor_terra = (70, 40, 20)
                    else:
                        cor_terra = (160, 110, 60)

                    pygame.draw.rect(tela, cor_terra, slot['rect'], border_radius=0)

                    if slot['adubado']:
                        pos_cenoura_x = slot['rect'].centerx - (imagem_cenoura.get_width() // 2)
                        pos_cenoura_y = slot['rect'].centery - (imagem_cenoura.get_height() // 2)
                        tela.blit(imagem_cenoura, (pos_cenoura_x, pos_cenoura_y))

            tela.blit(imagem_jogador, (pos_desenho_x, pos_desenho_y))

            porcentagem = int((slots_adubados / total_slots) * 100)
            texto_progresso = fonte_menu.render(f"Fertilized: {porcentagem}%", True, (255, 255, 255))
            tela.blit(texto_progresso, (20, 20))

            texto_sair = fonte_coord.render("Press ESC to exit", True, (230, 230, 230))
            tela.blit(texto_sair, (cenario.LARGURA - 220, 20))

            if slots_adubados == total_slots:
                texto_sucesso = fonte_titulo.render("Fertilized Plantation!", True, (255, 255, 255))

                # --- REDIMENSIONAR O TEXTO ---
                fator_escala = 0.6  # 0.6 diminui para 60% do tamanho. Ajuste esse valor como preferir!
                novo_tamanho = (int(texto_sucesso.get_width() * fator_escala), int(texto_sucesso.get_height() * fator_escala))
                texto_sucesso = pygame.transform.scale(texto_sucesso, novo_tamanho)
                
                superficie_texto = pygame.Surface((texto_sucesso.get_width() + 20, texto_sucesso.get_height() + 10), pygame.SRCALPHA)
                superficie_texto.fill((0, 0, 0, 150))
                superficie_texto.blit(texto_sucesso, (10, 5))
                pos_x_win = (cenario.LARGURA - superficie_texto.get_width()) // 2
                tela.blit(superficie_texto, (pos_x_win, cenario.ALTURA - 90))

        # --- LÓGICA DO MINIGAME FOOD DROP ---
        elif estado_cenario == "minigame_food_drop":
            tela.blit(imagem_fundo_minigame, (0, 0))

            if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                cesta_x -= cesta_velocidade
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                cesta_x += cesta_velocidade

            cesta_x = max(0, min(cesta_x, cenario.LARGURA - cesta_largura))
            rect_cesta = pygame.Rect(cesta_x, cesta_y, cesta_largura, cesta_altura)

            # Desenha a imagem da bandeja no lugar do retângulo branco
            tela.blit(imagem_bandeja, (cesta_x, cesta_y))

            for cookie in cookies:
                cookie['rect'].y += cookie['vel']

                if cookie['rect'].colliderect(rect_cesta):
                    pontos_minigame += 10
                    cookie['rect'].y = random.randint(-200, -30)
                    cookie['rect'].x = random.randint(20, cenario.LARGURA - 40)

                elif cookie['rect'].y > cenario.ALTURA:
                    cookie['rect'].y = random.randint(-200, -30)
                    cookie['rect'].x = random.randint(20, cenario.LARGURA - 40)

                tela.blit(imagem_cookie, (cookie['rect'].x, cookie['rect'].y))

            # 2. SEGUNDO: Desenha o fogo por cima dos cookies (criando a camada da frente no rodapé)
            pos_fogo_y = cenario.ALTURA - altura_fogo
            tela.blit(imagem_fogo, (-50, pos_fogo_y))

            # 3. TERCEIRO: Desenha a bandeja por cima de tudo para pegar os cookies
            tela.blit(imagem_bandeja, (cesta_x, cesta_y))

            texto_pts = fonte_menu.render(f"Points: {pontos_minigame}", True, (255, 255, 255))
            tela.blit(texto_pts, (20, 20))

            texto_sair = fonte_coord.render("Press ESC to exit", True, (200, 200, 200))
            tela.blit(texto_sair, (cenario.LARGURA - 200, 20))

            if pontos_minigame >= 500:
                texto_win = fonte_titulo.render("YOU WON!", True, (100, 255, 100))
                tela.blit(texto_win, ((cenario.LARGURA - texto_win.get_width()) // 2, cenario.ALTURA // 2 - 30))

        # --- HUD (Apenas Coordenadas) ---
        if estado_cenario not in ("minigame_food_drop", "minigame_plantacao"):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            texto_coord = fonte_coord.render(f"X: {mouse_x} | Y: {mouse_y}", True, (255, 255, 255))
            superficie_coord = pygame.Surface((texto_coord.get_width() + 10, texto_coord.get_height() + 6), pygame.SRCALPHA)
            superficie_coord.fill((0, 0, 0, 120))
            superficie_coord.blit(texto_coord, (5, 3))
            tela.blit(superficie_coord, (cenario.LARGURA - superficie_coord.get_width() - 10, 10))

        # ==========================================
        # EFEITO NOITE GLOBAL (Escurece todo o jogo)
        # ==========================================
        if noite_ativada and estado_cenario not in ("minigame_food_drop", "minigame_plantacao"):
            overlay_noite = pygame.Surface((cenario.LARGURA, cenario.ALTURA), pygame.SRCALPHA)
            overlay_noite.fill((10, 10, 30, 160))  # Cor preta/azulada com transparência
            tela.blit(overlay_noite, (0, 0))

        # ==========================================
        # EXIBIÇÃO DA CARTA EM TAMANHO LEGÍVEL
        # ==========================================
        if carta_aberta:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - tempo_abertura_carta >= 3000:
                carta_aberta = False
                rodando = False

            # Fundo escuro semi-transparente para destacar a carta
            overlay_carta = pygame.Surface((cenario.LARGURA, cenario.ALTURA), pygame.SRCALPHA)
            overlay_carta.fill((0, 0, 0, 190))
            tela.blit(overlay_carta, (0, 0))

            # Centraliza e desenha a carta redimensionada
            carta_rect = imagem_carta_grande.get_rect(center=(cenario.LARGURA // 2, cenario.ALTURA // 2))
            tela.blit(imagem_carta_grande, carta_rect.topleft)

            # Aviso abaixo da carta
            texto_aviso_tempo = fonte_coord.render("Lendo carta...", True, (255, 255, 255))
            tela.blit(texto_aviso_tempo, (cenario.LARGURA // 2 - 50, carta_rect.bottom + 10))

        # --- HUD (Apenas Coordenadas) ---
        if estado_cenario not in ("minigame_food_drop", "minigame_plantacao"):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            texto_coord = fonte_coord.render(f"X: {mouse_x} | Y: {mouse_y}", True, (255, 255, 255))

        # --- INVENTÁRIO ---
        if inventario_aberto:
            superficie_fundo = pygame.Surface((cenario.LARGURA, cenario.ALTURA), pygame.SRCALPHA)
            superficie_fundo.fill((0, 0, 0, 150))
            tela.blit(superficie_fundo, (0, 0))

            painel_largura, painel_altura = 260, 100
            painel_x = (cenario.LARGURA - painel_largura) // 2
            painel_y = (cenario.ALTURA - painel_altura) // 2

            pygame.draw.rect(tela, (50, 35, 25), (painel_x, painel_y, painel_largura, painel_altura), border_radius=10)
            pygame.draw.rect(tela, (200, 170, 120), (painel_x, painel_y, painel_largura, painel_altura), width=4, border_radius=10)

            tamanho_slot = 60
            espacamento = 15
            inicio_x = painel_x + 20
            inicio_y = painel_y + 20

            for i in range(3):
                slot_x = inicio_x + i * (tamanho_slot + espacamento)
                slot_y = inicio_y

                pygame.draw.rect(tela, (30, 20, 15), (slot_x, slot_y, tamanho_slot, tamanho_slot), border_radius=5)
                pygame.draw.rect(tela, (150, 120, 80), (slot_x, slot_y, tamanho_slot, tamanho_slot), width=2, border_radius=5)

                if i < len(itens_inventario) and itens_inventario[i] is not None:
                    item_img = itens_inventario[i]
                    img_x = slot_x + (tamanho_slot - item_img.get_width()) // 2
                    img_y = slot_y + (tamanho_slot - item_img.get_height()) // 2
                    tela.blit(item_img, (img_x, img_y))

        

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()