import math
import os
import pathlib
import draw
from collections import namedtuple


data_folder_str = 'D:/GIT/Python/geowordle_real_datas/cluster_graphs_graphml/'
scale_epsilon = 0.02

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_number(s):
    try:
        start = s.index(">") + 1
        end = s.index("<", start)
        return abs(float(s[start:end]))
    except ValueError:
        return "error"

    # find the first  >
    # find the second <
    # return positive number in between

    return 0


def readFile(file_path):
    points_list = []
    count = 0
    with open(file_path, 'r') as f:
        Lines = f.readlines()
        # Strips the newline character
        for line in Lines:
            if "node id" in line:
                # if contains "node id"
                # get key_0
                c = get_number(Lines[count + 1])
                # get key_1
                x = get_number(Lines[count + 2])
                # get kety_2
                y = get_number(Lines[count + 3])
                points_list.append([x, y, c])
            count += 1
    return points_list


def output(out_f_name, points, num_colors,width_o, height_o,  min_x, min_y, max_x, max_y,col_list,x_offset, y_offset):
    with open(out_f_name, 'w') as f:
        ## c lines
        s = "c This is  a DIMACS file {} {} {} {} {}\n".format(out_f_name,  min_x, min_y, max_x, max_y)

        f.write(s)
        ## l lines
        s = 'l '
        for c in col_list:
            s+= c
            s+=","
        s = s[:-1]
        s += '\n'
        f.write(s)
        ## p lines
        s = "p {} {} {} {} 0\n".format(width_o, height_o, len(points), num_colors)
        f.write(s)

        ## p lines

        ## edge lines
        txt = "{x} {y} {c} 0\n"
        X = set()
        Y = set()
        for p in points:
            assert(p[0] >= min_x), p[0]
            assert(p[1] >= min_y), p[1]
            assert(p[2] >= 0)
            x = round(p[0]-min_x+x_offset , 6)
            y = round(p[1]-min_y + y_offset,6)
            assert (x not in X), x
            X.add(x)
            assert (y not in Y), y
            Y.add(y)

            s = txt.format(x= x, y= y, c=p[2])

            f.write(s)


def draw_plot(vis_f_name):
    if os.name == 'nt':
        dic_path = pathlib.Path(data_folder_str)
        plot_file = dic_path / (vis_f_name + "_plot.png")

        out_file = vis_f_name + "_out.txt"
        out_path = dic_path / out_file
        with open(out_path, 'r') as f:
            problem = draw.Problem(f)
            problem.draw(plot_file)
            f.close()



def clea_coordinates(raw_points, i):
    x_set = set()
    count = 0
    for p in raw_points:
        d = 2
        p_x = round(p[i], d)
        while p_x in x_set and d < 12:
            d = d + 2
            p_x = round(p[i], d)
        raw_points[count][i] = p_x
        assert(raw_points[count][i] not in x_set)
        x_set.add(raw_points[count][i])
        count += 1

    X = set()
    Y = set()
    for p in raw_points:

        assert (p[0] not in X), p.x
        X.add(p[0])
        assert (p[1] not in Y), p.y
        Y.add(p[1])



def clean_color(raw_points):
    c_set = set()
    for p in raw_points:
        c_set.add(p[2])

    c_list = list(c_set)
    count = 0
    for p in raw_points:
        raw_points[count][2] = c_list.index(p[2])
        count += 1
    return len(c_list)


def findscope(raw_points):
    s_set = set()
    for p in raw_points:
        s_set.add(p[0])
    min_x = min(s_set)
    max_x = max(s_set)

    s_set = set()
    for p in raw_points:
        s_set.add(p[1])
    min_y = min(s_set)
    max_y = max(s_set)
    return min_x, max_x, min_y, max_y

def saleCoordinates(raw_points):
    # 2% free space all rounds
    min_x, max_x, min_y, max_y = findscope(raw_points)
    width = 1000
    height = (max_y- min_y)/(max_x- min_x) *1000
    x_offset = scale_epsilon * width
    width_o = width + 2*x_offset
    y_offset = scale_epsilon * height
    height_o = height + 2* y_offset

    count = 0
    for p in raw_points:

        raw_points[count][0] = (p[0]-min_x)/(max_x- min_x) * 1000 + x_offset
        raw_points[count][1] = (p[1]-min_y)/(max_y- min_y) * height + y_offset
        assert(raw_points[count][0]  <  width_o),"{} < {}".format(raw_points[count][0],width_o)
        assert(raw_points[count][1]  <  height_o)
        count += 1
    return width_o, height_o


def generate(input_file):
    dic_path = pathlib.Path(data_folder_str)
    input_path = dic_path / input_file
    points = readFile(input_path)
    width_o, height_o = saleCoordinates(points)
    clea_coordinates(points, 0)
    clea_coordinates(points, 1)


    col_number = clean_color(points)

    out_file = input_file + "_out.txt"
    out_path = dic_path / out_file
    output(out_path, points, col_number, width_o, height_o)

    X = set()
    Y = set()
    for p in points:

        assert (p[0] not in X), p.x
        X.add(p[0])
        assert (p[1] not in Y), p.y
        Y.add(p[1])



def generate_real_coo(input_file):
    dic_path = pathlib.Path(data_folder_str)
    input_path = dic_path / input_file
    points = readFile(input_path)

    min_x, max_x, min_y, max_y = findscope(points)
    x_offset = scale_epsilon * (max_x-min_x)
    y_offset = scale_epsilon * (max_y-min_y)
    width_o = (max_x-min_x) + 2*x_offset
    height_o = (max_y-min_y) + 2*y_offset



    col_number = clean_color(points)

    out_file = input_file + "_real_out.txt"
    out_path = dic_path / out_file
    output(out_path, points, col_number, width_o, height_o)

    X = set()
    Y = set()
    for p in points:

        assert (p[0] not in X), p.x
        X.add(p[0])
        assert (p[1] not in Y), p.y
        Y.add(p[1])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    data_path = pathlib.Path('D:/GIT/Python/geowordle_real_datas/cluster_graphs_graphml/')
    file_list = []
    for x in data_path.iterdir():
        if x.is_file():
            s = x.name
            if s.endswith(".graphml"):
                generate(x.name)
                draw_plot(x.name)
                generate_real_coo(x.name)



