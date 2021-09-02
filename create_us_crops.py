import math
import pathlib

import pandas
import pandas as pd
import excel_reader as er
import xlrd
xlrd.xlsx.ensure_elementtree_imported(False, None)
xlrd.xlsx.Element_has_iter = True



x_pixel = 1859 *72.0/96.0
y_pixel = 968*72.0/96.0
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

data_path_str = "D:/GIT/Python/geowordle_real_datas/us_crops/back_up_raw"
def get_coordinates(file_name, columns):
    raw_df = pd.read_excel( path(file_name),
        engine='openpyxl',
    )
    #raw_df = er.read_excel(path(file_name))
    datas = raw_df[columns]
    return datas


def get_crops(file_name):
    raw_df = pd.read_excel( path(file_name),
        engine='openpyxl',
    )
    raw_df = er.read_excel(path(file_name))
    print(raw_df.columns)
    raw_df.columns = ["FIPS", "CROP"]
    return raw_df

def check_valid(df_cd):
    # why not unique???

    s = set()
    for index, row in df_cd.iterrows():
        if(row['FIPS'] in s):
            print(row)
        else:
            s.add(row['FIPS'])
    assert(not df_cd.isnull().values.any())

def get_filter_coordinate(row):
    if not isinstance(row[1], float):
        x = float(row[1][:-1].replace('\U00002013', '-'))
        y = float(row[2][:-1].replace('\U00002013', '-'))
    else:
        x = row[1]
        y = row[2]
    if(x>xmin and y > ymin and x < xmax and y < ymax):
        x= round((x-xmin) * x_scale_ratio,6)
        assert(x > 0),x
        y= round((y-ymin) * y_scale_ratio,6)
        assert (y > 0)
        return x, y
    else:
        return -1, -1


def get_points(filename,df_cd):

    datas = df_cd[["Longitude","Latitude","CROP" ]]

    crops_set = set()
    # get colors
    for row in datas.itertuples():
        crops_set.add(row[3])
    crops_list = list(crops_set)
    points =[]
    for row in datas.itertuples():
        x, y = get_filter_coordinate(row)
        print(row, x,y)
        if(x > 0):
            col = crops_list.index(row[3])
            points.append([x,y,col])
    return points,crops_list

        #row("Longitude") , row("Latitude"), row("CROP")

def export(filename,df_cd):
    excel_file =filename + ".xlsx"
    plain_file = filename + ".txt"
    with pd.ExcelWriter( path('output.xlsx') ) as writer:
        df_cd.to_excel( writer, sheet_name='all_info' )
    points,crops_list = get_points(filename,df_cd)
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

def get_all_infos(c_list):
    data_df = er.getData(data_path_str,c_list)
    # create excel writer object
    writer = pd.ExcelWriter(path('output.xlsx'))
    # write dataframe to excel
    data_df.to_excel(writer)
    # save the excel
    writer.save()
    return data_df


def get_full(name, df):
    export(name,df)


def get_data_by_area(min_bound, df):
    df_new = df.loc[(df['Area'] >= min_bound)]
    return df_new


#[0, 2, 29, 30, 20,23,24,25,26]
def mergStates(df):
    crop_df_merged ={}
    for index, row in df.iterrows():
        state = row["State"]
        if state not in  crop_df_merged:
            crop_df_merged[state] = { "Corn":0, "Wheat":0, "Cotton":0, "Soybeans":0, "Vegetables":0 }
        crop_df_merged[state]["Corn"] += row["Corn"]
        crop_df_merged[state]["Wheat"] += row["Wheat"]
        crop_df_merged[state]["Cotton"] += row["Cotton"]
        crop_df_merged[state]["Soybeans"] += row["Soybeans"]
        crop_df_merged[state]["Vegetables"] += row["Vegetables"]


    return crop_df_merged

def dominantStates(df):
    summed = mergStates(df)
    for key, v in summed.items():
        max_v = 0
        max_string = "no predominance"
        for i, n in v.items():
            if n > max_v:
                max_v = n
                max_string = i
        summed[key] = max_string
    print(summed)
    summed_dict = pd.DataFrame(summed.items())
    print(summed_dict)
    return summed_dict


def conty_level_all():
    crop_df = get_all_infos([0, 2, 29, 30])
    crop_df.columns = ["State", "FIPS", "Area", "CROP"]
    cor_df = get_coordinates("coordinates.xlsx",["County", "FIPS", "Latitude", "Longitude"])
    #print(cor_df)

    df_cd = pd.merge( crop_df, cor_df, how='col', on = "FIPS" )

    get_full("crops_all", df_cd);
    df_new = get_data_by_area(100000, df_cd)
    get_full("crops_100000", df_new);
if __name__ == '__main__':
    #conty_level_all()

    crop_df = get_all_infos([0, 2, 29, 20,23,24,25,26])
    crop_df.columns = ["State", "FIPS", "Area",  "Corn", "Wheat", "Cotton", "Soybeans", "Vegetables"]
    states_info = dominantStates(crop_df)
    cor_df = get_coordinates("states_coordinates.xlsx",["state","latitude","longitude"])
    cor_df.columns = ["State", "Latitude", "Longitude"]
    print(states_info)
    states_info.columns = ['State', 'CROP']
    df_cd = pd.merge( states_info, cor_df, how='inner', on = "State" )
    print(df_cd)
    get_full("crops_states", df_cd);





