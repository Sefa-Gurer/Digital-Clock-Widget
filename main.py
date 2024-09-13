from tkinter import *
from gui import Screen
import time

class Play:
    def __init__(self):

        self.window_width = 520
        self.window_height = 220

        screen_horizontal_cell = 25
        screen_vertical_cell = 9
        self.screen_ratio = screen_horizontal_cell/screen_vertical_cell
        self.margin = 20

        # Ana pencereyi oluştur
        self.root = Tk()

        window_size = f"{self.window_width}x{self.window_height}"

        # Pencere boyutunu ve şeffaflığını ayarla
        self.root.geometry(window_size)
        self.root.attributes('-alpha', 1)  # Pencereyi tam görünür yap
        self.root.wm_attributes('-transparentcolor', '#ab23ff')  # Bu rengi şeffaf yap

        # Canvas'ı oluştur
        self.canvas = Canvas(self.root, width=self.window_width, height=self.window_height, bg='#ab23ff', highlightthickness=0)
        self.canvas.pack()

        screen_size = self.find_screen_size()

        self.screen = Screen(self.canvas,
            square_corner_one=screen_size[0],
            square_corner_two=screen_size[1],
            horizontal_cell = screen_horizontal_cell,
            vertical_cell = screen_vertical_cell,
            square_color="red")

        self.run()

    def run(self):

        # 1000 milisaniye (1 saniye) sonra tekrar run()'u çalıştır
        self.root.after(1000, self.run)

    def find_screen_size(self):
        if (self.window_height-(2*self.margin)) * self.screen_ratio <= (self.window_width-(2*self.margin)):
            screen_height = self.window_height-(2*self.margin)
            screen_width = screen_height * self.screen_ratio
        else:
            screen_width = self.window_width-(2*self.margin)
            screen_height = screen_width / self.screen_ratio

        corner_one = (self.window_width-screen_width)/2,(self.window_height-screen_height)/2
        corner_two = (self.window_width-corner_one[0]),(self.window_height-corner_one[1])

        return (corner_one,corner_two)

if __name__ == '__main__':
    play = Play()
    # Ana pencereyi başlat
    play.root.mainloop()