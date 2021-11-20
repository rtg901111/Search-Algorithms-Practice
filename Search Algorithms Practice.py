from collections import defaultdict
import math
import heapq

ACTION_CONVERSION = {1: [1, 0, 0], 2: [-1, 0, 0], 3: [0, 1, 0], 4: [0, -1, 0], 5: [0, 0, 1], 6: [0, 0, -1], 
                     7: [1, 1, 0], 8: [1, -1, 0], 9: [-1, 1, 0], 10: [-1, -1, 0], 11: [1, 0, 1], 12: [1, 0, -1],
                     13: [-1, 0, 1], 14: [-1, 0, -1], 15: [0, 1, 1], 16: [0, 1, -1], 17: [0, -1, 1], 18: [0, -1, -1]}

#Graph = {[Node]: {[Adjacent Node]: Edge Cost}}
GRAPH = defaultdict(dict)

def read_input(file_name = 'input.txt'):

    line_count = 1
    file = open(file_name, "r")
    for line in file:
        if line_count == 1:
            algorithm = line.split()[0]
        elif line_count == 2:
            dimensions = line.split()
            for i in range(len(dimensions)):
                dimensions[i] = int(dimensions[i])
        elif line_count == 3:
            entrance_grid = line.split()
            for i in range(len(entrance_grid)):
                entrance_grid[i] = int(entrance_grid[i])
            entrance_grid = tuple(entrance_grid)
        elif line_count == 4:
            exit_grid = line.split()
            for i in range(len(exit_grid)):
                exit_grid[i] = int(exit_grid[i])
            exit_grid = tuple(exit_grid)
        elif line_count == 5:
            N = int(line)  
        else:
            line = line.split()
            for i in range(3):
                line[i] = int(line[i])
            grid = line[0:3]
            #actions = line[3:]

            adjacent_grid = [0, 0, 0]
            #for action in actions:
            #    action = int(action)
            for i in range(3, len(line)):
                action = int(line[i])
                action_valid = True
                conversion = ACTION_CONVERSION[action] 
                for i in range(len(adjacent_grid)):
                    adjacent_grid[i] = grid[i] + conversion[i]
                
                for i in range(len(adjacent_grid)):
                    if adjacent_grid[i] < 0 or adjacent_grid[i] >= dimensions[i]:
                        action_valid = False
                
                if action_valid == True:
                    #GRAPH[tuple(grid)] = dict()
                    if algorithm != "BFS":
                        if action > 6:
                            GRAPH[tuple(grid)][tuple(adjacent_grid)] = 14
                        else:
                            GRAPH[tuple(grid)][tuple(adjacent_grid)] = 10
                    else:
                        GRAPH[tuple(grid)][tuple(adjacent_grid)] = 1
        
        line_count += 1
    file.close()

    return algorithm, dimensions, entrance_grid, exit_grid, N


def breadth_first_search(entrance_grid: tuple, exit_grid: tuple):
    #Each element in visited is grid points
    visited = dict()
 
    #Each element in queue is a list: [(grid_coordinate), cumulative cost, total steps]
    queue = deque()
    queue.append([entrance_grid, 0, 1])
    
    visited[entrance_grid] = None #visited = {child: parent}

    failed = False

    while len(queue) > 0:

        curr_element = queue.popleft()
        curr_grid = curr_element[0]
        if curr_grid == exit_grid:
            'Done'
            return curr_element[1], curr_element[2], visited, exit_grid, failed
            #generate_output(curr_element[1], curr_element[2], lineage, exit_grid, failed)
            #print("Success generated")
            #return

        for child in GRAPH[curr_grid].keys():
            if child not in visited:
                queue.append([child, curr_element[1] + 1, curr_element[2] + 1])
                #visited.append(child)
                visited[child] = curr_grid
                #lineage[child] = curr_grid

                if child == exit_grid: #Done
                    return curr_element[1] + 1, curr_element[2] + 1, visited, exit_grid, failed

    failed = True
    return curr_element[1], curr_element[2], visited, exit_grid, failed
    #generate_output(curr_element[1], curr_element[2], lineage, exit_grid, failed)
    #print("Failure generated")
    #return  

def uniform_cost_search(entrance_grid: tuple, exit_grid: tuple):
    #Each element in visited is grid points
    visited = dict()

    #Each element in queue is a list: [(grid_coordinate), cumulative cost, total steps]
    #queue = deque()
    queue = []
    queue.append([0, entrance_grid, 1]) #New element: [cumulative cost, (grid_coordinate), total steps]
    heapq.heapify(queue)
    
    visited[entrance_grid] = None 

    lineage = dict() #lineage = {child: parent}  
    lineage[entrance_grid] = None 

    failed = False
    queue_set = set()
    queue_set.add(entrance_grid)
    while len(queue) > 0:
        #sort
        #queue = deque(sorted(queue, key = lambda x: x[1]))

        #curr_element = queue.popleft()
        curr_element = heapq.heappop(queue)
        curr_grid = curr_element[1]
        if curr_grid == exit_grid:
            'Done'
            generate_output(curr_element[0], curr_element[2], lineage, exit_grid, failed)
            return
        
        queue_set.remove(curr_grid)
        visited[curr_grid] = None 

        for child in GRAPH[curr_grid].keys():
            if child not in visited and child not in queue_set:
                #queue.append([child, curr_element[1] + GRAPH[curr_grid][child], curr_element[2] + 1])
                heapq.heappush(queue, [curr_element[0] + GRAPH[curr_grid][child], child, curr_element[2] + 1])
                lineage[child] = curr_grid
                queue_set.add(child)
                continue
            
            if child in queue_set:
                for element in queue:
                    if element[1] == child and element[0] > curr_element[0] + GRAPH[curr_grid][child]:
                        element[0] = curr_element[0] + GRAPH[curr_grid][child]
                        element[2] = curr_element[2] + 1
                        lineage[child] = curr_grid
            
            heapq.heapify(queue)

    failed = True
    generate_output(curr_element[0], curr_element[2], lineage, exit_grid, failed)
    return

def a_heuristic_search(entrance_grid: tuple, exit_grid: tuple):
    #Each element in visited is grid points
    visited = dict()

    #Each element in queue is a list: [(grid_coordinate), cumulative cost, total steps, f score]
    #queue = deque()
    queue = []
    #queue.append([entrance_grid, 0, 1, 0 + heuristic(entrance_grid, exit_grid)])
    queue.append([0 + heuristic(entrance_grid, exit_grid), 0, 1, entrance_grid])  #New element is [f score, cumulative cost, total steps, (grid_coordinate)]
    heapq.heapify(queue)
    #visited.append(entrance_grid)
    visited[entrance_grid] = None 

    lineage = dict() #lineage = {child: parent}
    lineage[entrance_grid] = None 

    failed = False
    queue_set = set()
    queue_set.add(entrance_grid)
    while len(queue) > 0:
        #sort
        #queue = deque(sorted(queue, key = lambda x: x[3]))

        #curr_element = queue.popleft()
        curr_element = heapq.heappop(queue)
        curr_grid = curr_element[3]
        if curr_grid == exit_grid:
            'Done'
            generate_output(curr_element[1], curr_element[2], lineage, exit_grid, failed)
            return

        queue_set.remove(curr_grid)
        visited[curr_grid] = None
        

        for child in GRAPH[curr_grid].keys():
            if child not in visited and child not in queue_set:
                #queue.append([child, curr_element[1] + GRAPH[curr_grid][child], curr_element[2] + 1, curr_element[1] + GRAPH[curr_grid][child] + heuristic(child, exit_grid)])
                heapq.heappush(queue, [curr_element[1] + GRAPH[curr_grid][child] + heuristic(child, exit_grid), curr_element[1] + GRAPH[curr_grid][child], curr_element[2] + 1, child])
                lineage[child] = curr_grid
                queue_set.add(child)
                continue
            
            if child in queue_set:
                for element in queue: 
                    if element[3] == child and element[0] > curr_element[1] + GRAPH[curr_grid][child] + heuristic(child, exit_grid):
                        element[0] = curr_element[1] + GRAPH[curr_grid][child] + heuristic(child, exit_grid)
                        element[1] = curr_element[1] + GRAPH[curr_grid][child]
                        element[2] = curr_element[2] + 1
                        lineage[child] = curr_grid
                    
            heapq.heapify(queue)

    failed = True
    generate_output(curr_element[1], curr_element[2], lineage, exit_grid, failed)
    return

def heuristic(child_node: tuple, exit_node: tuple):
    temp_list = []
    for i in range(len(exit_node)):
        temp_list.append((exit_node[i] - child_node[i]) ** 2)
    return int(math.sqrt(sum(temp_list)))


def generate_output(total_cost: int, total_steps: int, lineage: dict, exit_grid: tuple, failed: bool):
    if failed == True:
        file = open("output.txt", "w")
        file.write("FAIL")
        file.close()
        return

    lineage_list = []
    child = exit_grid
    #while child in lineage:
    while lineage[child] != None:
        parent = lineage[child]
        lineage_list.append((child, GRAPH[parent][child]))
        child = parent
    
    lineage_list.append((child, 0))

    file = open("output.txt", "w")

    file.write(str(total_cost) + "\n")
    file.write(str(total_steps) + "\n")

    for i in range(len(lineage_list)-1, -1, -1):
        line = ""
        for j in range(len(lineage_list[i][0])):
            line += str(lineage_list[i][0][j]) + " "
        line += str(lineage_list[i][1])
        file.write(line)

        if i > 0:
            file.write("\n")
    
    file.close()
    return

if __name__ == "__main__":
    algorithm, dimensions, entrance_grid, exit_grid, N = read_input('input.txt')
 
    if algorithm == 'BFS':
        total_cost, total_steps, lineage, exit_grid, failed = breadth_first_search(entrance_grid, exit_grid)
        generate_output(total_cost, total_steps, lineage, exit_grid, failed) 

    elif algorithm == "UCS":
        uniform_cost_search(entrance_grid, exit_grid)

    elif algorithm == "A*": 
        a_heuristic_search(entrance_grid, exit_grid)

         
