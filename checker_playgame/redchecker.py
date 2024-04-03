class RedChecker():
    def __init__(self, circle_x, circle_y):
        """
        construct a class for red checker
        """
        self.square_size = 100
        self.lenth = 8
        SMALL_FACTOR = 0.9
        self.radius = self.square_size * SMALL_FACTOR
        self.king = False
        self.highlight_checker = False
        self.circle_x = circle_x
        self.circle_y = circle_y
        self.color = 1  # red color
        self.can_move = False
        self.can_jump = False
        self.become_king()

    def become_king(self):
        low_bound = (self.lenth-1) * self.square_size
        high_bound = self.lenth * self.square_size
        if low_bound < self.circle_y < high_bound:
            self.king = True

    def display(self):
        """
        display a checker or a king checker
        The checker is a black circle with white frame
        The king checker has a crown on it
        """
        RED = (255, 0, 0)
        TWO = 2
        fill_color = RED
        if self.highlight_checker is False:
            STROKE_WEIGHT = 2
        else:
            STROKE_WEIGHT = 4
        STROKE_COLOR = 255  # white color
        strokeWeight(STROKE_WEIGHT)
        stroke(STROKE_COLOR)
        fill(*fill_color)
        ellipse(self.circle_x, self.circle_y, self.radius, self.radius)

        STROKE_COLOR = 255  # white color
        stroke(STROKE_COLOR)
        FACTOR = 0.8
        small_radius = self.radius * FACTOR
        ellipse(self.circle_x, self.circle_y, small_radius, small_radius)

        if self.king is True:
            k_image = loadImage("crown.png")
            image(k_image, self.circle_x-k_image.width/TWO,
                  self.circle_y-k_image.width/TWO)
