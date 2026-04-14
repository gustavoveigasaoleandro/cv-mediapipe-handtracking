import cv2
import mediapipe as mp
import os
from time import sleep
from pynput.keyboard import Controller
import numpy as np

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (255, 0, 0)
VERMELHO = (0, 0, 255)
AZUL_CLARO = (255, 255, 0)


mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

# Inicializa o MediaPipe Hands
maos = mp_maos.Hands(
    max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
camera = cv2.VideoCapture(0)
resolution = (1280, 720)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
bloco_notas = False
chrome = False
calculadora = False
teclas = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
          ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
          ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', ' ']]

offset = 50
contador = 0
texto = '>'
teclado = Controller()
img_quadro = np.ones((resolution[1], resolution[0], 3), np.uint8) * 255
cor_pincel = (255, 0, 0)
espessura_pincel = 20
x_quadro, y_quadro = 0, 0


def imprimir_botoes(img, posicao, letra, tamanho=50, cor_retangulo=BRANCO, cor_texto=PRETO):
    x, y = posicao
    cv2.rectangle(img, (x, y), (x + tamanho, y + tamanho),
                  cor_retangulo, cv2.FILLED)
    cv2.rectangle(img, (x, y), (x + tamanho, y + tamanho), AZUL, 1)
    cv2.putText(img, letra, (x + 15, y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, cor_texto, 2)
    return img


def encontrar_maos(img, lado_invertido=False):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    resultado = maos.process(img)
    todas_maos = []
    if resultado.multi_hand_landmarks:
        for lado_mao, marcacao_maos in zip(resultado.multi_handedness, resultado.multi_hand_landmarks):
            info_maos = {}
            cordenadas = []
            for marcacao in marcacao_maos.landmark:
                # Converte as coordenadas normalizadas para pixels
                h, w, c = img.shape
                cx, cy, cz = int(
                    marcacao.x * w), int(marcacao.y * h), int(marcacao.z * w)
                cordenadas.append((cx, cy, cz))

            info_maos['coordenadas'] = cordenadas

            if lado_invertido:
                if lado_mao.classification[0].label == "Left":
                    info_maos['lado'] = "Right"
                else:
                    info_maos['lado'] = "Left"
            else:
                info_maos['lado'] = lado_mao.classification[0].label

            todas_maos.append(info_maos)
            mp_desenho.draw_landmarks(
                img, marcacao_maos, mp_maos.HAND_CONNECTIONS)

    return img, todas_maos


def dedos_levantados(mao):
    mao_dedos = []
    dedos = [8, 12, 16, 20]
    for i in dedos:
        if mao['coordenadas'][i][1] < mao['coordenadas'][i-2][1]:
            mao_dedos.append(True)
        else:
            mao_dedos.append(False)
    return mao_dedos


while True:
    sucesso, img = camera.read()
    if not sucesso or img is None:
        print("Erro: Não foi possível capturar a imagem da câmera.")
        break
    img = cv2.flip(img, 1)

    img, todas_maos = encontrar_maos(img)

    if len(todas_maos) == 1:
        if len(todas_maos[0]['coordenadas']) >= 21:
            info_dedos_mao1 = dedos_levantados(todas_maos[0])
            print("Mão 1:", info_dedos_mao1)
            if todas_maos[0]['lado'] == "Left":
                indicador_x, indicador_y, indicador_z = todas_maos[0]['coordenadas'][8]
                cv2.putText(img, f'Distancia camera: {indicador_z}', (
                    850, 50), cv2.FONT_HERSHEY_COMPLEX, 1, BRANCO, 2)
                for i_linha, linha_teclado in enumerate(teclas):
                    for indice, letra in enumerate(linha_teclado):
                        if sum(info_dedos_mao1) <= 1:
                            letra = letra.lower()
                        img = imprimir_botoes(
                            img, (offset+indice*80, offset+i_linha*80), letra)
                        if offset+indice*80 < indicador_x < offset+indice*80 + 50 and offset+i_linha*80 < indicador_y < offset+i_linha*80 + 50:
                            img = imprimir_botoes(
                                img, (offset+indice*80, offset+i_linha*80), letra, cor_retangulo=VERDE)
                            if indicador_z < -85:
                                contador = 1
                                escreve = letra
                                img = imprimir_botoes(
                                    img, (offset+indice*80, offset+i_linha*80), letra, cor_retangulo=AZUL_CLARO)

                if contador:
                    contador += 1

                    if contador == 3:
                        texto += escreve
                        contador = 0
                        teclado.press(escreve)
                cv2.rectangle(img, (offset, 450),
                              (830, 500), BRANCO, cv2.FILLED)
                cv2.rectangle(img, (offset, 450), (830, 500), AZUL, 1)
                cv2.putText(img, texto[-40:], (offset+10, 470),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, PRETO, 2)
                cv2.circle(img, (indicador_x, indicador_y),
                           7, AZUL, cv2.FILLED)

                if info_dedos_mao1 == [False, False, False, True] and len(texto) > 1:
                    texto = texto[:-1]
                    sleep(0.2)

            if todas_maos[0]['lado'] == "Right":
                if info_dedos_mao1 == [True, False, False, False] and bloco_notas == False:
                    bloco_notas = True
                    os.system("open /System/Applications/Notes.app")
                elif info_dedos_mao1 == [True, True, False, False] and chrome == False:
                    print("abrindo chrome")
                    chrome = True
                    os.system("open /Applications/Google\\ Chrome.app")
                elif info_dedos_mao1 == [True, True, True, False] and calculadora == False:
                    calculadora = True
                    os.system("open /System/Applications/Calculator.app")
                if info_dedos_mao1 == [False, False, False, False] and bloco_notas == True:
                    bloco_notas = False
                    os.system('killall Notes')
                if info_dedos_mao1 == [True, False, False, True] and chrome == True:
                    break
    if len(todas_maos) == 2:
        info_dedos_mao1 = dedos_levantados(todas_maos[0])
        info_dedos_mao2 = dedos_levantados(todas_maos[1])
        indicador_x, indicador_y, indicador_z = todas_maos[0]['coordenadas'][8]

        if sum(info_dedos_mao2) == 1:
            cor_pincel = AZUL
        elif sum(info_dedos_mao2) == 2:
            cor_pincel = VERDE
        elif sum(info_dedos_mao2) == 3:
            cor_pincel = VERMELHO
        elif sum(info_dedos_mao2) == 4:
            cor_pincel = BRANCO
        else:
            img_quadro = np.ones(
                (resolution[1], resolution[0], 3), np.uint8) * 255

        espessura_pincel = abs(indicador_z) // 3+5

        cv2.circle(img, (indicador_x, indicador_y),
                   espessura_pincel, cor_pincel, cv2.FILLED)

        if info_dedos_mao1 == [True, False, False, False]:
            if x_quadro == 0 and y_quadro == 0:
                x_quadro, y_quadro = indicador_x, indicador_y

            cv2.line(img_quadro, (x_quadro, y_quadro),
                     (indicador_x, indicador_y), cor_pincel, espessura_pincel)

            x_quadro, y_quadro = indicador_x, indicador_y
        else:
            x_quadro, y_quadro = 0, 0

        img = cv2.addWeighted(img, 1, img_quadro, 0.2, 0)
    cv2.imshow("Camera", img)
    cv2.imshow("Quadro", img_quadro)
    tecla = cv2.waitKey(1)
    if tecla == 27:  # ESC
        break

with open("texto.txt", "w") as arquivo:
    arquivo.write(texto)


cv2.imwrite("quadro.png", img_quadro)
