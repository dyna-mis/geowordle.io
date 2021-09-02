import math
import pathlib

import pandas as pd
import excel_reader as er
import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True



x_pixel = 1859
y_pixel = 968
ymax = 49.8
ymin = 24.2
xmin = -125.5
xmax = -66.5
x_scale_ratio = x_pixel/(xmax-xmin)
y_scale_ratio = y_pixel/(ymax-ymin)



def path(file_name):
    data_path = pathlib.Path( data_path_str)
    file_path = data_path/file_name
    return file_path

data_path_str = "D:/GIT/Python/geowordle_real_datas/us_crops"
def get_cols(file_name):
    raw_df = pd.read_excel( path(file_name),
        engine='openpyxl',
    )
    #raw_df = er.read_excel(path(file_name))
    print(raw_df.columns)
    datas = raw_df[["Type"]]
    return datas


def check_valid(df_cd):
    pass


def get_filter_coordinate(row):
    row = row.split('\n')[0]
    row = str(row.encode('utf-8'))

    print(row)

    cor =row.rsplit('/', 1)[-1]
    cor = cor.split(' (')[0]
    print(cor)

    x = float(cor.split(';')[1][:-1].replace('\U00002013', '-'))
    y = float(cor.split(';')[0][2:].replace('\U00002013', '-'))
    if(x>xmin):
        print(x_scale_ratio)
        x= round((x-xmin) * x_scale_ratio,6)
        print(x)
        assert(x > 0),x
        y= round((y-ymin) * y_scale_ratio,6)
        assert (y > 0)
        return x, y
    else:
        return -1, -1


def get_points(filename,datas):

    print(datas)

    crops_set = set()
    # get colors
    for row in datas.itertuples():
        crops_set.add(row[2])
    crops_list = list(crops_set)
    points =[]
    for row in datas.itertuples():
        x, y = get_filter_coordinate(row)
        if(x > 0):
            col = crops_list.index(row[2])
            points.append([x,y,col])
    print(crops_list)
    return points,crops_list

        #row("Longitude") , row("Latitude"), row("CROP")

def export(filename,df_cd):

    plain_file = filename + ".txt"
    '''
    points,crops_list = get_points(filename,df_cd)
    print(crops_list)
    with open(path(plain_file), 'w') as f:
        ## c lines
        s = "c This is  a DIMACS file {}\n".format(filename)

        f.write(s)
        ## l lines
        s = 'l '
        for c in crops_list:
            s+= c
            s+=","
        s = s[:-1]
        s += '\n'
        f.write(s)
        ## p lines
        s = "p {} {} {} {} 0\n".format(x_pixel, y_pixel, len(points), len(crops_list))
        f.write(s)

        ## p lines

        ## edge lines
        txt = "{x} {y} {c} 0\n"
        X = set()
        Y = set()
        for p in points:
            assert(p[0] > 0), p[0]
            assert(p[1] > 0), p[1]
            assert(p[2] >= 0)
            x = p[0]
            y = p[1]
            assert (x not in X), x
            X.add(x)
            assert (y not in Y), y
            Y.add(y)

            s = txt.format(x= x, y= y, c=p[2])

            f.write(s)
'''

def get_coordinates(file_name):
    with open(path(file_name), mode='r', encoding='utf-8-sig') as fp:
        Lines = fp.readlines()
        for line in Lines:
            print(line)
            get_filter_coordinate(line)

if __name__ == '__main__':
    cor_df = get_cols("power.xlsx")
    cor_df = get_coordinates("power.txt")
    print(data_path_str)


    check_valid( cor_df )

    export("output",cor_df)



    # output offsets, having min_x in command (later for visualization)

