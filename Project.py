import tkinter as t 
from tkinter import colorchooser as tc
import random
import json 
from tkinter.messagebox import showwarning, showinfo

class GameOfLife:
    
    def __init__(self):
        self.board = [0] * 2025
        self.previous_states = set()
        self.is_running = False
        self.speed = 500  
        self.max_score = 0  
        self.shape_default = 0
        self.default_shape_label = ''
        
        self.color_alive = "red"
        self.color_dead = 'blue'
        self.WINDOW = t.Tk()
        self.WINDOW.title("Game of Life")
        self.WINDOW.geometry("900x900")
        self.canvas = t.Canvas(self.WINDOW, width=900, height=900, bg='white')
        self.canvas.pack()
        
        self.control_window = self.create_control_window()
        self.cell_size = 20
        self.create_buttons()
        self.random_click()
        self.canvas.bind("<Button-1>", self.click_btn) 
        self.WINDOW.mainloop()
        

    def create_control_window(self):
        control_window = t.Toplevel(self.WINDOW)
        control_window.title("Control Panel")
        control_window.geometry("200x400")

        self.score_label = t.Label(control_window, text="Score: 0")
        self.score_label.pack()

        self.max_score_label = t.Label(control_window, text="Max Score: 0")
        self.max_score_label.pack()

        start_button = t.Button(control_window, text="Start", command=self.start_game)
        start_button.pack()

        pause_button = t.Button(control_window, text="Pause", command=self.pause_game)
        pause_button.pack()

        resume_button = t.Button(control_window, text="Resume", command=self.resume_game)
        resume_button.pack()

        self.speed_scale = t.Scale(control_window, from_=100, to=1000, orient='horizontal', 
                                    label='Speed (ms)', command=self.update_speed)
        self.speed_scale.set(self.speed)  
        self.speed_scale.pack()

        btn_clear_board = t.Button(control_window, text="Clear", command=self.reset_game)
        btn_clear_board.pack()

        btn_save_preset = t.Button(control_window, text="Save Preset", command=self.save_preset)
        btn_save_preset.pack()

        btn_load_preset = t.Button(control_window, text="Load Preset", command=self.load_preset)
        btn_load_preset.pack()

        btn_toggle_shape = t.Button(control_window, text="Toggle Shape", command=self.change_cell)
        btn_toggle_shape.pack()

        btn_info_cell = t.Button(control_window, text="Info Cell", command=self.info_cell)
        btn_info_cell.pack()

        btn_change_colors = t.Button(control_window, text="Change Colors", command=self.change_colors)
        btn_change_colors.pack()
        return control_window

    def update_speed(self, value):
        self.speed = int(value)
        if self.is_running:
            self.pause_game()
            self.resume_game()
        
    def create_buttons(self):
        self.rects = []
        for j in range(45):
            row = []
            for i in range(45):
                rect = self.canvas.create_rectangle(i * self.cell_size, j * self.cell_size,
                                                     (i + 1) * self.cell_size, (j + 1) * self.cell_size,
                                                     fill=self.color_dead, outline='black')
                row.append(rect)
            self.rects.append(row)

    def click_btn(self, event):
        if self.shape_default == 0:
            x, y = event.x // self.cell_size, event.y // self.cell_size
            index = y * 45 + x
            if self.board[index] == 0:
                self.canvas.itemconfig(self.rects[y][x], fill=self.color_alive)
                self.board[index] = 1
            else:
                self.canvas.itemconfig(self.rects[y][x], fill=self.color_dead)
                self.board[index] = 0
            self.update_score() 
        elif self.shape_default == 1:
            x, y = event.x // self.cell_size, event.y // self.cell_size
            if x + 2 < 45 and y + 2 < 45:
                for dy in range(3):
                    for dx in range(3):
                        self.canvas.itemconfig(self.rects[y + dy][x + dx], fill =self.color_alive)
                        self.board[(y + dy) * 45 + (x + dx)] = 1
                self.update_score()
        elif self.shape_default == 2: #planer1
            x, y = event.x // self.cell_size, event.y // self.cell_size
            if x + 2 < 45 and y + 2 < 45:  
                self.canvas.itemconfig(self.rects[y][x + 1], fill=self.color_alive)  
                self.board[y * 45 + (x + 1)] = 1
                
                self.canvas.itemconfig(self.rects[y + 1][x + 2], fill=self.color_alive)  
                self.board[(y + 1) * 45 + (x + 2)] = 1
                
                self.canvas.itemconfig(self.rects[y + 2][x], fill=self.color_alive)  
                self.board[(y + 2) * 45 + x] = 1
                
                self.canvas.itemconfig(self.rects[y + 2][x + 1], fill=self.color_alive)  
                self.board[(y + 2) * 45 + (x + 1)] = 1
                
                self.canvas.itemconfig(self.rects[y + 2][x + 2], fill=self.color_alive)  
                self.board[(y + 2) * 45 + (x + 2)] = 1
                
                self.update_score()
        elif self.shape_default == 3: #planer2
            x, y = event.x // self.cell_size, event.y // self.cell_size
            if x + 2 < 45 and y + 2 < 45:  
                self.canvas.itemconfig(self.rects[y][x], fill=self.color_alive)  
                self.board[y * 45 + (x)] = 1
                
                self.canvas.itemconfig(self.rects[y][x + 1], fill=self.color_alive)  
                self.board[(y) * 45 + (x + 1)] = 1
                
                self.canvas.itemconfig(self.rects[y][x + 2], fill=self.color_alive)  
                self.board[(y) * 45 + (x + 2)] = 1
                
                self.canvas.itemconfig(self.rects[y + 1][x], fill=self.color_alive)  
                self.board[(y + 1) * 45 + (x)] = 1
                
                self.canvas.itemconfig(self.rects[y + 2][x + 1], fill=self.color_alive)  
                self.board[(y + 2) * 45 + (x + 1)] = 1
                
                self.update_score()
        elif self.shape_default == 4: #planer3
            x, y = event.x // self.cell_size, event.y // self.cell_size
            if x + 2 < 45 and y + 2 < 45:  
                self.canvas.itemconfig(self.rects[y][x], fill=self.color_alive)  
                self.board[y * 45 + (x)] = 1
                
                self.canvas.itemconfig(self.rects[y][x + 1], fill=self.color_alive)  
                self.board[(y) * 45 + (x + 1)] = 1
                
                self.canvas.itemconfig(self.rects[y][x + 2], fill=self.color_alive)  
                self.board[(y) * 45 + (x + 2)] = 1
                
                self.canvas.itemconfig(self.rects[y + 1][x + 2], fill=self.color_alive)  
                self.board[(y + 1) * 45 + (x + 2)] = 1
                
                self.canvas.itemconfig(self.rects[y + 2][x + 1], fill=self.color_alive)  
                self.board[(y + 2) * 45 + (x + 1)] = 1
        elif self.shape_default == 5: #planer4
            x, y = event.x // self.cell_size, event.y // self.cell_size
            if x + 2 < 45 and y + 2 < 45:  
                self.canvas.itemconfig(self.rects[y][x + 1], fill=self.color_alive)  
                self.board[(y) * 45 + (x)] = 1
                
                self.canvas.itemconfig(self.rects[y + 1][x], fill=self.color_alive)  
                self.board[(y + 1) * 45 + (x)] = 1  
                
                self.canvas.itemconfig(self.rects[y + 2][x], fill=self.color_alive)  
                self.board[(y + 2) * 45 + x] = 1
                
                self.canvas.itemconfig(self.rects[y + 2][x + 1], fill=self.color_alive)  
                self.board[(y + 2) * 45 + (x + 1)] = 1
                
                self.canvas.itemconfig(self.rects[y + 2][x + 2], fill=self.color_alive)  
                self.board[(y + 2) * 45 + (x + 2)] = 1

    def random_click(self):
        number_of_plus = random.randint(2, 15)
        for _ in range(number_of_plus):
            center_x = random.randint(1, 43)
            center_y = random.randint(1, 43)
            plus_cells = [
                (center_x, center_y),  
                (center_x - 1, center_y),  
                (center_x + 1, center_y),  
                (center_x, center_y - 1), 
                (center_x, center_y + 1)   
            ]
            if all(self.board[y * 45 + x] == 0 for x, y in plus_cells):
                for x, y in plus_cells:
                    index = y * 45 + x
                    self.board[index] = 1
                    self.canvas.itemconfig(self.rects[y][x], fill=self.color_alive)
        self.update_score()

    def count_neighbors(self, i):
        result = 0
        directions = [-46, -45, -44, -1, 1, 44, 45, 46]
        for n in directions:
            neighbor_index = i + n
            if neighbor_index >= 0 and neighbor_index < 2025:
                result += self.board[neighbor_index]
        return result
    
    def logic_game_life(self):
        if not self.is_running:
            self.WINDOW.after(self.speed, self.logic_game_life)
            return
        self.new_board = [0] * 2025
        for i in range(2025):
            count = self.count_neighbors(i)
            if self.board[i] == 1:
                if count < 2 or count > 3:
                    self.new_board[i] = 0  
                else:
                    self.new_board[i] = 1  
            else:
                if count == 3:
                    self.new_board[i] = 1  
        if sum(self.new_board) == 0:
            self.is_running = False
            showwarning(title='Игра Приостановлена', message=f'Все клетки мертвы\nВаш Max Score: {self.max_score}' )
            return
        if self.board == self.new_board:
            self.is_running = False
            showinfo(title='Игра Приостановлена', message=f'Стабильная конфигурация\nВаш Max Score: {self.max_score}')
            return
        for i in range(2025):
            if self.new_board[i] == 1:
                self.canvas.itemconfig(self.rects[i // 45][i % 45], fill=self.color_alive)
            else:
                self.canvas.itemconfig(self.rects[i // 45][i % 45], fill=self.color_dead)


        self.board = self.new_board  
        self.update_score()  
        self.WINDOW.after(self.speed, self.logic_game_life)  
    
    def update_cell_colors(self):
        for i in range(2025):
            color = self.color_alive if self.board[i] == 1 else self.color_dead
            self.canvas.itemconfig(self.rects[i // 45][i % 45], fill=color)


    def update_score(self):
        score = sum(self.board)  
        self.score_label.config(text=f"Score: {score}")  
        if score > self.max_score:  
            self.max_score = score
            self.max_score_label.config(text=f"Max Score: {self.max_score}") 

    def start_game(self):
        self.is_running = True
        self.WINDOW.after(self.speed, self.logic_game_life)  

    def pause_game(self):
        self.is_running = False

    def resume_game(self):
        self.is_running = True
        self.WINDOW.after(self.speed, self.logic_game_life)

    def speed_up(self):
        self.speed = max(100, self.speed - 100)  

    def speed_down(self):
        self.speed += 100  

    def reset_game(self):
        self.board = [0] * 2025
        self.create_buttons()

    def save_preset(self):
        preset_data = {
            "board": self.board,
            "speed": self.speed,
            "color_alive": self.color_alive,
            "color_dead": self.color_dead
        }
        with open("preset.json", "w") as f:
            json.dump(preset_data, f)
        showinfo(title='Preset Saved | Пресет сохранен', message='The current board state, speed, color_alive and color_dead have been saved.\nСохранен пресет с текущей скоростью программы, расстоновкой поля, цветом живых и цветом мертвых.')

    def load_preset(self):
        try:
            with open("preset.json", "r") as f:
                preset_data = json.load(f) 
                self.board = preset_data["board"]
                self.speed = preset_data["speed"]
                self.color_alive = preset_data["color_alive"]
                self.color_dead = preset_data["color_dead"]
            for i in range(2025):
                if self.board[i] == 1:
                    self.canvas.itemconfig(self.rects[i // 45][i % 45], fill=self.color_alive)
                else:
                    self.canvas.itemconfig(self.rects[i // 45][i % 45], fill=self.color_dead)
            self.update_score()
            showinfo(title='Preset Loaded | Сохраненный пресет загружен', message='The board state, speed, color_alive, color_dead have been loaded.\nУстановлен пресет с сохраненной скоростью программы, расстоновкой поля, цветом живых и цветом мертвых.')
        except FileNotFoundError:
            showwarning(title='Error | Ошибка', message='No preset file found.\n Не найден пресет с сохраненными настройками.')

    def change_colors(self):
        color_alive = tc.askcolor(title="Choose color for alive cells")[1]
        color_dead = tc.askcolor(title="Choose color for dead cells")[1]
        if color_alive and color_dead:
            self.color_alive = color_alive
            self.color_dead = color_dead
            self.update_cell_colors()

    def change_cell(self):
        self.shape_default += 1
        if self.shape_default > 5:
            self.shape_default = 0
    
    def info_cell(self):
        if self.shape_default == 0:
            showinfo(title='Already Cell | Текущая фигура', message='Cell: Single\nФигура: Одиночная расстановка')
        elif self.shape_default == 1:
            showinfo(title='Already Cell | Текущая фигура', message='Cell: Cube 3x3\nФигура: Расстановка 3х3')
        elif self.shape_default == 2:
            showinfo(title='Already Cell | Текущая фигура', message='Cell: Planer№1\nФигура: Планер №1')
        elif self.shape_default == 3:
            showinfo(title='Already Cell | Текущая фигура', message='Cell: Planer№2\nФигура: Планер №2')
        elif self.shape_default == 4:
            showinfo(title='Already Cell | Текущая фигура', message='Cell: Planer№3\nФигура: Планер №3')
        elif self.shape_default == 5:
            showinfo(title='Already Cell | Текущая фигура', message='Cell: Planer№4\nФигура: Планер №4')

if __name__ == "__main__":
    GameOfLife()