import tkinter as tk
import time

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Cronometru")
        
        self.time_label = tk.Label(root, text="00:00:00", font=("Helvetica", 48))
        self.time_label.pack()

        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 24), command=self.start)
        self.start_button.pack(side="left", padx=20, pady=20)

        self.pause_button = tk.Button(root, text="Pause", font=("Helvetica", 24), command=self.pause_continue, state=tk.DISABLED)
        self.pause_button.pack(side="left", padx=20, pady=20)

        self.stop_button = tk.Button(root, text="Stop", font=("Helvetica", 24), command=self.stop, state=tk.DISABLED)
        self.stop_button.pack(side="left", padx=20, pady=20)
        
        self.running = False
        self.paused = False
        self.start_time = 0
        self.elapsed_time = 0
        
        self.update_time()

    def update_time(self):
        if self.running:
            elapsed = time.time() - self.start_time + self.elapsed_time
            mins, secs = divmod(elapsed, 60)
            hours, mins = divmod(mins, 60)
            self.time_label.config(text=f"{int(hours):02}:{int(mins):02}:{int(secs):02}")
        self.root.after(100, self.update_time)

    def start(self):
        if not self.running and not self.paused:
            self.running = True
            self.start_time = time.time()
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
    
    def pause_continue(self):
        if self.running:
            self.running = False
            self.paused = True
            self.elapsed_time += time.time() - self.start_time
            self.pause_button.config(text="Continue")
        elif self.paused:
            self.running = True
            self.paused = False
            self.start_time = time.time()
            self.pause_button.config(text="Pause")

    def stop(self):
        if self.running or self.paused:
            self.running = False
            self.paused = False
            self.elapsed_time += time.time() - self.start_time
        self.time_label.config(text="00:00:00")
        print(f"Elapsed Time: {int(self.elapsed_time // 3600):02}:{int((self.elapsed_time % 3600) // 60):02}:{int(self.elapsed_time % 60):02}")
        self.elapsed_time = 0
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(text="Pause", state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    root.mainloop()
