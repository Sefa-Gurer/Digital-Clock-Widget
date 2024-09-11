from tkinter import *
from gui import Screen

class Play:
    def __init__(self):

        self.screen_width = 400
        self.screen_height = 250

        # Ana pencereyi oluştur
        root = Tk()

        screen_size = str(self.screen_width)+"x"+str(self.screen_height)
        # Pencere boyutunu ve şeffaflığını ayarla
        root.geometry(screen_size)
        root.attributes('-alpha', 1)  # Pencereyi tam görünür yap
        root.wm_attributes('-transparentcolor', '#ab23ff')  # Bu rengi şeffaf yap

        # Canvas'ı oluştur
        canvas = Canvas(root, width=400, height=250, bg='#ab23ff', highlightthickness=0)
        canvas.pack()

        Screen(canvas,
               square_corner_one=(25,25),
               square_corner_two=(self.screen_width-25,self.screen_height-25),
               square_color="red")

        # Ana pencereyi başlat
        root.mainloop()


#---------------kalınan yer-------------------
    # def run():

if __name__ == '__main__':
    play = Play()