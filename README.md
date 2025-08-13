# AirDraw: Draw in Air with Hand Gestures

**AirDraw** is a Python application that lets you draw on a virtual canvas using hand gestures tracked via your webcam. It uses MediaPipe for real-time hand tracking and OpenCV for visualization and menu controls. You can select pen color, background color, adjust pen thickness, save your work, and clear the canvas—all through intuitive in-video gestures.

---

## Features

- Draw by moving your index finger in the air.
- Pen lifts (stops drawing) when your whole palm is open.
- Select pen colors from the left sidebar using pinch and point gestures.
- Select background colors from the right sidebar.
- Adjust pen thickness at the top using "+" and "−" buttons.
- Save your drawing or clear the canvas using bottom center buttons.
- Visual fingertip pointer matching your selected pen color.
- Simple keyboard controls: press `c` to clear, `q` to quit.

---

## Installation

1. Clone this repository:git clone https://github.com/Yaseen2112/airdraw.git
    cd airdraw

2. Install dependencies:
pip install -r requirements.txt


---

## Usage

Start the app:
python air_draw.py



**Controls:**
- **Draw**: Raise only your index finger to draw.
- **Lift Pen**: Open your whole palm (all fingers extended).
- **Menu Interaction**: Pinch gesture (touch thumb and index fingertips) and point to select pen/background colors, thickness, save, or clear.
- **Clear Canvas**: Press `c` on your keyboard.
- **Quit**: Press `q` on your keyboard.

---

## Troubleshooting

- Make sure your webcam is plugged in and functioning.
- If hand tracking doesn't work, ensure MediaPipe and OpenCV are installed.
- Use in good lighting for best results.
- The app tracks one hand at a time.

---

## Author

**Shaik Yaseen**
- Email: skyaseen2112@gmail.com
- Phone: 9704330969
- GitHub: [Yaseen2112](https://github.com/Yaseen2112)

---

## License

MIT License

---

## Acknowledgements

- [MediaPipe](https://mediapipe.dev/)
- [OpenCV](https://opencv.org/)

---

Feel free to reach out for feedback, custom features, or collaboration!

