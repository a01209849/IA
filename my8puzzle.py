import random
import heapq
import sys

class Puzzle:

    def __init__(self):
        #Size of the puzzle
        self.n = 3
        self.matrix = [[-1 for x in range(self.n)] for y in range(self.n)]
        array = []
        self.level = 0
        self.childu = 0
        self.childr = 0
        self.childd = 0
        self.childl = 0
        self.id = 0

        #goal1
        #hard 15 sec
        #self.matrix = [[8,6,7],[2,5,4],[3,0,1]]

        #medium
        #self.matrix = [[3,1,7],[5,4,8],[6,2,0]]

        #easy
        #self.matrix = [[4,1,3],[7,0,5],[8,2,6]]
        #self.matrix = [[0,1,3],[4,2,5],[7,8,6]]

        #goal2
        #self.matrix = [[2,0,3],[5,1,4],[6,8,7]]

        #goal3
        #self.matrix = [[3,6,4],[0,1,2],[8,7,5]]

        #First state is the goal1
        #self.matrix = [[1,2,3],[4,5,6],[7,8,0]]

        #Not solvable goal1
        #self.matrix = [[8,1,2],[0,4,3],[7,6,5]]


        for x in range(self.n):
            for y in range(self.n):
                r = random.randrange(0,self.n*self.n)
                while r in array:
                    r = random.randrange(0,self.n*self.n)
                self.matrix[x][y] = r
                array.append(r)
        

    def isGoal(self, goal):
        for i in range(self.n):
          for j in range(self.n):
              if goal[i][j] != self.matrix[i][j]:
                  return False

        return True

    def print_puzzle(self):
        for i in range(self.n):
          for j in range(self.n):
            if j !=(self.n - 1):
               print(self.matrix[i][j], end = " ")
            else:
               print(self.matrix[i][j], end = "")
          if i!=(self.n - 1):
            print()
        print("\n")

    def coordZero(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j] == 0:
                    return i, j

    def numChild(self):
        x, y = self.coordZero()

        if (x == 0 and y == 0) or (x == self.n - 1 and y == self.n - 1) or (x == self.n - 1 and y == 0) or (x == 0 and y == self.n - 1):
            return 2
        elif x == 0 or x == self.n - 1 or y == 0 or y == self.n - 1:
            return 3
        else:
            return 4

    def nextMatrix(self):
        x, y = self.coordZero()
        mat = [[-1 for x in range(self.n)] for y in range(self.n)]
        for i in range(self.n):
          for j in range(self.n):
              mat[i][j] = self.matrix[i][j]

        if self.childu == 0 and x - 1 >= 0:
            mat[x][y] = self.matrix[x - 1][y]
            mat[x - 1][y] = 0
            self.childu = 1
        elif self.childr == 0 and y + 1 < self.n:
            mat[x][y] = self.matrix[x][y + 1]
            mat[x][y + 1] = 0
            self.childr = 1
        elif self.childd == 0 and x + 1 < self.n:
            mat[x][y] = self.matrix[x + 1][y]
            mat[x + 1][y] = 0
            self.childd = 1
        elif self.childl == 0 and y - 1 >= 0:
            mat[x][y] = self.matrix[x][y - 1]
            mat[x][y - 1] = 0
            self.childl = 1

        return mat

    def solvable(self):
        count = 0

        array = [-1,-1,-1,-1,-1,-1,-1,-1,-1]
        k = 0
        for i in range(3):
            for j in range(3):
                array[k] = self.matrix[i][j]
                k = k + 1

        for i in range(8):
            for j in range(i+1, 9):
                if array[j] and array[i] and array[i] > array[j]:
                    count += 1

        return count % 2 == 0

"""-----------------------------------PUZZLE-END------------------------------------"""

class Node:
    def __init__(self, matrix, i, n, parent, level):
        self.matrix = matrix
        self.id = i
        self.n = n
        self.manhattan = 0
        self.parent = parent
        self.level = level
        self.childu = 0
        self.childr = 0
        self.childd = 0
        self.childl = 0

    def isGoal(self, goal):
        if self.matrix == goal:
            return True
        else:
            return False

    def findNumber(self, number, goal):
        for i in range(self.n):
            for j in range(self.n):
                if goal[i][j] == number:
                    return i, j

    def manhattanDistance(self, goal):
        h = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j] != 0:
                    if self.matrix[i][j] != goal[i][j]:
                        x, y = self.findNumber(self.matrix[i][j], goal)
                        h = h + (abs(i - x) + abs(j - y))
        self.manhattan = h + self.level

    def print_node(self):
        for i in range(self.n):
          for j in range(self.n):
            if j !=(self.n - 1):
               print(self.matrix[i][j], end = " ")
            else:
               print(self.matrix[i][j], end = "")
          if i!=(self.n - 1):
            print()
        print("\n")

    def coordZero(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j] == 0:
                    return i, j

    def numChild(self):
        x, y = self.coordZero()

        if (x == 0 and y == 0) or (x == self.n - 1 and y == self.n - 1) or (x == self.n - 1 and y == 0) or (x == 0 and y == self.n - 1):
            return 2
        elif x == 0 or x == self.n - 1 or y == 0 or y == self.n - 1:
            return 3
        else:
            return 4

    def nextMatrix(self):
        x, y = self.coordZero()
        mat = [[-1 for x in range(self.n)] for y in range(self.n)]
        for i in range(self.n):
          for j in range(self.n):
              mat[i][j] = self.matrix[i][j]

        if self.childu == 0 and x - 1 >= 0:
            mat[x][y] = self.matrix[x - 1][y]
            mat[x - 1][y] = 0
            self.childu = 1
        elif self.childr == 0 and y + 1 < self.n:
            mat[x][y] = self.matrix[x][y + 1]
            mat[x][y + 1] = 0
            self.childr = 1
        elif self.childd == 0 and x + 1 < self.n:
            mat[x][y] = self.matrix[x + 1][y]
            mat[x + 1][y] = 0
            self.childd = 1
        elif self.childl == 0 and y - 1 >= 0:
            mat[x][y] = self.matrix[x][y - 1]
            mat[x][y - 1] = 0
            self.childl = 1

        return mat

    def nodeVisited(self, existingNodes):
        for node in existingNodes:
            if node.matrix == self.matrix:
                return True
        return False


    def __repr__(self):
        return repr((self.matrix, self.id, self.manhattan))
""" ----------------------------------NODE-END------------------------------------ """

#goal1
goal = [[1,2,3],[4,5,6],[7,8,0]]
#goal2
#goal = [[1,4,7],[2,5,8],[3,6,0]]
#goal3
#goal = [[1,2,3],[8,0,4],[7,6,5]]

puzzle = Puzzle()
print("First state.\n")
puzzle.print_puzzle()

if puzzle.isGoal(goal) == True:
    print("The first state is the goal state.")
    sys.exit()

if goal == [[1,2,3],[4,5,6],[7,8,0]] and puzzle.solvable() == True:
    print("The puzzle is solvable.\n")
else:
    print("The puzzle is not solvable.\n")
    sys.exit()

priorityNode = []
existingNodes = []
id = 1

for i in range(puzzle.numChild()):
    node = Node(puzzle.nextMatrix(), id, puzzle.n, puzzle, (puzzle.level + 1))
    node.manhattanDistance(goal)
    if node.nodeVisited(existingNodes) == False:
        priorityNode.append(node)
        existingNodes.append(node)
        id = id + 1

priorityNode.sort(key=lambda node: node.manhattan)
priorityNode.reverse()
if len(priorityNode) != 0:
    nodeN = priorityNode.pop()

while nodeN.isGoal(goal) == False:
    for i in range(nodeN.numChild()):
        node = Node(nodeN.nextMatrix(), id, nodeN.n, nodeN, nodeN.level + 1)
        node.manhattanDistance(goal)
        if node.nodeVisited(existingNodes) == False:
            priorityNode.append(node)
            existingNodes.append(node)
            id = id + 1

    priorityNode.sort(key=lambda node: node.manhattan)
    priorityNode.reverse()
    if len(priorityNode) != 0:
        nodeN = priorityNode.pop()

path = []
while True:
    path.append(nodeN)
    nodeN = nodeN.parent
    if nodeN.id == 0:
        break

path.reverse()

for n in path:
    if n.id == 0:
        n.print_puzzle()
    else:
        n.print_node()
