import time
import tkinter as tk
from tkinter import messagebox
import threading
import winsound

class PomodoroApp:
    def __init__(self, master):
        self.work_duration = 25 * 60
        self.short_break = 5 * 60
        self.long_break = 15 * 60
        self.cycles = 4
        self.current_cycle = 0
        self.is_running = False

        # Configuração geral da janela
        master.title("Pomodoro Timer")
        master.configure(bg="#f0f0f0")
        master.geometry("300x300")
        master.resizable(False, False)

        # Título
        self.label = tk.Label(master, text="Pomodoro Timer", font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#333")
        self.label.pack(pady=20)

        # Exibição do cronômetro
        self.time_display = tk.Label(master, text="25:00", font=("Helvetica", 48, "bold"), bg="#f0f0f0", fg="#e53935")
        self.time_display.pack(pady=10)

        # Frame para os botões
        self.button_frame = tk.Frame(master, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        # Botões estilizados
        btn_style = {"font": ("Helvetica", 12), "width": 8, "bg": "#4caf50", "fg": "white", "activebackground": "#388e3c"}

        self.start_button = tk.Button(self.button_frame, text="Iniciar", command=self.start_timer, **btn_style)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Parar", command=self.stop_timer, **btn_style)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Resetar", command=self.reset_timer, **btn_style)
        self.reset_button.grid(row=0, column=2, padx=5)

        # Rodapé com instruções (opcional)
        self.footer = tk.Label(master, text="Foco e disciplina!", font=("Helvetica", 10), bg="#f0f0f0", fg="#555")
        self.footer.pack(pady=10)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.current_cycle = 1
            self.start_work()

    def stop_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.current_cycle = 0
        self.update_time_display(self.work_duration)

    def start_work(self):
        if self.current_cycle <= self.cycles and self.is_running:
            self.alert("Início do Trabalho!")
            self.countdown(self.work_duration, self.start_break)

    def start_break(self):
        if self.current_cycle < self.cycles and self.is_running:
            self.alert("Hora do Intervalo Curto!")
            self.countdown(self.short_break, self.start_next_cycle)
        elif self.current_cycle == self.cycles and self.is_running:
            self.alert("Hora do Intervalo Longo!")
            self.countdown(self.long_break, self.end_pomodoro)

    def start_next_cycle(self):
        if self.is_running:
            self.current_cycle += 1
            self.start_work()

    def end_pomodoro(self):
        self.is_running = False
        self.alert("Pomodoro Completo!")
        self.update_time_display(self.work_duration)

    def countdown(self, count, next_func):
        def run():
            local_count = count
            while local_count >= 0 and self.is_running:
                mins, secs = divmod(local_count, 60)
                time_str = f"{mins:02d}:{secs:02d}"
                self.time_display.config(text=time_str)
                time.sleep(1)
                local_count -= 1
            if self.is_running:
                next_func()
        t = threading.Thread(target=run)
        t.start()

    def update_time_display(self, seconds):
        mins, secs = divmod(seconds, 60)
        self.time_display.config(text=f"{mins:02d}:{secs:02d}")

    def alert(self, message):
        messagebox.showinfo("Pomodoro Timer", message)
        duration = 500  # ms
        freq = 1000     # Hz
        winsound.Beep(freq, duration)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()