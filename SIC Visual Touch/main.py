import cv2
import mediapipe as mp
import pyautogui

# Inicializar a câmera
cam = cv2.VideoCapture(0)
# O cv2.VideoCapture(0) inicializa a câmera conectada ao computador. O parâmetro 0 indica que estamos usando a câmera padrão (geralmente a webcam do laptop).

# Inicializar o modelo FaceMesh do Mediapipe
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
# O FaceMesh é um modelo do Mediapipe que detecta e rastreia os pontos faciais. 'refine_landmarks=True' melhora a precisão dos pontos faciais detectados.

# Obter a largura e altura da tela usando PyAutoGUI
screen_w, screen_h = pyautogui.size()
# PyAutoGUI é usado para obter a resolução da tela (largura e altura). Esses valores serão usados para mover o cursor na tela.

# Obter a largura e altura do frame da câmera
frame_h, frame_w = None, None
# Inicializa as variáveis de altura e largura do frame como None. Esses valores serão definidos na primeira leitura do frame da câmera.

while True:
    # Ler um frame da câmera
    _, frame = cam.read()
    # O método cam.read() captura um frame da câmera. A variável '_' é ignorada, e 'frame' contém a imagem capturada.

    # Inicializar frame_h e frame_w
    if frame_h is None or frame_w is None:
        frame_h, frame_w, _ = frame.shape
        # Se frame_h e frame_w ainda não foram definidos, inicializa com as dimensões do frame capturado. frame.shape fornece a altura, largura e número de canais da imagem.

    # Espelhar o frame horizontalmente
    frame = cv2.flip(frame, 1)
    # cv2.flip(frame, 1) espelha a imagem horizontalmente. Isso é feito para criar uma visualização mais natural, como em um espelho.

    # Converter o frame de BGR para RGB (necessário pelo Mediapipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # O Mediapipe requer imagens no formato RGB. cv2.cvtColor converte a imagem de BGR (padrão do OpenCV) para RGB.

    # Processar o frame RGB usando o modelo FaceMesh para detectar pontos faciais
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    # O método face_mesh.process() processa o frame e detecta os pontos faciais. 'output.multi_face_landmarks' contém os pontos faciais detectados para cada rosto na imagem.

    if landmark_points:
        # Obter os pontos faciais do primeiro rosto detectado
        landmarks = landmark_points[0].landmark
        # Se pontos faciais foram detectados, 'landmarks' contém as coordenadas dos pontos faciais para o primeiro rosto.

        # Obter landmarks dos cantos dos olhos (por exemplo, 133 e 362 para o olho esquerdo)
        eye_landmarks = [landmarks[133], landmarks[362]]
        # 'eye_landmarks' armazena os pontos dos cantos dos olhos. Os índices 133 e 362 representam pontos específicos para o olho esquerdo.

        # Desenhar círculos vermelhos ao redor dos landmarks dos olhos
        for landmark in eye_landmarks:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 0, 255))  # Desenhar círculo vermelho
            # cv2.circle desenha um círculo vermelho (0, 0, 255) ao redor de cada ponto dos olhos. 'x' e 'y' são as coordenadas na imagem.

        # Calcular a posição média dos landmarks dos olhos
        eye_x = int((eye_landmarks[0].x + eye_landmarks[1].x) * frame_w / 2)
        eye_y = int((eye_landmarks[0].y + eye_landmarks[1].y) * frame_h / 2)
        # A posição média dos pontos dos olhos é calculada para determinar o ponto central dos olhos. Isso é usado para mover o cursor.

        # Calcular a posição do cursor com base na posição dos olhos
        screen_x = screen_w * (eye_x / frame_w)
        screen_y = screen_h * (eye_y / frame_h)
        # Converte as coordenadas dos olhos para as coordenadas da tela. 'screen_x' e 'screen_y' são as posições onde o cursor será movido.

        # Mover o cursor para a nova posição
        pyautogui.moveTo(screen_x, screen_y)
        # pyautogui.moveTo() move o cursor do mouse para as coordenadas calculadas na tela.

    # Mostrar o frame com os landmarks desenhados
    cv2.imshow('Eye Controlled Mouse', frame)
    # cv2.imshow() exibe a imagem com os pontos faciais desenhados na janela chamada 'Eye Controlled Mouse'.

    # Obter os landmarks correspondentes ao olho esquerdo (landmarks 145 e 159)
    left = [landmarks[145], landmarks[159]]
    # 'left' armazena os pontos do olho esquerdo usados para detectar o piscar.

    # Desenhar círculos cianos ao redor dos landmarks do olho esquerdo
    for landmark in left:
        x = int(landmark.x * frame_w)
        y = int(landmark.y * frame_h)
        cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)
        # cv2.circle desenha círculos cianos (0, 255, 255) ao redor dos pontos do olho esquerdo. '-1' preenche o círculo.

    # Verificar se o usuário pisca o olho esquerdo (diferença na coordenada y é pequena)
    if (left[0].y - left[1].y) < 0.004:
        pyautogui.click()
        pyautogui.sleep(1)
        # Compara a diferença nacoordenada y dos pontos do olho esquerdo para verificar se o olho está piscando. Se a diferença for pequena, simula um clique e espera 1 segundo para evitar múltiplos cliques.

    # Mostrar o frame com os landmarks desenhados
    cv2.imshow('Eye Controlled Mouse', frame)

    # Esperar um evento de pressionamento de tecla com um atraso de 1 milissegundo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Sair do loop se a tecla 'q' for pressionada
        # cv2.waitKey(1) espera por um evento de tecla. Se a tecla 'q' for pressionada, o loop é encerrado.

# Liberar a câmera e fechar todas as janelas do OpenCV
cam.release()
cv2.destroyAllWindows()
# Libera a câmera e fecha todas as janelas do OpenCV após o término do loop.
