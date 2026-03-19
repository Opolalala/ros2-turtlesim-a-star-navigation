import math
import heapq

def A_Star(grid,start,goal):
  row = len(grid)
  col = len(grid[0])


  dist = [[math.inf for _ in range(col)] for _ in range(row)]
  dist[start[0]][start[1]] = 0

  directions = [(-1,0),(1,0),(0,-1),(0,1)]
  parent = [[None for _ in range(col)] for _ in range(row)]

  heap = [(0, start)]
  while heap:
    j, k = heapq.heappop(heap)
    if k[0] == goal[0] and k[1] == goal[1]:
      print("yay")
      break

    for d in directions:
      i = (d[0] + k[0], d[1] + k[1])

      if i[0] >= 0 and i[0]<row and i[1] >= 0 and i[1]<col:
        g = dist[k[0]][k[1]] + 1
        if dist[i[0]][i[1]] >  g and not grid[i[0]][i[1]] == 1:
          h = abs(goal[0]-i[0]) + abs(goal[1]-i[1])
          f = g + h
          heapq.heappush(heap, (f, i))
          dist[i[0]][i[1]] = g
          parent[i[0]][i[1]] = k

  cur_tuple = (goal[0], goal[1])
  path= [cur_tuple]

  while not (cur_tuple[0] == start[0] and cur_tuple[1] == start[1]):
    j = parent[cur_tuple[0]][cur_tuple[1]]
    cur_tuple = j
    path.append(cur_tuple)

  path.reverse()
  return path
