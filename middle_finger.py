import cv2

def displayMiddleFingerMessage(img):
    """
    Displays a fun 'Middle Finger' message with multiple emojis on the screen.
    Args:
        img: Frame captured from the webcam where the message will appear.
    """
    h, w, _ = img.shape
    font_scale = 1.2
    font_color = (0, 0, 255)  # Red
    font_thickness = 2

    # Main message
    message = "Middle finger to you!"
    cv2.putText(img, message, (int(w / 6), int(h / 2 - 50)), cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, font_color, font_thickness)

    # Angry emojis block
    angry_emojis = "😡 🤬 🤯 😤 😠 💥 👊"
    cv2.putText(img, angry_emojis, (int(w / 6), int(h / 2 + 10)), cv2.FONT_HERSHEY_SIMPLEX,
                font_scale, font_color, font_thickness)
