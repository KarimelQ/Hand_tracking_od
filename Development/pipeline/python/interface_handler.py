import tkinter as tk

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gesture Detection")
        self.root.geometry("800x600")
        self.gesture_label = tk.Label(root, text="Gesture ", font=("Helvetica", 24))
        self.gesture_label.pack(fill=tk.BOTH, expand=True)

    def update_gesture_label(self, gesture_text):
        self.gesture_label.config(text=gesture_text)