# Detector de Movimento com OpenCV (Webcam / Raspberry Pi)

Este projeto implementa um detector de movimento em tempo real usando Python e OpenCV, pensado para rodar em computadores ou em um Raspberry Pi com câmera USB ou câmera nativa.

O script captura os frames da câmera, aplica suavização, subtração de fundo e limiarização, detecta contornos de movimento dentro de uma região de interesse (ROI) e exibe o vídeo com as caixas delimitando as áreas em movimento.  
Também mostra o FPS e imprime no terminal quando o estado muda entre “MOVIMENTO” e “SEM MOVIMENTO”.

---

## Funcionalidades

- Captura de vídeo em tempo real da webcam (`CAM_INDEX` configurável).
- Uso de background dinâmico com `cv2.accumulateWeighted`.
- Detecção de movimento apenas dentro de uma região central da imagem (ROI).
- Desenho de:
  - Caixa azul da ROI.
  - Caixas verdes nas regiões com movimento detectado.
- Exibição de status textual na tela:
  - MOVIMENTO (vermelho)
  - SEM MOVIMENTO (cinza)
- Cálculo e exibição de FPS suavizado.
- Log no terminal sempre que o estado muda.
- Encerramento com a tecla `q`.

---

## Tecnologias utilizadas

- Python 3  
- OpenCV (`opencv-python`)  
- NumPy  
- Biblioteca padrão `time`

---

## Pré-requisitos

- Python 3 instalado  
- Webcam funcionando  
- Dependências instaladas:
  - `opencv-python`
  - `numpy`

---

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   

python3 -m venv venv

source venv/bin/activate   # Linux / macOS

pip install opencv-python numpy

python detector_movimento.py



