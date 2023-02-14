import pygame
from copy import deepcopy
from settings import * 

#Setup
pygame.init()
pygame.display.init()

#Pygame Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
window_title = pygame.display.set_caption(TITLE)

#The Othello Board
class Othello_board:

    def __init__(self):
        self.width = 60
        self.row = 8
        self.col = 8
        self.margin = 100
        self.tiles = [[0 for _ in range(self.col)] for _ in range(self.row)]
        self.stable = [[0 for _ in range(self.col)] for _ in range(self.row)]
        self.offense = 2
        self.tiles[self.row // 2 - 1][self.col // 2 - 1] = 1
        self.tiles[self.row // 2][self.col // 2] = 1
        self.tiles[self.row // 2][self.col // 2 - 1] = 2
        self.tiles[self.row // 2 - 1][self.col // 2] = 2
        self.count_black = 2
        self.count_white = 2
        self.count_available = 4
        self.count_stable_black = 0
        self.count_stable_white = 0
        self.count_total_stable_direct_black = 0
        self.count_total_stable_direct_white = 0
        self.available = []
        self.updateAvailable()

    def updateAvailable(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color = self.offense
        color_reverse = 3 - color
        self.available = []
        for i in range(self.row):
            for j in range(self.col):
                if self.tiles[i][j] == -1:
                    self.tiles[i][j] = 0
        for i in range(self.row):
            for j in range(self.col):
                if self.tiles[i][j] == self.offense:
                    for dx, dy in directions:
                        checking_i = i + dy
                        checking_j = j + dx
                        find_one_reverse_color = False
                        while 0 <= checking_i < self.row and 0 <= checking_j < self.col:
                            chess = self.tiles[checking_i][checking_j]
                            if chess == color_reverse:
                                checking_i += dy
                                checking_j += dx
                                find_one_reverse_color = True
                            elif chess == 0 and find_one_reverse_color:
                                self.tiles[checking_i][checking_j] = -1
                                self.available.append((checking_i, checking_j))
                                break
                            else:
                                break

    def reverse(self, set_i, set_j):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, -1), (1, -1), (-1, 1)]
        color_reverse = self.offense
        color = 3 - color_reverse
        for dx, dy in directions:
            checking_i = set_i + dy
            checking_j = set_j + dx
            while 0 <= checking_i < self.row and 0 <= checking_j < self.col:
                chess = self.tiles[checking_i][checking_j]
                if chess == color_reverse:
                    checking_i += dy
                    checking_j += dx
                elif chess == color:
                    reversing_i = set_i + dy
                    reversing_j = set_j + dx
                    while (reversing_i, reversing_j) != (checking_i, checking_j):
                        self.tiles[reversing_i][reversing_j] = color
                        reversing_i += dy
                        reversing_j += dx
                    break
                else:
                    break

    def updateStable(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        find_new_stable_chess = True
        while find_new_stable_chess:
            find_new_stable_chess = False
            self.count_total_stable_direct_black = 0
            self.count_total_stable_direct_white = 0
            for i in range(self.row):
                for j in range(self.col):
                    if (self.tiles[i][j] == 1 or self.tiles[i][j] == 2) and not self.stable[i][j]:
                        count_stable_direction = 0
                        for direction in directions:
                            if self.checkDirectionStable(i, j, direction):
                                count_stable_direction += 1
                        if count_stable_direction == 4:
                            find_new_stable_chess = True
                            self.stable[i][j] = 1
                        else:
                            if self.tiles[i][j] == 1:
                                self.count_total_stable_direct_white += count_stable_direction
                            elif self.tiles[i][j] == 2:
                                self.count_total_stable_direct_black += count_stable_direction

    def checkDirectionStable(self, i, j, direction):
        directions = [direction, (-direction[0], -direction[1])]
        color = self.tiles[i][j]
        color_reverse = 3 - color
        count_tmp = 0
        for dx, dy in directions:
            find_unstable_chess = False
            checking_i = i + dy
            checking_j = j + dx
            while True:
                if not (0 <= checking_i < self.row and 0 <= checking_j < self.col):
                    if find_unstable_chess:
                        count_tmp += 1
                        break
                    else:
                        return True
                if self.tiles[checking_i][checking_j] == color:
                    if self.stable[checking_i][checking_j]:
                        return True
                    else:
                        checking_i += dy
                        checking_j += dx
                        find_unstable_chess = True
                elif self.tiles[checking_i][checking_j] == color_reverse:
                    if self.stable[checking_i][checking_j]:
                        count_tmp += 1
                        break
                    else:
                        checking_i += dy
                        checking_j += dx
                        find_unstable_chess = True
                else:
                    break
        if count_tmp == 2:
            return True
        else:
            return False

    def updateCount(self):
        self.count_black = 0
        self.count_white = 0
        self.count_available = 0
        self.count_stable_white = 0
        self.count_stable_black = 0
        for i in range(self.row):
            for j in range(self.col):
                chess = self.tiles[i][j]
                if chess == 1:
                    self.count_white += 1
                elif chess == 2:
                    self.count_black += 1
                elif chess == -1:
                    self.count_available += 1
                if self.stable[i][j] == 1:
                    if self.tiles[i][j] == 1:
                        self.count_stable_white += 1
                    elif self.tiles[i][j] == 2:
                        self.count_stable_black += 1
    
    def copy(self):
        othello_board_new = Othello_board()
        othello_board_new.offense = self.offense
        othello_board_new.available = [item for item in self.available]
        for i in range(self.row):
            for j in range(self.col):
                othello_board_new.tiles[i][j] = self.tiles[i][j]
                othello_board_new.stable[i][j] = self.stable[i][j]
        othello_board_new.count_black = self.count_black
        othello_board_new.count_white = self.count_white
        othello_board_new.count_available = self.count_available
        othello_board_new.count_stable_black = self.count_stable_black
        othello_board_new.count_stable_white = self.count_stable_white
        othello_board_new.count_total_stable_direct_black = self.count_total_stable_direct_black
        othello_board_new.count_total_stable_direct_white = self.count_total_stable_direct_white
        return othello_board_new


def setChess(Othello_board, px, py):

    set_i = (py - Othello_board.margin) // Othello_board.width
    set_j = (px - Othello_board.margin) // Othello_board.width

    othello_board_new = None

    if 0 <= set_i < Othello_board.row and 0 <= set_j < Othello_board.col and \
    Othello_board.tiles[set_i][set_j] == -1:
        othello_board_new = Othello_board.copy()
        othello_board_new.tiles[set_i][set_j] = Othello_board.offense
        othello_board_new.offense = 3 - Othello_board.offense
        othello_board_new.reverse(set_i, set_j)
        othello_board_new.updateAvailable()
        othello_board_new.updateStable()
        othello_board_new.updateCount()

        if othello_board_new.count_available == 0:
            othello_board_new.offense = 3 - othello_board_new.offense
            othello_board_new.updateAvailable()
            othello_board_new.updateCount()

    return othello_board_new

#Displayed Images
class Images:

    def __init__(self):
        self.width = 50
        self.background = pygame.image.load('images/background.png')

        #Tiles and Disks
        self.tile = pygame.image.load('images/tile.png')
        self.blank_tile = pygame.transform.scale(self.tile, (self.width, self.width))

        self.options = pygame.image.load('images/options.png')
        self.available = pygame.transform.scale(self.options, (self.width, self.width))

        self.blackdisk = pygame.image.load('images/black_disk.png')
        self.black = pygame.transform.scale(self.blackdisk, (self.width, self.width))

        self.whitedisk = pygame.image.load('images/white_disk.png')
        self.white = pygame.transform.scale(self.whitedisk, (self.width, self.width))

        #Buttons
        self.undo_button = pygame.image.load('images/undo_button.png').convert_alpha()
        self.undo = pygame.transform.scale(self.undo_button, (self.width * 2, self.width))
        #self.restart_button = pygame.image.load('images/restart_button.png').convert_alpha()
        #self.restart = pygame.transform.scale(self.restart_button, (self.width * 2, self.width))

def draw(screen, images, othello_board):

    screen.blit(images.background, (0, 0))

    width = othello_board.width
    row = othello_board.row
    col = othello_board.col
    margin = othello_board.margin
    for i in range(row + 1):
        for j in range(col + 1):
            pygame.draw.line(screen, (0, 0, 0),
                             (margin + i * width, margin),
                             (margin + i * width, margin + col * width))
            pygame.draw.line(screen, (0, 0, 0),
                             (margin, margin + j * width),
                             (margin + row * width, margin + j * width))

    for i in range(row):
        for j in range(col):
            color = images.blank_tile
            chess = othello_board.tiles[i][j]
            if chess == 1:
                color = images.white
            elif chess == 2:
                color = images.black
            elif chess == -1:
                color = images.available
            screen.blit(color, (margin + j * width + width // 2 - images.width // 2,
                                margin + i * width + width // 2 - images.width // 2))
    
    pos = margin * 2.5 + othello_board.width * col
    if othello_board.offense == 1:
        screen.blit(images.black, (pos - 70, pos // 3 + images.width * 2))
        screen.blit(images.white, (pos - 70, pos // 2 + images.width * 1))
        screen.blit(images.available, (pos - 70, pos // 3.3 + images.width))
    else:
        screen.blit(images.black, (pos - 70, pos // 3 + images.width * 2))
        screen.blit(images.white, (pos - 70, pos // 2 + images.width * 1))
        screen.blit(images.available, (pos - 70, pos // 3.3 + images.width))
    
    textSurfaceObj = FONT.render(str(othello_board.count_black), True, DARKTURQUOISE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 3.5, pos // 2.3 + images.width)
    screen.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = FONT.render(str("Player:"), True, DEEPPINK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width + 20, pos // 2.3 + images.width)
    screen.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = FONT.render(str(othello_board.count_white), True, DARKTURQUOISE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 3.5, pos // 1.89 + images.width)
    screen.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = FONT.render(str("AI:"), True, DEEPPINK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width + 20, pos // 1.89 + images.width)
    screen.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = FONT.render(str(othello_board.count_available), True, DARKTURQUOISE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width * 3.5, pos // 3 + images.width)
    screen.blit(textSurfaceObj, textRectObj)

    textSurfaceObj = FONT.render(str("Available:"), True, DEEPPINK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos + images.width + 20, pos // 3 + images.width)
    screen.blit(textSurfaceObj, textRectObj)

    screen.blit(images.undo, (660,490))
    #screen.blit(images.restart, (810,490))


class Othello_boardTreeNode:

    def __init__(self, othello_board):
        self.parent = None
        self.kids = {}
        self.othello_board = othello_board

    def getScore(self):
        othello_board = self.othello_board
        return 100 * (othello_board.count_stable_white - othello_board.count_stable_black) \
            + (othello_board.count_total_stable_direct_white
               - othello_board.count_total_stable_direct_black)


class Othello_boardTree:

    def __init__(self, node):
        self.root = node
        self.expandLayer = 5

    def expandTree(self):
        node = self.root
        for i, j in node.othello_board.available:
            if (i, j) not in node.kids:
                othello_board_new = setChessAI(node.othello_board, i, j)
                node_new = Othello_boardTreeNode(othello_board_new)
                node.kids[(i, j)] = node_new
                node_new.parent = node

    def findBestChess(self, player_color):
        scores = {}
        alpha = -6400
        for key in self.root.kids:
            score = self.MaxMin(self.root.kids[key], player_color,
                                self.expandLayer - 1, alpha)
            scores.update({key: score})
            if alpha < score:
                alpha = score
        if not scores:
            return (-1, -1)
        max_key = max(scores, key=scores.get)
        min_key = min(scores, key=scores.get)
        #print(scores[min_key], scores[max_key])
        return max_key

    def MaxMin(self, node, player_color, layer, pruning_flag):
        if layer and node.othello_board.available:
            if node.othello_board.offense == player_color:
                beta = 6400
                for i, j in node.othello_board.available:
                    if (i, j) in node.kids:
                        score = self.MaxMin(
                            node.kids[(i, j)], player_color, layer - 1, beta)
                    else:
                        othello_board_new = setChessAI(node.othello_board, i, j)
                        node_new = Othello_boardTreeNode(othello_board_new)
                        node.kids[(i, j)] = node_new
                        node_new.parent = node
                        score = self.MaxMin(
                            node_new, player_color, layer - 1, beta)
                    if score <= pruning_flag:
                        beta = score
                        break
                    if beta > score:
                        beta = score
                return beta
            else:
                alpha = -6400
                for i, j in node.othello_board.available:
                    if (i, j) in node.kids:
                        score = self.MaxMin(
                            node.kids[(i, j)], player_color, layer - 1, alpha)
                    else:
                        othello_board_new = setChessAI(node.othello_board, i, j)
                        node_new = Othello_boardTreeNode(othello_board_new)
                        node.kids[(i, j)] = node_new
                        node_new.parent = node
                        score = self.MaxMin(
                            node_new, player_color, layer - 1, alpha)
                    if score >= pruning_flag:
                        alpha = score
                        break
                    if alpha < score:
                        alpha = score
                return alpha
        else:
            node.othello_board.updateStable()
            node.othello_board.updateCount()
            score = node.getScore()
            return score


def setChessAI(othello_board, set_i, set_j):

    othello_board_new = None

    if 0 <= set_i < othello_board.row and 0 <= set_j < othello_board.col and \
            othello_board.tiles[set_i][set_j] == -1:
        othello_board_new = othello_board.copy()
        othello_board_new.tiles[set_i][set_j] = othello_board.offense
        othello_board_new.offense = 3 - othello_board.offense
        othello_board_new.reverse(set_i, set_j)
        othello_board_new.updateAvailable()
        othello_board_new.updateCount()

        if othello_board_new.count_available == 0:
            othello_board_new.offense = 3 - othello_board_new.offense
            othello_board_new.updateAvailable()

    return othello_board_new

#Buttons Clicking
class Button():
    def __init__(self, x,y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()  [0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

def main():    
    images = Images()

    othello_board = Othello_board()

    node = Othello_boardTreeNode(othello_board)
    othello_boardTree = Othello_boardTree(node)
    othello_boardTree.expandTree()

    draw(screen, images, othello_board)
    undo_button = Button(700, 620, images.undo, 1)
    pygame.display.update()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONUP:
                set_i = set_j = -1
                if othello_board.offense == player_color:
                    px, py = pygame.mouse.get_pos()
                    set_i = (py - othello_board.margin) // othello_board.width
                    set_j = (px - othello_board.margin) // othello_board.width
                if (set_i, set_j) in othello_board.available:
                    othello_boardTree.root = othello_boardTree.root.kids[(
                        set_i, set_j)]
                    othello_board = othello_boardTree.root.othello_board
                    draw(screen, images, othello_board)
                    pygame.display.update()
                    othello_boardTree.expandTree()
                hold = deepcopy(othello_boardTree.root.parent)
                
            set_i = set_j = -1
            if othello_board.offense != player_color:
                set_i, set_j = othello_boardTree.findBestChess(player_color)
            if (set_i, set_j) in othello_board.available:
                othello_boardTree.root = othello_boardTree.root.kids[(
                    set_i, set_j)]
                othello_board = othello_boardTree.root.othello_board
                draw(screen, images, othello_board)
                pygame.display.update()
                othello_boardTree.expandTree()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos1 = pygame.mouse.get_pos()
                if pos1[0] > 685 and pos1[0] < 795 and pos1[1] > 480 and pos1[1] < 530:
                    if othello_boardTree.root.parent:
                        othello_boardTree.root = hold
                        othello_board = othello_boardTree.root.othello_board
                elif pos1[0] > 685 and pos1[0] < 795 and pos1[1] > 550 and pos1[1] < 600:
                    othello_board = Othello_board()
                    node = Othello_boardTreeNode(othello_board)
                    othello_boardTree = Othello_boardTree(node)
                    othello_boardTree.expandTree()
                draw(screen, images, othello_board)
                pygame.display.update()


if __name__ == "__main__":
    main()