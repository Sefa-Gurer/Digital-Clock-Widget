import time

def get_current_time():
    """Güncel saati çeker"""
    t = time.localtime()
    return (t.tm_hour,t.tm_min)

def find_array_diff(current,old):
    """İki dizi arasındaki farkları bulur. (eklenenler,çıkanlar) döndürür"""

    add_array = [[],[],[],[]]

    for i, in_array in enumerate(current,start=0):
        for in_item in in_array:
            if in_item not in old[i]:
                add_array[i].append(in_item)

    return add_array

def divide_digits(current_time):
    """Bir sayıyı basamaklarına ayırır"""

    digits = []
    for i in current_time:
        tens_place = i // 10
        ones_place = i % 10
        digits.append((tens_place,ones_place))
    return digits

def divide_cells(digits):
    """Basamağı hücrelere böler"""
    """ 
        cell id ==>    0  
                     5   1
                       6 
                     4   2
                       3
    """
    cells_lib = {
        0:[0,1,2,3,4,5],
        1:[1,2],        2:[0,1,3,4,6],        3:[0,1,2,3,6],
        4:[1,2,5,6],    5:[0,2,3,5,6],        6:[0,2,3,4,5,6],
        7:[0,1,2,5],    8:[0,1,2,3,4,5,6],    9:[0,1,2,3,5,6]
    }
    cells = []
    for i in digits:
        for j in i:
            cells.append(cells_lib[j])
    return cells

def draw_digit(canvas,square_corner_one,square_corner_two,square_color,tag):
    """Bir dikdörtgen (veya kare) çizer"""
    canvas.create_rectangle(
        square_corner_one[0], square_corner_one[1], 
        square_corner_two[0], square_corner_two[1], 
        fill=square_color, outline=square_color,
        tags=tag
    )