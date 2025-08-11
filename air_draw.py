import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

# Configurations
W, H = 640, 480
CANVAS_COLOR = (0, 0, 0)  # Black background by default
PEN_COLOR = (0, 255, 0)   # Default pen color: Green
PEN_THICKNESS = 5
MAX_PEN_THICKNESS = 20
MIN_PEN_THICKNESS = 1

# Pen and background color options
PEN_COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 255), (255, 255, 255)]  # Green, Red, Blue, Yellow, White
PEN_NAMES = ["Green", "Red", "Blue", "Yellow", "White"]

BG_COLORS = [(0, 0, 0), (0, 0, 255), (0, 255, 255), (255, 255, 255), (128, 128, 128)]  # Black, Red, Yellow, White, Gray
BG_NAMES = ["Black", "Red", "Yellow", "White", "Gray"]

# Menu position configurations
MENU_Y = H - 60
BUTTON_W, BUTTON_H = 50, 50
SIDE_MARGIN = 10
TOP_MARGIN = 10
BOTTOM_MARGIN = 60

# Generate button positions for pen colors (left sidebar)
def vertical_positions(count, height, margin_top, margin_bottom):
    space = height - margin_top - margin_bottom
    gap = space // (count + 1)
    return [margin_top + gap * (i + 1) for i in range(count)]

pen_buttons_y = vertical_positions(len(PEN_COLORS), H, TOP_MARGIN, BOTTOM_MARGIN)
bg_buttons_y = vertical_positions(len(BG_COLORS), H, TOP_MARGIN, BOTTOM_MARGIN)

PEN_BOXES = [(SIDE_MARGIN, y, BUTTON_W, BUTTON_H) for y in pen_buttons_y]
BG_BOXES = [(W - SIDE_MARGIN - BUTTON_W, y, BUTTON_W, BUTTON_H) for y in bg_buttons_y]

# Pen thickness controls at top center
THICKNESS_LABEL_POS = (W // 2 - 40, TOP_MARGIN + 35)
THICKNESS_MINUS_POS = (W // 2 - 90, TOP_MARGIN)
THICKNESS_PLUS_POS = (W // 2 + 50, TOP_MARGIN)

SAVE_BOX = (W // 2 - BUTTON_W - 10, H - BUTTON_H - 10, BUTTON_W, BUTTON_H)
CLEAR_BOX = (W // 2 + 10, H - BUTTON_H - 10, BUTTON_W, BUTTON_H)

# Initialize canvas
canvas = np.zeros((H, W, 3), dtype=np.uint8)
canvas[:] = CANVAS_COLOR

# Initialize webcam capture
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

prev_x, prev_y = 0, 0
show_menu = False
frame_count_menu = 0

def dist(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def is_pinch(pts, threshold=40):
    return dist(pts['index'], pts['thumb']) < threshold

def point_in_box(pt, box):  # box = (x, y, w, h)
    x, y = pt
    bx, by, bw, bh = box
    return bx <= x <= bx + bw and by <= y <= by + bh

def draw_buttons(frame):
    # Draw Pen color buttons (left sidebar)
    for i, (x, y, w, h) in enumerate(PEN_BOXES):
        cv2.rectangle(frame, (x, y), (x + w, y + h), PEN_COLORS[i], -1)
        border_color = (255, 255, 255) if PEN_COLOR == PEN_COLORS[i] else (100, 100, 100)
        cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, 2)
        cv2.putText(frame, PEN_NAMES[i], (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Draw Background color buttons (right sidebar)
    for i, (x, y, w, h) in enumerate(BG_BOXES):
        cv2.rectangle(frame, (x, y), (x + w, y + h), BG_COLORS[i], -1)
        border_color = (255, 255, 255) if CANVAS_COLOR == BG_COLORS[i] else (100, 100, 100)
        cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, 2)
        cv2.putText(frame, BG_NAMES[i], (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Draw Pen thickness buttons (+ and -) at top center
    # Minus button
    cv2.rectangle(frame, (THICKNESS_MINUS_POS[0], THICKNESS_MINUS_POS[1]),
                  (THICKNESS_MINUS_POS[0] + 40, THICKNESS_MINUS_POS[1] + 40), (50, 50, 50), -1)
    cv2.putText(frame, "-", (THICKNESS_MINUS_POS[0] + 12, THICKNESS_MINUS_POS[1] + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # Plus button
    cv2.rectangle(frame, (THICKNESS_PLUS_POS[0], THICKNESS_PLUS_POS[1]),
                  (THICKNESS_PLUS_POS[0] + 40, THICKNESS_PLUS_POS[1] + 40), (50, 50, 50), -1)
    cv2.putText(frame, "+", (THICKNESS_PLUS_POS[0] + 12, THICKNESS_PLUS_POS[1] + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Pen thickness label
    cv2.putText(frame, f"Thickness: {PEN_THICKNESS}", THICKNESS_LABEL_POS, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # Draw Save button (bottom center)
    # Save button (bottom center left)
    sx, sy, sw, sh = SAVE_BOX
    cv2.rectangle(frame, (sx, sy), (sx + sw, sy + sh), (0, 128, 255), -1)
    cv2.rectangle(frame, (sx, sy), (sx + sw, sy + sh), (20, 60, 255), 2)
    cv2.putText(frame, "SAVE", (sx + 20, sy + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)  # Smaller text, centered better

    # Clear button (bottom center right)
    cx, cy, cw, ch = CLEAR_BOX
    cv2.rectangle(frame, (cx, cy), (cx + cw, cy + ch), (100, 100, 100), -1)
    cv2.putText(frame, "CLEAR", (cx + 12, cy + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)  # Smaller text, centered better

def save_canvas(canvas):
    filename = f"AirDraw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    cv2.imwrite(filename, canvas)
    print(f"Saved as {filename}")


def fingers_up_status(lm):
    # Check thumb, index and middle fingers are up or not
    tips = [4, 8, 12, 16, 20]
    pips = [3, 6, 10, 14, 18]
    return [lm[tip].y < lm[pip].y for tip, pip in zip(tips, pips)]


try:
    with mp_hands.Hands(
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
        max_num_hands=1
    ) as hands:

        cv2.namedWindow("AirDraw (press Q to quit)", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("AirDraw (press Q to quit)", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (W, H))
            frame = cv2.flip(frame, 1)
            cam_display = frame.copy()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                lm = hand.landmark
                index_tip = (int(lm[8].x * W), int(lm[8].y * H))
                thumb_tip = (int(lm[4].x * W), int(lm[4].y * H))

                # Visual circle at index fingertip with current pen color
                cv2.circle(cam_display, index_tip, 13, PEN_COLOR, 4)
                cv2.circle(cam_display, thumb_tip, 13, (255, 0, 0), 4)  # Show thumb tip as well

                fingers = fingers_up_status(lm)
                thumb_up, index_up, middle_up, ring_up, pinky_up = fingers
                all_fingers_up = all(fingers)

                pen_lift = all_fingers_up  # Lift pen when all fingers and palm are open

                # Pinch detection: thumb and index close
                if is_pinch({'index': index_tip, 'thumb': thumb_tip}):
                    show_menu = True
                    frame_count_menu = 0
                    draw_buttons(cam_display)

                    # Pen color selection on left sidebar
                    for i, box in enumerate(PEN_BOXES):
                        if point_in_box(index_tip, box):
                            PEN_COLOR = PEN_COLORS[i]

                    # Background color selection on right sidebar
                    for i, box in enumerate(BG_BOXES):
                        if point_in_box(index_tip, box):
                            CANVAS_COLOR = BG_COLORS[i]
                            canvas[:] = CANVAS_COLOR

                    # Pen Thickness + and - buttons at top center
                    plus_button = (THICKNESS_PLUS_POS[0], THICKNESS_PLUS_POS[1], 40, 40)
                    minus_button = (THICKNESS_MINUS_POS[0], THICKNESS_MINUS_POS[1], 40, 40)
                    if point_in_box(index_tip, plus_button):
                        PEN_THICKNESS = min(PEN_THICKNESS + 1, MAX_PEN_THICKNESS)
                    elif point_in_box(index_tip, minus_button):
                        PEN_THICKNESS = max(PEN_THICKNESS - 1, MIN_PEN_THICKNESS)

                    # Save button
                    if point_in_box(index_tip, SAVE_BOX):
                        save_canvas(canvas)

                    # Clear button
                    if point_in_box(index_tip, CLEAR_BOX):
                        canvas[:] = CANVAS_COLOR

                    prev_x, prev_y = 0, 0  # Reset previous points while selecting

                else:
                    draw = not pen_lift
                    if draw:
                        if prev_x == 0 and prev_y == 0:
                            prev_x, prev_y = index_tip
                        cv2.line(canvas, (prev_x, prev_y), index_tip, PEN_COLOR, PEN_THICKNESS)
                        prev_x, prev_y = index_tip
                    else:
                        prev_x, prev_y = 0, 0

                mp_drawing.draw_landmarks(cam_display, hand, mp_hands.HAND_CONNECTIONS)

            else:
                prev_x, prev_y = 0, 0
                show_menu = False

            if show_menu:
                draw_buttons(cam_display)
                frame_count_menu += 1
                if frame_count_menu > 30:
                    show_menu = False

            out = cv2.addWeighted(cam_display, 0.7, canvas, 0.9, 0)
            cv2.imshow("AirDraw (press Q to quit)", out)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('c'):
                canvas[:] = CANVAS_COLOR

finally:
    cap.release()
    cv2.destroyAllWindows()
