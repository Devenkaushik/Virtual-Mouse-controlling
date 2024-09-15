# AI Virtual Mouse

An AI-based Virtual Mouse project that uses **Python**, **OpenCV**, and **Hand Tracking** to enable users to control their computer mouse through hand gestures. This system eliminates the need for traditional hardware devices, offering a hands-free experience for controlling the cursor and performing various mouse actions.

## Features

- **Hand Gesture Detection:** Uses OpenCV and Hand Tracking to detect hand gestures.
- **Cursor Control:** Move the cursor by moving your hand.
- **Left Click and Right Click:** Perform mouse clicks using specific hand gestures.
- **Drag and Drop:** Execute the drag-and-drop action.
- **Scrolling:** Scroll up and down using hand gestures.
- **Zoom In/Out:** Control zoom functionality using full hand gestures.
  
## Technology Stack

- **Python:** Programming language used for implementation.
- **OpenCV:** Open-source computer vision library for capturing and processing video.
- **Mediapipe:** Used for detecting and tracking hands in real-time.
- **PyAutoGUI:** Python module used for controlling the mouse and keyboard operations.

## Prerequisites

Make sure you have Python installed on your machine. You can download Python from [here](https://www.python.org/downloads/).

### Install the required packages:

```bash
pip install opencv-python
pip install mediapipe
pip install pyautogui
```

## How to Run the Project

1. Clone this repository or download the code.
2. Install the required packages mentioned above.
3. Run the Python file.

```bash
    mouse.py
```

4. Make sure your webcam is working as it will be used for hand detection.

## Hand Gestures

- **Move Mouse:** Move the hand to control the mouse pointer.
- **Left Click:** Pinch your index finger and thumb together.
- **Right Click:** Pinch your middle finger and thumb together.
- **Scroll Up/Down:** Use a hand gesture to scroll the page.
- **Zoom In/Out:** Use a full hand gesture to control zoom.

## Issues Faced

- **Fast Zoom Out:** There was an issue where the zoom-out action was too fast, and the scroll-up feature was missing. These issues have been fixed by fine-tuning gesture detection and the PyAutoGUI scroll functionality.

## Future Improvements

- Enhance gesture recognition for more accurate control.
- Add support for more mouse actions like double-click, middle-click, etc.
- Optimize performance for better response time and smoother interaction.


## Contributions

Feel free to fork this repository and contribute. If you have suggestions or issues, you can report them by opening a new issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This content provides a clear structure for your project and helps others understand its purpose, features, and how to use it. Let me know if you'd like to modify or add more details!
