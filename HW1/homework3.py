MAPPINGS = {1: [1, 0, 0], 2: [-1, 0, 0], 3: [0, 1, 0], 4: [0, -1, 0], 5: [0, 0, 1], 6: [0, 0, -1], 7: [1, 1, 0],
            8: [1, -1, 0], 9: [-1, 1, 0], 10: [-1, -1, 0], 11: [1, 0, 1], 12: [1, 0, -1], 13: [-1, 0, 1],
            14: [-1, 0, -1],
            15: [0, 1, 1], 16: [0, 1, -1], 17: [0, -1, 1], 18: [0, -1, -1]}


def read_input_file():
    """
    Reads input file called "input.txt" in the same directory as the python file line by line

    :return:
    A list in which every member is a line of input file
    """
    input_file = open('input.txt', 'r')
    input_file_lines = input_file.readlines()

    for line in input_file_lines:
        line = line.strip()
        print(line)

    input_file.close()


def write_output_file(output_file_lines=None):
    """
    Writes output file and solution of the problem to "output.txt" file in the same dictionary as the python file
    """

    if output_file_lines is None:
        output_file_lines = ['1\n', '2\n', '3']
    output_file = open('output.txt', 'w')
    output_file.writelines(output_file_lines)

    output_file.close()


read_input_file()
write_output_file()
