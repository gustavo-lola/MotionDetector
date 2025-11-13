import cv2
import numpy as np
import time

CAM_INDEX = 0
BLUR_KSIZE = 21
THRESH_BIN = 25
DILATE_ITERS = 2
AREA_MIN = 5000
ALPHA_BG = 0.05
ROI_RATIO = 0.85
FPS_SMOOTH = 0.9

cap = cv2.VideoCapture(CAM_INDEX)
if not cap.isOpened():
    raise RuntimeError(f"Nao foi possivel abrir a camera {CAM_INDEX}. Tente novamente.")

time.sleep(0.5)
ret, frame = cap.read()
if not ret:
    cap.release()
    raise RuntimeError("Falha ao ler o primeiro frame")

gray0 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray0 = cv2.GaussianBlur(gray0, (BLUR_KSIZE, BLUR_KSIZE), 0)
bg = gray0.astype("float")

h, w = gray0.shape
roi_w = int(w * ROI_RATIO)
roi_h = int(h * ROI_RATIO)

x0 = (w - roi_w) // 2
y0 = (h - roi_h) // 2
x1 = x0 + roi_w
y1 = y0 + roi_h

ultimo_estado_mov = None
ultimo_print = time.time()
fps = 0.0
t_prev = time.time()

print("Sistema iniciado, observando a camera... (q para sair)")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        t_now = time.time()
        dt = t_now - t_prev
        t_prev = t_now
        fps = FPS_SMOOTH * fps + (1 - FPS_SMOOTH) * (1.0 / dt if dt > 0 else 0)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (BLUR_KSIZE, BLUR_KSIZE), 0)

        gray_roi = gray[y0:y1, x0:x1]

        cv2.accumulateWeighted(gray_roi, bg[y0:y1, x0:x1], ALPHA_BG)

        diff = cv2.absdiff(gray_roi, cv2.convertScaleAbs(bg[y0:y1, x0:x1]))

        _, thresh = cv2.threshold(diff, THRESH_BIN, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=DILATE_ITERS)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        area_total = 0
        for c in contours:
            area = cv2.contourArea(c)
            if area < AREA_MIN:
                continue
            area_total += area

            (x, y, w_box, h_box) = cv2.boundingRect(c)
            cv2.rectangle(
                frame,
                (x0 + x, y0 + y),
                (x0 + x + w_box, y0 + y + h_box),
                (0, 255, 0),
                2,
            )

        movimento = area_total >= AREA_MIN

        cv2.rectangle(frame, (x0, y0), (x1, y1), (255, 0, 0), 1)

        status_text = "MOVIMENTO" if movimento else "SEM MOVIMENTO"
        color = (0, 0, 255) if movimento else (200, 200, 200)
        cv2.putText(
            frame,
            f"{status_text} | FPS: {fps:0.1f}",
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2,
        )

        cv2.imshow("Detector de Movimento (Webcam)", frame)

        if ultimo_estado_mov is None or movimento != ultimo_estado_mov:
            print(">>", status_text)
            ultimo_estado_mov = movimento
            ultimo_print = time.time()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
