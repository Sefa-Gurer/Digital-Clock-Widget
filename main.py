from tkinter import *
from gui import Screen
import utils

class Play:
    def __init__(self):

        self.window_width = 420
        self.window_height = 220

        screen_horizontal_cell = 25
        screen_vertical_cell = 9
        self.screen_ratio = screen_horizontal_cell/screen_vertical_cell
        self.margin = 20

        self.old_digits_cells = [[],[],[],[]]

        # Ana pencereyi oluştur
        self.root = Tk()

        window_size = f"{self.window_width}x{self.window_height}"

        self.root.overrideredirect(True)

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
        current_time = utils.get_current_time()
        digits = utils.divide_digits(current_time)
        digits_cells = utils.divide_cells(digits)

        if digits_cells != self.old_digits_cells:
            print("Saat değişti")

            add_item = utils.find_array_diff(digits_cells,self.old_digits_cells)
            delete_item = utils.find_array_diff(self.old_digits_cells,digits_cells)

            for i, value in enumerate(add_item, start=1):
                for j in value:
                    square_corner_one,square_corner_two = self.screen.digits[f"digit{i}"].cell[f"cell{j}"]
                    utils.draw_digit(self.canvas,square_corner_one,square_corner_two,"lightsteelblue",tag=f"cell{i}{j}")

            for i, value in enumerate(delete_item, start=1):
                for j in value:
                    self.canvas.delete(f"cell{i}{j}")

        self.old_digits_cells = digits_cells
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