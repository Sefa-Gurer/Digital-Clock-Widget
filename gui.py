class Screen:
    def __init__(self,
                 canvas,
                 square_corner_one,
                 square_corner_two,
                 square_color="blue"):

        self.canvas = canvas  # Canvas'ı sakla, ileride başka şeyler çizmek için kullanılabilir
        self.square_corner_one = square_corner_one
        self.square_corner_two = square_corner_two
        self.square_color = square_color


        # for i in range(4):
        #     "digit"+str(i) = Digits(i,)


        # Geometrik şekiller çizelim
        self.draw_square()

    # def find_digits_corner(self,digits_id):
    #     """ 
    #     digits ==>  1 2 : 1 2
    #     id     ==>  2 1 :-1-2
    #     """
    #     if digits_id == 2:
    #         corner_one = self.square_corner_one
    #         corner_two =   
    #     self.square_corner_one
    #     self.square_corner_two

    def draw_square(self):
        """Bir dikdörtgen (veya kare) çizer"""
        self.canvas.create_rectangle(
            self.square_corner_one[0], self.square_corner_one[1], 
            self.square_corner_two[0], self.square_corner_two[1], 
            fill=self.square_color, outline=self.square_color,
            tags="cerceve"
        )
    
    def draw_delete(self):
        self.canvas.delete("cerceve")

class Digits:
    def __init__(self,
                 id,
                 corner_one,
                 corner_two,
                 colors="blue"):

        self.id = id
        self.corner_one = corner_one
        self.corner_two = corner_two
        self.colors = colors
        
class Cells:
    def __init__(self,
                id,
                value):

        self.id = id
        self.value = value
