import tkinter as tk

def main():
    window = tk.Tk()
    window.title("Nexusbyte Ticketing App")
    window.geometry("400x300")
    
    label = tk.Label(window, text="Welcome to Nexusbyte Ticketing App!", font=("Arial", 14))
    label.pack(pady=20)
    
    window.mainloop()

if __name__ == "__main__":
    main()
