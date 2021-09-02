import csv
import os
import pathlib
import random

import draw
import generate_graphml
input_path = ""
cheese_set = set()
def clean_color(raw_points, dict):
    for p in raw_points:
        l = str.split(p[2],",")
        #p[2] = random.choice(l).strip()
        #p[2] = l[0].strip()



        count = 0
        max = 0
        max_index = 0
        for c in l:
            c= c.strip()
            if dict[c] > max:
                max_index = count
                max = dict[c]
            count += 1
        p[2] = l[max_index].strip()
        cheese_set.add(p[2])
    print(dict)
    print(cheese_set)
    c_list = list(cheese_set)
    print(c_list)
    count = 0
    for p in raw_points:
        raw_points[count][2] = c_list.index(p[2])
        count += 1
    return c_list

def readFile(input_file):
    input_file_path = input_path / input_file
    with open(input_file_path, mode='r') as csv_file:
        points = []
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            points.append([float(row["lng"]), float(row["lat"]), row["cheeses"]])
            line_count += 1
        print(f'Processed {line_count} lines.')
        print(points)
    return points

def generate(file):
    points = readFile(file)
    width_o, height_o = generate_graphml.saleCoordinates(points)
    generate_graphml.clea_coordinates(points, 0)
    generate_graphml.clea_coordinates(points, 1)
    frequencies(points)
    col_list = clean_color(points)
    print(col_list)

    out_file = file + "_out.txt"
    out_path = input_path / out_file
    generate_graphml. output(out_path, points, len(col_list), width_o, height_o)

    X = set()
    Y = set()
    for p in points:
        assert (p[0] not in X), p.x
        X.add(p[0])
        assert (p[1] not in Y), p.y
        Y.add(p[1])

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
        scale_x = width_o/(max_x- min_x)
        scale_y = height_o/(max_y - min_y)
        for p in points:
            assert(p[0] >= min_x), p[0]
            assert(p[1] >= min_y), p[1]
            assert(p[2] >= 0)
            x = round((p[0]-min_x+x_offset)* scale_x, 6)
            y = round((p[1]-min_y + y_offset) * scale_y,6)
            assert (x not in X), x
            X.add(x)
            assert (y not in Y), y
            Y.add(y)

            s = txt.format(x= x, y= y, c=p[2])

            f.write(s)



def generate_real_coo(file):
    points = readFile(file)
    print(points)
    min_x, max_x, min_y, max_y = generate_graphml.findscope(points)
    x_offset = generate_graphml.scale_epsilon * (max_x-min_x)
    y_offset = generate_graphml.scale_epsilon * (max_y-min_y)
    width_o = (max_x-min_x) + 2*x_offset
    height_o = (max_y-min_y) + 2*y_offset
    dict = frequencies(points)
    print(dict)
    col_list = clean_color(points, dict)
    print(col_list)
    out_file = file + "_real_out.txt"
    out_path = input_path / out_file
    x_offset = 0
    y_offset = 0
    min_x = -5.3
    min_y = 41
    max_x =10.2
    max_y = 51.6
    width_o = 780.68
    height_o = 747.443

    output(out_path, points, len(col_list), width_o, height_o, min_x, min_y, max_x, max_y, col_list, x_offset, y_offset)

    X = set()
    Y = set()
    print(points)
    for p in points:
        assert (p[0] not in X), p[0]
        X.add(p[0])
        assert (p[1] not in Y), p[1]
        Y.add(p[1])




def draw_plot(vis_f_name):
    if os.name == 'nt':
        plot_file = input_path / (vis_f_name + "_plot.png")
        out_file = vis_f_name + "_out.txt"
        out_path = input_path / out_file
        with open(out_path, 'r') as f:
            problem = draw.Problem(f)
            problem.draw(plot_file)
            f.close()


def frequencies(points):
    dict = {}
    for p in points:
        l = str.split(p[2], ",")
        for c in l:
            s = c.strip()
            if s in dict:
                dict[s] = dict[s] + 1
            else:
                dict[s] = 1
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
    return dict



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_path = pathlib.Path('D:/GIT/Python/geowordle_real_datas/cheese/')
    ##generate("results.csv")
    ##draw_plot("results.csv")
    generate_real_coo("results.csv")






