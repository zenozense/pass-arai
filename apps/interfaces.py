import tkinter as tk

window = tk.Tk()
window.title("PASS ARAI")

def handle_button_press(event):
    print("Button pressed")

button = tk.Button(text="ลองกดดู")
button.bind("<Button-1>", handle_button_press)
button.pack()

window.mainloop()