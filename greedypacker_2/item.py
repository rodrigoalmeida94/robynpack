"""
2D Item class.
"""
class Item:
    """
    Items class for rectangles inserted into sheets
    """
    def __init__(self, width, height, bottom_clear=0, top_clear=0, left_clear=0, right_clear=0,
                 CornerPoint: tuple = (0, 0),
                 rotation: bool = True, id=0) -> None:
        self.width = width
        self.height = height
        self.x = CornerPoint[0]
        self.y = CornerPoint[1]
        self.area = self.width * self.height
        self.rotated = False
        self.id = id
        self.bottom_clear = bottom_clear
        self.top_clear = top_clear
        self.left_clear = left_clear
        self.right_clear = right_clear

        self.total_width =  self.left_clear + self.width + self.right_clear
        self.total_height =  self.bottom_clear + self.height + self.top_clear



    def __repr__(self):
        return 'Item(width=%r, height=%r, x=%r, y=%r, b_c=%r, t_c=%r, l_c=%r, r_c=%r,)' % (self.width, self.height, self.x, self.y, self.bottom_clear, self.top_clear, self.left_clear, self.right_clear)


    def rotate(self) -> None:
        self.left_clear, self.top_clear, self.right_clear, self.bottom_clear = self.bottom_clear, self.left_clear, self.top_clear, self.right_clear
        self.width, self.height = self.height, self.width
        self.total_width, self.total_height = self.total_height, self.total_width
        self.rotated = False if self.rotated == True else True
