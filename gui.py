class Screen:
    def __init__(self,
                 canvas,
                 square_corner_one,
                 square_corner_two,
                 square_color = "blue"):

        # Geometrik şekiller çizelim
        canvas.create_rectangle(square_corner_one[0], square_corner_one[1], 
                                square_corner_two[0], square_corner_two[1], 
                                fill=square_color, outline=square_color)

