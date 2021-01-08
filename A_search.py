import pygame
from queue import PriorityQueue

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

tot_width_r = 600
tot_width_c = 600

class Point:
	
	def __init__(self,row,col,tot_rows,tot_cols,width_r,width_c):
		self.row         = row
		self.col         = col
		self.total_cols  = tot_cols
		self.total_rows  = tot_rows
		self.y           = self.row * width_r
		self.x           = self.col * width_c
		self.width_c     = width_c
		self.width_r     = width_r
		self.color       = WHITE
		self.neighbors   = []

	def is_barrier(self):
		return self.color == BLACK
	def make_start(self):
		self.color = ORANGE
	def make_end(self):
		self.color = TURQUOISE
	def make_barrier(self):
		self.color = BLACK
	def get_pos(self):
		return self.row,self.col


	def draw(self,win):
		pygame.draw.rect(win, self.color,(self.x,self.y,self.width_r,self.width_c))

	def get_neighbors(self,grid):

		if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): # up
			self.neighbors.append(grid[self.row-1][self.col])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # left
			self.neighbors.append(grid[self.row][self.col - 1])

		if self.row + 1 < self.total_rows and not grid[self.row + 1][self.col].is_barrier(): # down
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.col + 1 < self.total_cols and not grid[self.row][self.col+1].is_barrier(): # down
			self.neighbors.append(grid[self.row][self.col+1])




def make_grid(rows,cols):
	grid = []
	width_r = tot_width_r//rows
	width_c = tot_width_c//cols
	for i in range(rows):
		grid.append([])
		for j in range(cols):
			point = Point(i,j,rows,cols,width_r,width_c)
			grid[i].append(point)
	return grid

def draw_grid(win,rows,cols):
	width_r = tot_width_r//rows
	width_c = tot_width_c//cols
	for i in range(rows):
		pygame.draw.line(win,GREY,(0,i*width_r),(tot_width_c,i*width_r))
		for j in range(cols):
			pygame.draw.line(win,GREY,(j*width_c,0),(j*width_c,tot_width_r))

def draw(win,rows,cols,grid):
	win.fill(WHITE)
	for row in grid:
		for point in row:
			point.draw(win)
	draw_grid(win,rows,cols)
	pygame.display.update()

def h(p1,p2):
	return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def reconstruct_path(come_from,current):
	while current in come_from:
		current.color = PURPLE
		current = come_from[current]

def algorithm(draw,start,end,grid):
	open_set = PriorityQueue()
	open_set_hash = {start}
	came_from = {}
	count = 0
	f_score = {point : float("inf") for row in grid for point in row}
	g_score = {point : float("inf") for row in grid for point in row}
	g_score[start] = 0
	f_score[start] = h(start.get_pos(),end.get_pos())
	open_set.put((0,count,start))

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
				# print("ff")
				return False
		current = open_set.get()[2] 
		tmp_g_score = g_score[current] + 1
		open_set_hash.remove(current)
		if current==end:
			reconstruct_path(came_from,current)
			end.make_end()
			return True


		for neighbor in current.neighbors:
			if g_score[neighbor] > tmp_g_score:
				
				g_score[neighbor] =  tmp_g_score
				f_score[neighbor] = tmp_g_score + h(neighbor.get_pos(),end.get_pos())
				came_from[neighbor] = current

				if neighbor not in open_set_hash:
					open_set_hash.add(neighbor)
					count +=1
					open_set.put((f_score[neighbor],count,neighbor))
					if neighbor != end:
						neighbor.color = GREEN
		draw()

		if current != start:
			current.color = RED

	return True 





def main(rows,cols):

	win = pygame.display.set_mode((tot_width_r,tot_width_c))
	pygame.display.set_caption("Path finding algorithm")
	width_c = tot_width_c // cols
	width_r = tot_width_r // rows
	run = True
	grid = make_grid(rows,cols)	
	start,end = None,None
	running = False
	while run:
		draw(win,rows,cols,grid)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]:
				x,y = pygame.mouse.get_pos()
				row,col = y // width_r,x // width_c
				# print(x,y,row,col)
				point = grid[row][col]
				if point.color != WHITE or running:
					continue

				if not start:
					start = point
					point.make_start() 
				elif not end:
					end = point
					point.make_end()
				else:
					point.make_barrier()

			if pygame.mouse.get_pressed()[2]:
				

			if pygame.mouse.get_pressed()[2]: #left
				x,y = pygame.mouse.get_pos()
				row,col = y // width_r,x // width_c
				point = grid[row][col]
				point.color = WHITE
				if start == point:
					start = None
				if point == end:
					end = None
			
			if event.type == pygame.KEYDOWN:
				status = True
				if event.key == pygame.K_r and start and end and  not running:
					running = True
					for row in grid:
						for point in row:
							point.get_neighbors(grid)

					status = algorithm(lambda:draw(win,rows,cols,grid),start,end,grid)
					
				if event.key == pygame.K_c or status == False:
					# print("gg")
					start = None
					end = None
					running = False
					grid = make_grid(rows,cols)








	pygame.quit()

main(50,50)