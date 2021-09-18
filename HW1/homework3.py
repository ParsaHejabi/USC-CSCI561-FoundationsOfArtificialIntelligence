import math
from math import inf
from queue import Queue

MAPPINGS = {1: (1, 0, 0), 2: (-1, 0, 0), 3: (0, 1, 0), 4: (0, -1, 0), 5: (0, 0, 1), 6: (0, 0, -1), 7: (1, 1, 0),
            8: (1, -1, 0), 9: (-1, 1, 0), 10: (-1, -1, 0), 11: (1, 0, 1), 12: (1, 0, -1), 13: (-1, 0, 1),
            14: (-1, 0, -1),
            15: (0, 1, 1), 16: (0, 1, -1), 17: (0, -1, 1), 18: (0, -1, -1)}


def read_input_file():
    """
    Reads input file called "input.txt" in the same directory as the python file line by line

    :return:
    A list in which every member is a line of input file
    """
    output = []
    input_file = open('input.txt', 'r')
    input_file_lines = input_file.readlines()

    for line in input_file_lines:
        line = line.strip()
        output.append(line)

    input_file.close()
    return output


def write_output_file(output_file_lines=None, fail=False):
    """
    Writes output file and solution of the problem to "output.txt" file in the same dictionary as the python file
    """
    output_file = open('output.txt', 'w')

    if fail is True:
        output_file.write("FAIL")
    else:
        if output_file_lines is None:
            output_file_lines = ['1\n', '2\n', '3']
        output_file.writelines(output_file_lines)
    output_file.close()


def tuple_to_string(my_tuple, cost, put_lf=False):
    output = ''
    for elem in my_tuple:
        output += f'{elem} '

    output += str(cost)
    if put_lf:
        output += '\n'

    return output


def euclidean_distance(first_tuple, second_tuple):
    return math.sqrt(math.pow(first_tuple[0] - second_tuple[0], 2) + math.pow(first_tuple[1] - second_tuple[1], 2)
                     + math.pow(first_tuple[2] - second_tuple[2], 2))


class CustomPriorityQueue:
    def __init__(self):
        self.priority_queue = {}

    def size(self):
        return len(self.priority_queue)

    def push(self, coordinates_tuple, cost):
        self.priority_queue[coordinates_tuple] = cost

    def pop(self):
        min_index = min(self.priority_queue, key=self.priority_queue.get)
        min_grid_point = self.priority_queue[min_index]
        del self.priority_queue[min_index]
        return [min_index, min_grid_point]

    def exists(self, coordinates_tuple):
        return coordinates_tuple in self.priority_queue.keys()

    def get(self, coordinates_tuple):
        return self.priority_queue.get(coordinates_tuple)

    def update(self, coordinates_tuple, new_cost):
        self.priority_queue[coordinates_tuple] = new_cost


input_file_list = read_input_file()
algorithm = input_file_list[0]
sizes = [int(item) for item in input_file_list[1].split()]
sizes = (sizes[0], sizes[1], sizes[2])
source_coordinates = [int(item) for item in input_file_list[2].split()]
source_coordinates = (source_coordinates[0], source_coordinates[1], source_coordinates[2])
dest_coordinates = [int(item) for item in input_file_list[3].split()]
dest_coordinates = (dest_coordinates[0], dest_coordinates[1], dest_coordinates[2])
n = int(input_file_list[4])
graph = {}
for i in range(n):
    graph_node = [int(item) for item in input_file_list[5 + i].split()]
    node_coordinates = (graph_node[0], graph_node[1], graph_node[2])
    graph[node_coordinates] = graph_node[3:]

if algorithm == 'BFS':
    visited = {}
    node_cost = {}
    father_node = {}

    for node in graph.keys():
        visited[node] = False
        node_cost[node] = inf
        father_node[node] = -1

    queue = Queue(maxsize=0)

    visited[source_coordinates] = True
    node_cost[source_coordinates] = 0
    father_node[source_coordinates] = -1

    queue.put(source_coordinates)
    while not queue.empty():
        front_node = queue.get()
        for action in graph[front_node]:
            next_node = (front_node[0] + MAPPINGS[action][0], front_node[1] + MAPPINGS[action][1],
                         front_node[2] + MAPPINGS[action][2])
            if next_node in graph and visited[next_node] is False:
                visited[next_node] = True
                node_cost[next_node] = node_cost[front_node] + 1
                father_node[next_node] = front_node
                queue.put(next_node)

                if next_node == dest_coordinates:
                    iterate_answer = dest_coordinates
                    answer = [tuple_to_string(iterate_answer, 1, False)]
                    while father_node[iterate_answer] != -1:
                        if father_node[iterate_answer] == source_coordinates:
                            answer.append(tuple_to_string(father_node[iterate_answer], 0, True))
                        else:
                            answer.append(tuple_to_string(father_node[iterate_answer], 1, True))
                        iterate_answer = father_node[iterate_answer]

                    answer.reverse()

                    answer_list = [f'{len(answer) - 1}\n', f'{len(answer)}\n'] + answer
                    write_output_file(answer_list, fail=False)
                    exit()

    write_output_file(fail=True)

elif algorithm == 'UCS':
    visited = {}
    node_cost = {}
    father_node = {}

    for node in graph.keys():
        visited[node] = False
        node_cost[node] = inf
        father_node[node] = -1

    priority_queue = CustomPriorityQueue()

    visited[source_coordinates] = True
    node_cost[source_coordinates] = 0
    father_node[source_coordinates] = -1

    priority_queue.push(source_coordinates, 0)
    while priority_queue.size() != 0:
        [top_node, top_node_cost] = priority_queue.pop()

        if top_node == dest_coordinates:
            iterate_answer = dest_coordinates
            answer = [tuple_to_string(iterate_answer, node_cost[iterate_answer], False)]
            while father_node[iterate_answer] != -1:
                if father_node[iterate_answer] == source_coordinates:
                    answer.append(tuple_to_string(father_node[iterate_answer], 0, True))
                else:
                    answer.append(
                        tuple_to_string(father_node[iterate_answer], node_cost[father_node[iterate_answer]], True))
                iterate_answer = father_node[iterate_answer]

            answer.reverse()

            answer_list = [f'{top_node_cost}\n', f'{len(answer)}\n'] + answer
            write_output_file(answer_list, fail=False)
            exit()
        else:
            visited[top_node] = True
            for action in graph[top_node]:
                next_node = (top_node[0] + MAPPINGS[action][0], top_node[1] + MAPPINGS[action][1],
                             top_node[2] + MAPPINGS[action][2])
                if next_node in graph and not (visited[next_node] is True or priority_queue.exists(next_node)):
                    if action <= 6:
                        priority_queue.push(next_node, top_node_cost + 10)
                        node_cost[next_node] = 10
                    else:
                        priority_queue.push(next_node, top_node_cost + 14)
                        node_cost[next_node] = 14
                    father_node[next_node] = top_node
                elif next_node in graph and priority_queue.exists(next_node):
                    if action <= 6:
                        if priority_queue.get(next_node) > top_node_cost + 10:
                            priority_queue.update(next_node, top_node_cost + 10)
                            node_cost[next_node] = 10
                            father_node[next_node] = top_node
                    else:
                        if priority_queue.get(next_node) > top_node_cost + 14:
                            priority_queue.update(next_node, top_node_cost + 14)
                            node_cost[next_node] = 14
                            father_node[next_node] = top_node

    write_output_file(fail=True)

elif algorithm == 'A*':
    visited = {}
    node_cost = {}
    father_node = {}

    for node in graph.keys():
        visited[node] = False
        node_cost[node] = inf
        father_node[node] = -1

    priority_queue = CustomPriorityQueue()

    visited[source_coordinates] = True
    node_cost[source_coordinates] = 0
    father_node[source_coordinates] = -1

    priority_queue.push(source_coordinates, 0 + euclidean_distance(source_coordinates, dest_coordinates))
    while priority_queue.size() != 0:
        [top_node, top_node_cost] = priority_queue.pop()

        if top_node == dest_coordinates:
            iterate_answer = dest_coordinates
            answer = [tuple_to_string(iterate_answer, node_cost[iterate_answer], False)]
            total_cost = node_cost[iterate_answer]
            while father_node[iterate_answer] != -1:
                if father_node[iterate_answer] == source_coordinates:
                    answer.append(tuple_to_string(father_node[iterate_answer], 0, True))
                else:
                    answer.append(
                        tuple_to_string(father_node[iterate_answer], node_cost[father_node[iterate_answer]], True))
                    total_cost += node_cost[father_node[iterate_answer]]
                iterate_answer = father_node[iterate_answer]

            answer.reverse()

            answer_list = [f'{total_cost}\n', f'{len(answer)}\n'] + answer
            write_output_file(answer_list, fail=False)
            exit()
        else:
            visited[top_node] = True
            for action in graph[top_node]:
                next_node = (top_node[0] + MAPPINGS[action][0], top_node[1] + MAPPINGS[action][1],
                             top_node[2] + MAPPINGS[action][2])
                if next_node in graph and not (visited[next_node] is True or priority_queue.exists(next_node)):
                    if action <= 6:
                        priority_queue.push(next_node, top_node_cost + 10 + euclidean_distance(next_node,
                                                                                               dest_coordinates))
                        node_cost[next_node] = 10
                    else:
                        priority_queue.push(next_node, top_node_cost + 14 + euclidean_distance(next_node,
                                                                                               dest_coordinates))
                        node_cost[next_node] = 14
                    father_node[next_node] = top_node
                elif next_node in graph and priority_queue.exists(next_node):
                    if action <= 6:
                        if priority_queue.get(next_node) > top_node_cost + 10 + euclidean_distance(next_node,
                                                                                                   dest_coordinates):
                            priority_queue.update(next_node, top_node_cost + 10 + euclidean_distance(next_node,
                                                                                                     dest_coordinates))
                            node_cost[next_node] = 10
                            father_node[next_node] = top_node
                    else:
                        if priority_queue.get(next_node) > top_node_cost + 14 + euclidean_distance(next_node,
                                                                                                   dest_coordinates):
                            priority_queue.update(next_node, top_node_cost + 14 + euclidean_distance(next_node,
                                                                                                     dest_coordinates))
                            node_cost[next_node] = 14
                            father_node[next_node] = top_node

    write_output_file(fail=True)
