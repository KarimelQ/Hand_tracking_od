import tkinter as tk

class GestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand tracking")
        self.root.geometry("800x600")
        self.canvas = tk.Canvas(root, width=800, height=600, bg="black")
        self.canvas.pack()

    def update_hand_position(self, x,y):
        self.canvas.delete("all")
        self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="white")  # Adjust the size of the oval as needed
