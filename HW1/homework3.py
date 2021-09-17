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
    distance_to_source = {}
    father_node = {}

    for node in graph.keys():
        visited[node] = False
        distance_to_source[node] = inf
        father_node[node] = -1

    queue = Queue(maxsize=0)

    visited[source_coordinates] = True
    distance_to_source[source_coordinates] = 0
    father_node[source_coordinates] = -1

    queue.put(source_coordinates)
    while not queue.empty():
        front_node = queue.get()
        for action in graph[front_node]:
            next_node = (front_node[0] + MAPPINGS[action][0], front_node[1] + MAPPINGS[action][1],
                         front_node[2] + MAPPINGS[action][2])
            if next_node in graph and visited[next_node] is False:
                visited[next_node] = True
                distance_to_source[next_node] = distance_to_source[front_node] + 1
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

# elif algorithm == 'UCS':
# elif algorithm == 'A*':
# write_output_file()
