
class Screen:
    def __init__(self,
                 canvas,
                 square_corner_one,
                 square_corner_two,
                 horizontal_cell,
                 vertical_cell,
                 square_color="blue"):

        self.canvas = canvas  # Canvas'ı sakla, ileride başka şeyler çizmek için kullanılabilir
        self.square_corner_one = square_corner_one
        self.square_corner_two = square_corner_two
        self.horizontal_cell = horizontal_cell
        self.vertical_cell = vertical_cell
        self.square_color = square_color

        self.horizontal_cell_size = (self.square_corner_two[0]-self.square_corner_one[0])/self.horizontal_cell

        self.digits = {}
        for i in range(5):
            i = i+1
            square_corner_one,square_corner_two = self.find_digits_corner(i)
            self.digits[f"digit{i}"] = Digits(self.canvas,i,square_corner_one,square_corner_two)

    def find_digits_corner(self,digit_id):
        """ 
        digits ==>  0 8 : 4 6
        id     ==>  1 2 5 3 4
        """

        if digit_id == 1:
            corner_one = self.square_corner_one
            corner_two = (self.horizontal_cell_size*5+self.square_corner_one[0],
                          self.square_corner_two[1])
        elif digit_id == 2:
            corner_one = (self.horizontal_cell_size*6+self.square_corner_one[0],
                          self.square_corner_one[1])
            corner_two = (self.horizontal_cell_size*11+self.square_corner_one[0],
                          self.square_corner_two[1])
        elif digit_id == 5:
            corner_one = (self.horizontal_cell_size*12+self.square_corner_one[0],
                          self.square_corner_one[1])
            corner_two = (self.horizontal_cell_size*13+self.square_corner_one[0],
                          self.square_corner_two[1])
        elif digit_id == 3:
            corner_one = (self.horizontal_cell_size*14+self.square_corner_one[0],
                          self.square_corner_one[1])
            corner_two = (self.horizontal_cell_size*19+self.square_corner_one[0],
                          self.square_corner_two[1])
        elif digit_id == 4:
            corner_one = (self.horizontal_cell_size*20+self.square_corner_one[0],
                          self.square_corner_one[1])
            corner_two = (self.horizontal_cell_size*25+self.square_corner_one[0],
                          self.square_corner_two[1])
        return corner_one,corner_two

    def draw_square(self,square_corner_one,square_corner_two,square_color,tag):
        """Bir dikdörtgen (veya kare) çizer"""
        self.canvas.create_rectangle(
            square_corner_one[0], square_corner_one[1], 
            square_corner_two[0], square_corner_two[1], 
            fill=square_color, outline=square_color,
            tags=tag
        )
    
    def draw_delete(self,tag):
        self.canvas.delete(tag)

class Digits:
    def __init__(self,
                 canvas,
                 id,
                 corner_one,
                 corner_two,
                 colors="blue"):

        self.canvas = canvas
        self.id = id
        self.corner_one = corner_one
        self.corner_two = corner_two
        self.colors = colors
        self.horizontal_cell = 5
        self.vertical_cell = 9

        self.horizontal_cell_size = (self.corner_two[0]-corner_one[0])/self.horizontal_cell
        self.vertical_cell_size = (self.corner_two[1]-corner_one[1])/self.vertical_cell

        self.cell = {}

        for i in range(7):

            # square_corner_one,square_corner_two = self.find_cells_corner(i)
            # self.draw_digit(square_corner_one,square_corner_two,"green",tag="cell")

            self.cell[f"cell{i}"] = self.find_cells_corner(i)

    def find_cells_corner(self,cell_id):
        """ 
        cell id ==>    0  
                     5   1
                       6 
                     4   2
                       3
        """
        if cell_id == 0:
            corner_one = (self.horizontal_cell_size*1 + self.corner_one[0],
                          self.corner_one[1])
            corner_two = (self.horizontal_cell_size*4 + self.corner_one[0],
                          self.vertical_cell_size*1 + self.corner_one[1])
        elif cell_id == 1:
            corner_one = (self.horizontal_cell_size*4 + self.corner_one[0],
                          self.vertical_cell_size*1 + self.corner_one[1])
            corner_two = (self.horizontal_cell_size*5 + self.corner_one[0],
                          self.vertical_cell_size*4 + self.corner_one[1])
        elif cell_id == 2:
            corner_one = (self.horizontal_cell_size*4 + self.corner_one[0],
                          self.vertical_cell_size*5 + self.corner_one[1])
            corner_two = (self.horizontal_cell_size*5 + self.corner_one[0],
                          self.vertical_cell_size*8 + self.corner_one[1])
        elif cell_id == 3:
            corner_one = (self.horizontal_cell_size*1 + self.corner_one[0],
                          self.vertical_cell_size*8 + self.corner_one[1])
            corner_two = (self.horizontal_cell_size*4 + self.corner_one[0],
                          self.vertical_cell_size*9 + self.corner_one[1])
        elif cell_id == 4:
            corner_one = (self.horizontal_cell_size*0 + self.corner_one[0],
                          self.vertical_cell_size*5 + self.corner_one[1])
            corner_two = (self.horizontal_cell_size*1 + self.corner_one[0],
                          self.vertical_cell_size*8 + self.corner_one[1])
        elif cell_id == 5:
            corner_one = (self.horizontal_cell_size*0 + self.corner_one[0],
                          self.vertical_cell_size*1 + self.corner_one[1])
            corner_two = (self.horizontal_cell_size*1 + self.corner_one[0],
                          self.vertical_cell_size*4 + self.corner_one[1])
        elif cell_id == 6:
            corner_one = (self.horizontal_cell_size*1 + self.corner_one[0],
                          self.vertical_cell_size*4 + self.corner_one[1])
            corner_two = (self.horizontal_cell_size*4 + self.corner_one[0],
                          self.vertical_cell_size*5 + self.corner_one[1])
        return corner_one,corner_two

    def draw_digit(self,square_corner_one,square_corner_two,square_color,tag):
        """Bir dikdörtgen (veya kare) çizer"""
        self.canvas.create_rectangle(
            square_corner_one[0], square_corner_one[1], 
            square_corner_two[0], square_corner_two[1], 
            fill=square_color, outline=square_color,
            tags=tag
        )