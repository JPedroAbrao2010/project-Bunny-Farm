import pygame
import random
import math

pygame.init()

LARGURA, ALTURA = 800, 600

fonte_ui = pygame.font.Font(None, 24)
fonte_titulo = pygame.font.Font(None, 50)

# --- CORES ---
COR_FUNDO = (0, 0, 0)             # Fundo Preto
COR_CAIXA = (45, 45, 50)          # Metal da caixa
COR_SILHUETA = (20, 20, 25)       # Recortes/Sombras na caixa
COR_ITEM = (210, 160, 50)        # Cor Amarela/Dourada única para TODOS os itens
COR_TEXTO = (255, 255, 255)

class DesenharObjeto:
    """Função estática para desenhar as formas específicas de cada item."""

    @staticmethod
    def desenhar_item(superficie, nome, x, y, angulo, cor, e_silhueta=False):
        tamanho_max = 200
        s = pygame.Surface((tamanho_max, tamanho_max), pygame.SRCALPHA)
        cx, cy = tamanho_max // 2, tamanho_max // 2

        c_preenchimento = cor
        c_linha = (70, 70, 80) if e_silhueta else (30, 30, 30)
        esp = 0 if not e_silhueta else 2

        if nome == "Martelo":
            pygame.draw.rect(s, c_preenchimento, (cx - 5, cy - 40, 10, 80), border_radius=3)
            pygame.draw.rect(s, c_preenchimento, (cx - 25, cy - 48, 50, 18), border_radius=4)
            if esp: pygame.draw.rect(s, c_linha, (cx - 25, cy - 48, 50, 18), esp, border_radius=4)

        elif nome == "Alicate":
            pygame.draw.line(s, c_preenchimento, (cx - 10, cy + 30), (cx - 3, cy - 5), 8)
            pygame.draw.line(s, c_preenchimento, (cx + 10, cy + 30), (cx + 3, cy - 5), 8)
            pygame.draw.polygon(s, c_preenchimento, [(cx - 8, cy - 5), (cx + 8, cy - 5), (cx, cy - 35)])

        elif nome == "Foice":
            pygame.draw.rect(s, c_preenchimento, (cx - 4, cy, 8, 45), border_radius=2)
            pygame.draw.arc(s, c_preenchimento, (cx - 35, cy - 40, 50, 50), 0, math.pi, 12)

        elif nome == "Chave":
            pygame.draw.rect(s, c_preenchimento, (cx - 5, cy - 30, 10, 60), border_radius=2)
            pygame.draw.circle(s, c_preenchimento, (cx, cy - 30), 14)
            pygame.draw.circle(s, COR_CAIXA if e_silhueta else (0, 0, 0, 0), (cx, cy - 30), 6)

        elif nome == "Óleo":
            pygame.draw.rect(s, c_preenchimento, (cx - 20, cy - 10, 40, 45), border_radius=8)
            pygame.draw.polygon(s, c_preenchimento, [(cx - 5, cy - 10), (cx + 5, cy - 10), (cx - 20, cy - 40)])

        elif nome == "Serrote":
            pygame.draw.polygon(s, c_preenchimento, [(cx - 50, cy - 15), (cx + 40, cy - 5), (cx + 30, cy + 15), (cx - 50, cy + 15)])
            pygame.draw.circle(s, c_preenchimento, (cx - 50, cy), 18, width=7)

        elif nome == "Trena":
            pygame.draw.rect(s, c_preenchimento, (cx - 25, cy - 25, 50, 50), border_radius=10)
            pygame.draw.rect(s, c_preenchimento, (cx + 25, cy + 10, 15, 8))

        elif nome == "Pá":
            pygame.draw.rect(s, c_preenchimento, (cx - 4, cy - 45, 8, 65))
            pygame.draw.polygon(s, c_preenchimento, [(cx - 22, cy + 20), (cx + 22, cy + 20), (cx, cy + 55)])

        elif nome == "Picareta":
            pygame.draw.rect(s, c_preenchimento, (cx - 4, cy - 30, 8, 70))
            pygame.draw.polygon(s, c_preenchimento, [(cx - 45, cy - 25), (cx, cy - 35), (cx + 45, cy - 25), (cx, cy - 20)])

        elif nome == "Tesoura":
            pygame.draw.polygon(s, c_preenchimento, [(cx - 5, cy), (cx - 15, cy - 35), (cx, cy - 10)])
            pygame.draw.polygon(s, c_preenchimento, [(cx + 5, cy), (cx + 15, cy - 35), (cx, cy - 10)])
            pygame.draw.circle(s, c_preenchimento, (cx - 12, cy + 15), 10, width=4)
            pygame.draw.circle(s, c_preenchimento, (cx + 12, cy + 15), 10, width=4)

        elif nome == "Pregos":
            for offset_x in [-12, 0, 12]:
                pygame.draw.rect(s, c_preenchimento, (cx + offset_x - 2, cy - 15, 4, 30))
                pygame.draw.rect(s, c_preenchimento, (cx + offset_x - 6, cy - 18, 12, 4))

        elif nome == "Engrenagem":
            pygame.draw.circle(s, c_preenchimento, (cx, cy), 28)
            for i in range(8):
                a = i * (math.pi / 4)
                dx, dy = int(math.cos(a) * 32), int(math.sin(a) * 32)
                pygame.draw.circle(s, c_preenchimento, (cx + dx, cy + dy), 7)
            pygame.draw.circle(s, COR_SILHUETA if e_silhueta else COR_FUNDO, (cx, cy), 10)

        elif nome == "Régua":
            pygame.draw.rect(s, c_preenchimento, (cx - 65, cy - 12, 130, 24), border_radius=3)

        # --- ITENS INÚTEIS (LIXO DO CELEIRO) ---
        elif nome == "Rato":
            pygame.draw.ellipse(s, c_preenchimento, (cx - 20, cy - 10, 40, 24))
            pygame.draw.circle(s, c_preenchimento, (cx - 15, cy - 12), 6)
            pygame.draw.line(s, c_preenchimento, (cx + 20, cy), (cx + 35, cy + 5), 2)

        elif nome == "Ovo":
            pygame.draw.ellipse(s, c_preenchimento, (cx - 15, cy - 22, 30, 44))

        elif nome == "Tomate":
            pygame.draw.circle(s, c_preenchimento, (cx, cy), 20)
            pygame.draw.polygon(s, c_preenchimento, [(cx - 5, cy - 20), (cx + 5, cy - 20), (cx, cy - 25)])

        elif nome == "Ferradura":
            pygame.draw.arc(s, c_preenchimento, (cx - 20, cy - 20, 40, 40), 0, math.pi, 10)

        elif nome == "Osso":
            pygame.draw.rect(s, c_preenchimento, (cx - 20, cy - 5, 40, 10))
            pygame.draw.circle(s, c_preenchimento, (cx - 20, cy - 5), 7)
            pygame.draw.circle(s, c_preenchimento, (cx - 20, cy + 5), 7)
            pygame.draw.circle(s, c_preenchimento, (cx + 20, cy - 5), 7)
            pygame.draw.circle(s, c_preenchimento, (cx + 20, cy + 5), 7)

        elif nome == "Lâmpada":
            pygame.draw.circle(s, c_preenchimento, (cx, cy - 8), 16)
            pygame.draw.rect(s, c_preenchimento, (cx - 8, cy + 6, 16, 12))

        elif nome == "Maçã":
            pygame.draw.circle(s, c_preenchimento, (cx, cy), 18)
            pygame.draw.line(s, c_preenchimento, (cx, cy - 18), (cx + 4, cy - 26), 3)

        elif nome == "Pneu":
            pygame.draw.circle(s, c_preenchimento, (cx, cy), 24, width=10)

        elif nome == "Garrafa":
            pygame.draw.rect(s, c_preenchimento, (cx - 10, cy - 10, 20, 35), border_radius=4)
            pygame.draw.rect(s, c_preenchimento, (cx - 5, cy - 25, 10, 15))

        elif nome == "Lápis":
            pygame.draw.rect(s, c_preenchimento, (cx - 4, cy - 25, 8, 45))
            pygame.draw.polygon(s, c_preenchimento, [(cx - 4, cy - 25), (cx + 4, cy - 25), (cx, cy - 35)])

        elif nome == "Massa":
            pygame.draw.ellipse(s, c_preenchimento, (cx - 22, cy - 15, 44, 30))

        elif nome == "Lama":
            pygame.draw.circle(s, c_preenchimento, (cx - 10, cy - 5), 14)
            pygame.draw.circle(s, c_preenchimento, (cx + 10, cy + 5), 18)
            pygame.draw.circle(s, c_preenchimento, (cx, cy + 10), 12)

        # Rotacionar a imagem final
        s_rotacionada = pygame.transform.rotate(s, -angulo)
        rect_rot = s_rotacionada.get_rect(center=(x, y))
        superficie.blit(s_rotacionada, rect_rot.topleft)

class Item:
    def __init__(self, nome, e_ferramenta, pos_inicial, angulo_correto=0, slot_target=None):
        self.nome = nome
        self.e_ferramenta = e_ferramenta
        self.x, self.y = pos_inicial
        self.angulo = random.choice([0, 90, 180, 270]) if e_ferramenta else 0
        self.angulo_correto = angulo_correto
        self.slot_target = slot_target
        self.sendo_arrastado = False
        self.encaixado = False

    def get_rect(self):
        return pygame.Rect(self.x - 30, self.y - 30, 60, 60)

    def desenhar(self, superficie):
        DesenharObjeto.desenhar_item(superficie, self.nome, self.x, self.y, self.angulo, COR_ITEM)

# --- POSICIONAMENTO DOS SLOTS DENTRO DA CAIXA ---
caixa_rect = pygame.Rect(40, 60, 580, 500)

slots = [
    {"nome": "Martelo", "pos": (90, 150), "angulo": 0},
    {"nome": "Alicate", "pos": (180, 150), "angulo": 0},
    {"nome": "Foice", "pos": (280, 150), "angulo": 90},
    {"nome": "Chave", "pos": (380, 150), "angulo": 0},
    {"nome": "Óleo", "pos": (480, 150), "angulo": 0},
    
    {"nome": "Serrote", "pos": (130, 280), "angulo": 90},
    {"nome": "Trena", "pos": (270, 280), "angulo": 0},
    {"nome": "Pá", "pos": (370, 280), "angulo": 0},
    {"nome": "Picareta", "pos": (500, 280), "angulo": 90},

    {"nome": "Tesoura", "pos": (100, 420), "angulo": 0},
    {"nome": "Pregos", "pos": (220, 420), "angulo": 0},
    {"nome": "Engrenagem", "pos": (350, 420), "angulo": 0},
    {"nome": "Régua", "pos": (490, 420), "angulo": 90},
]

def inicializar_minigame():
    itens = []
    
    # 1. Ferramentas Válidas
    for slot in slots:
        pos_chao = (random.randint(650, 750), random.randint(100, 530))
        item = Item(
            nome=slot["nome"],
            e_ferramenta=True,
            pos_inicial=pos_chao,
            angulo_correto=slot["angulo"],
            slot_target=slot["pos"]
        )
        itens.append(item)

    # 2. Lista Expandida de Itens Inúteis
    lixos = ["Rato", "Ovo", "Tomate", "Ferradura", "Osso", "Lâmpada", "Maçã", "Pneu", "Garrafa", "Lápis", "Massa", "Lama"]
    for nome in lixos:
        pos_chao = (random.randint(650, 750), random.randint(100, 530))
        item = Item(
            nome=nome,
            e_ferramenta=False,
            pos_inicial=pos_chao
        )
        itens.append(item)

    return itens

def jogar(tela):

    imagem_fundo = pygame.image.load("fundodobau.png")
    imagem_fundo = pygame.transform.smoothscale(imagem_fundo, (900, 600))

    itens = inicializar_minigame()

    rodando = True
    vitoria = False
    game_over = False

    item_selecionado = None
    mensagem_erro = ""

    relogio = pygame.time.Clock()

    # --- LOOP PRINCIPAL ---
    while rodando:

        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():

            # Fechar o minigame
            if evento.type == pygame.QUIT:
                rodando = False

            # ESC = sair do minigame
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False

            # Enquanto o jogo não terminou
            if not game_over and not vitoria:

                # Selecionar item com clique esquerdo
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                    for item in reversed(itens):

                        if not item.encaixado and item.get_rect().collidepoint(pos_mouse):

                            item_selecionado = item
                            item.sendo_arrastado = True
                            break

                # Soltar item com clique esquerdo
                elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:

                    if item_selecionado:

                        # Só verifica erro se for solto dentro da caixa
                        if caixa_rect.collidepoint(
                            item_selecionado.x,
                            item_selecionado.y
                        ):

                            # 1. Tentou colocar lixo na caixa
                            if not item_selecionado.e_ferramenta:

                                game_over = True

                                mensagem_erro = (
                                    f"GAME OVER! O item "
                                    f"'{item_selecionado.nome}' "
                                    f"não pertence à caixa!"
                                )

                            else:

                                slot_colidido = None

                                for slot in slots:

                                    dist = math.hypot(
                                        item_selecionado.x - slot["pos"][0],
                                        item_selecionado.y - slot["pos"][1]
                                    )

                                    if dist < 45:
                                        slot_colidido = slot
                                        break

                                if slot_colidido:

                                    # 2. Slot correto
                                    if slot_colidido["nome"] == item_selecionado.nome:

                                        angulo_valido = (
                                            item_selecionado.nome == "Engrenagem"
                                            or
                                            item_selecionado.angulo ==
                                            item_selecionado.angulo_correto
                                            or
                                            (
                                                item_selecionado.nome == "Régua"
                                                and item_selecionado.angulo in [90, 270]
                                            )
                                        )

                                        if angulo_valido:

                                            item_selecionado.encaixado = True

                                            item_selecionado.x, item_selecionado.y = (
                                                slot_colidido["pos"]
                                            )

                                        else:

                                            # Ângulo incorreto
                                            game_over = True

                                            mensagem_erro = (
                                                f"GAME OVER! "
                                                f"{item_selecionado.nome} "
                                                f"tentou ser forçado no ângulo errado!"
                                            )

                                    else:

                                        # 3. Slot de outra ferramenta
                                        game_over = True

                                        mensagem_erro = (
                                            f"GAME OVER! Espaço incorreto "
                                            f"para {item_selecionado.nome}!"
                                        )

                        item_selecionado.sendo_arrastado = False
                        item_selecionado = None

                # Rotacionar item
                elif (
                    evento.type == pygame.MOUSEBUTTONDOWN
                    and evento.button == 3
                ) or (
                    evento.type == pygame.KEYDOWN
                    and evento.key == pygame.K_SPACE
                ):

                    if item_selecionado:

                        item_selecionado.angulo = (
                            item_selecionado.angulo + 90
                        ) % 360

            # Reiniciar depois de Game Over ou Vitória
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:

                itens = inicializar_minigame()

                game_over = False
                vitoria = False
                mensagem_erro = ""
                item_selecionado = None

        # Atualizar posição do item arrastado
        if item_selecionado and item_selecionado.sendo_arrastado:

            item_selecionado.x, item_selecionado.y = pos_mouse

        # Checar vitória
        ferramentas = [
            i for i in itens
            if i.e_ferramenta
        ]

        if (
            not game_over
            and len(ferramentas) > 0
            and all(item.encaixado for item in ferramentas)
        ):

            vitoria = True

        # -------------------------------------------------
        # DESENHO / RENDERIZAÇÃO
        # -------------------------------------------------

        tela.blit(imagem_fundo, (-50, 0))

        # Caixa de ferramentas
        pygame.draw.rect(
            tela,
            COR_CAIXA,
            caixa_rect,
            border_radius=12
        )

        pygame.draw.rect(
            tela,
            (100, 100, 110),
            caixa_rect,
            width=4,
            border_radius=12
        )

        txt_caixa = fonte_ui.render(
            "Caixa de Ferramentas",
            True,
            COR_TEXTO
        )

        tela.blit(txt_caixa, (230, 80))

        # Moldes / silhuetas
        for slot in slots:

            DesenharObjeto.desenhar_item(
                tela,
                slot["nome"],
                slot["pos"][0],
                slot["pos"][1],
                slot["angulo"],
                COR_SILHUETA,
                e_silhueta=True
            )

        # Desenhar itens
        for item in itens:

            if not item.sendo_arrastado:
                item.desenhar(tela)

        # Desenhar item selecionado por último
        if item_selecionado:

            item_selecionado.desenhar(tela)

        # Instruções
        txt_instrucao = fonte_ui.render(
            "Clique Esquerdo: Arrastar | "
            "Botão Direito / Espaço: Rotacionar 90°",
            True,
            COR_TEXTO
        )

        tela.blit(txt_instrucao, (20, 570))

        # -------------------------------------------------
        # GAME OVER
        # -------------------------------------------------

        if game_over:

            s_overlay = pygame.Surface(
                (LARGURA, ALTURA),
                pygame.SRCALPHA
            )

            s_overlay.fill((0, 0, 0, 200))

            tela.blit(
                s_overlay,
                (0, 0)
            )

            txt_go = fonte_titulo.render(
                "GAME OVER",
                True,
                (255, 80, 80)
            )

            txt_msg = fonte_ui.render(
                mensagem_erro,
                True,
                COR_TEXTO
            )

            txt_rst = fonte_ui.render(
                "Pressione 'R' para tentar novamente",
                True,
                (200, 200, 200)
            )

            tela.blit(
                txt_go,
                txt_go.get_rect(
                    center=(LARGURA // 2, ALTURA // 2 - 40)
                )
            )

            tela.blit(
                txt_msg,
                txt_msg.get_rect(
                    center=(LARGURA // 2, ALTURA // 2 + 10)
                )
            )

            tela.blit(
                txt_rst,
                txt_rst.get_rect(
                    center=(LARGURA // 2, ALTURA // 2 + 50)
                )
            )

        # -------------------------------------------------
        # VITÓRIA
        # -------------------------------------------------

        elif vitoria:

            s_overlay = pygame.Surface(
                (LARGURA, ALTURA),
                pygame.SRCALPHA
            )

            s_overlay.fill((0, 0, 0, 180))

            tela.blit(
                s_overlay,
                (0, 0)
            )

            txt_vit = fonte_titulo.render(
                "Caixa Totalmente Organizada!",
                True,
                (100, 255, 100)
            )

            txt_rst = fonte_ui.render(
                "Pressione 'R' para jogar novamente",
                True,
                COR_TEXTO
            )

            tela.blit(
                txt_vit,
                txt_vit.get_rect(
                    center=(LARGURA // 2, ALTURA // 2 - 20)
                )
            )

            tela.blit(
                txt_rst,
                txt_rst.get_rect(
                    center=(LARGURA // 2, ALTURA // 2 + 30)
                )
            )

        # Atualizar a tela
        pygame.display.flip()

        # Limitar a 60 FPS
        relogio.tick(60)

    return "sair"