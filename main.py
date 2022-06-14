import pygame.draw
import random
from pygame import *
"""Nonogram game"""
pygame.init()


class Blocks:
    """Blocks class"""
    def __init__(self, screen, pos_x, pos_y, size, row_num, col_num):
        self.rect = Rect((pos_x, pos_y), (size, size))  # rect
        self.screen = screen

        self.row_num = row_num
        self.col_num = col_num

        # colors
        self.color_fill = (0, 0, 0)
        self.color_empty = (255, 255, 255)
        self.state_color = self.color_empty

    def checkClick(self, row, col):
        """Check Click"""

        x, y = pygame.mouse.get_pos()
        if (self.rect.left <= x <= self.rect.right) and (self.rect.top <= y <= self.rect.bottom):
            # switch
            if self.state_color == self.color_fill:
                self.state_color = self.color_empty
                row[self.row_num] -= 1
                col[self.col_num] -= 1

            elif self.state_color == self.color_empty:
                self.state_color = self.color_fill
                row[self.row_num] += 1
                col[self.col_num] += 1

        return row, col

    def randChoose(self, row, col, array):
        """Random Choose"""
        if random.randint(0, 2) == 0 or random.randint(0, 2) == 1:
            row[self.row_num] += 1
            col[self.col_num] += 1
            array[self.row_num][self.col_num] = 1
            return row, col, array
        return row, col, array

    def drawBlocks(self):
        "Draw blocks"
        pygame.draw.rect(self.screen, color=self.state_color, rect=self.rect)


class Numbers:
    """Numbers"""
    def __init__(self, screen, array, size, padding):

        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 75)
        self.array = array

        # images
        self.cols = [[], [], [], []]
        self.rows = [[], [], [], []]

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.size = size
        self.padding = padding

    def checkCol(self):
        """Check Col"""
        for c in range(len(self.cols)):

            firstNum = 0
            secondNum = 0
            theNum = None
            second = False

            for r in range(len(self.array[c])):
                if self.array[r][c] == 1 and second is False:
                    firstNum += 1
                if self.array[r][c] == 1 and second is True:
                    secondNum += 1

                if theNum == 1 and self.array[r][c] == 0:
                    second = True
                theNum = self.array[r][c]

            self.cols[c] = [self.font.render(str(firstNum), True, self.black, self.white),
                            self.font.render(str(secondNum), True, self.black, self.white)]

    def checkRow(self):
        """Check Row"""
        for r in range(len(self.rows)):

            firstNum = 0
            secondNum = 0
            theNum = None
            second = False

            for c in range(len(self.array[r])):
                if self.array[r][c] == 1 and second is False:
                    firstNum += 1
                if self.array[r][c] == 1 and second is True:
                    secondNum += 1

                if theNum == 1 and self.array[r][c] == 0:
                    second = True
                theNum = self.array[r][c]

            self.rows[r] = [self.font.render(str(firstNum), True, self.black, self.white),
                            self.font.render(str(secondNum), True, self.black, self.white)]


    def drawText(self):
        """draw texts"""
        for i in range(4):

            # create cols rect
            self.screen.blit(self.cols[i][0], self.cols[i][0].get_rect(topleft=(self.size * 1.5 + self.size * i + self.padding, self.padding)))
            self.screen.blit(self.cols[i][1], self.cols[i][1].get_rect(topleft=(self.size * 1.5 + self.size * i + self.padding, self.padding+self.size*0.65)))
            # create rows rect
            self.screen.blit(self.rows[i][0], self.rows[i][0].get_rect(topleft=(self.padding, self.size*1.5+self.size*i+self.padding)))
            self.screen.blit(self.rows[i][1], self.rows[i][1].get_rect(topleft=(self.padding+self.size*1, self.size * 1.5 + self.size * i + self.padding)))


class Main:
    """Main class"""
    def __init__(self):

        self.size = 100
        self.screen = pygame.display.set_mode((self.size*4+int(self.size*1.5), self.size*4+int(self.size*1.5)))
        self.padding = 5
        pygame.display.set_caption("Nonogram")

        # time
        self.clock = pygame.time.Clock()
        self.fps = 100

        self.run = True

        self.blocks = []
        self.black = (0, 0, 0)

        self.rowData = [0, 0, 0, 0]
        self.colData = [0, 0, 0, 0]

        self.buttonClick = False
        self.array = [[0 for x in range(4)] for i in range(4)]
        self.numbers = None

        self.restart = False

    def randomChoose(self):
        """Random choose blocks"""
        for block in self.blocks:
            self.rowData, self.colData, self.array = block.randChoose(self.rowData, self.colData, self.array)

    def createBlocks(self):
        """Create"""
        row, col = 0, 0
        for x in range(int(self.size*1.5)+self.padding, int(self.size * 1.5) + self.padding + self.size*4, self.size):
            for y in range(int(self.size * 1.5) + self.padding, int(self.size * 1.5) + self.padding + self.size * 4, self.size):
                self.blocks.append(Blocks(self.screen, x, y, self.size-self.padding*2, row, col))
                row += 1
            row = 0
            col += 1

    def checkTable(self):
        """Check Table"""
        array = [[0 for x in range(4)] for i in range(4)]

        for r in range(4):
            for c in range(4):
                index = r*3+c+r
                if self.blocks[index].state_color == self.blocks[index].color_fill:
                    array[c][r] = 1

        if self.array == array:
            print("done ")
            self.restart = True
            self.run = False

    def event(self):
        """Event loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.MOUSEBUTTONDOWN and self.buttonClick is False:
                self.buttonClick = True

            if event.type == pygame.MOUSEBUTTONUP and self.buttonClick is True:
                self.buttonClick = False
                for block in self.blocks:
                    self.rowData, self.colData = block.checkClick(self.rowData, self.colData)

            # check key press
            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.checkTable()



    def main(self):
        """Main func"""
        self.createBlocks()
        self.randomChoose()

        self.numbers = Numbers(self.screen, self.array, self.size, self.padding)
        self.numbers.checkCol()
        self.numbers.checkRow()
        while self.run is True:

            self.event()
            self.draw()

        if self.restart is True:
            self.__init__()
            self.main()
        else:
            quit()

    def draw_lines(self):
        """Draw lines"""

        # horizontal lines
        pygame.draw.line(self.screen, self.black, (0, int(self.size*1.5)), (self.screen.get_width(), int(self.size*1.5)), width=3)
        for y in [self.size*1.5+self.size, self.size*1.5+self.size*2, self.size*1.5+self.size*3]:
            pygame.draw.line(self.screen, self.black, (0, y), (self.screen.get_width(), y), width=3)

        # vertical lines
        for x in [self.size*1.5, self.size*1.5+self.size, self.size*1.5+self.size*2, self.size*1.5+self.size*3]:
            pygame.draw.line(self.screen, self.black, (x, 0), (x, self.screen.get_height()), width=3)

    def draw(self):
        self.screen.fill((255, 255, 255))

        for block in self.blocks:
            block.drawBlocks()

        self.draw_lines()
        self.numbers.drawText()
        pygame.display.flip()
        self.clock.tick(self.fps)


if __name__ == '__main__':
    Main().main()

