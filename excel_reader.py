import pathlib

import pandas as pd



def read_excel(input_path):
    df = pd.read_excel(input_path)

    return df

def read_all_sheets(input_path, c_list):
    xls = pd.ExcelFile( input_path )
    s_names = xls.sheet_names
    l = []
    for s in s_names:
        df = read_sheet_all(xls, s, c_list)
        checkNull(df)
        l.append(df)
    result = pd.concat(l)
    return result

def read_sheet(xls, sheet_str):
    df = pd.read_excel( xls, sheet_str, header=None)
    df.columns = range(0, 34)
    return df[[2, 30]]

#	Total Acres of Harvested Crops
def read_sheet_all(xls, sheet_str, c_list):
    df = pd.read_excel( xls, sheet_str, header=None)
    df.columns = range(0, 34)
    #return df[]
    return df[c_list]


def checkNull(df):
    col = df.columns
    for c in col:
        check_for_nan = df[c].isnull().values.any()
        if(check_for_nan):
            print(c)

def getData(data_path_str,c_list):
    data_path = pathlib.Path( data_path_str )
    list_all = []
    sum = 0
    for x in data_path.iterdir():
        if x.is_file():
            s = x.name
            if s.startswith("FIPS"):
                file_path = data_path / s
                result = read_all_sheets(file_path, c_list)
                sum += len(result)
                list_all.append( result )
    result = pd.concat( list_all)
    return result


if __name__ == '__main__':

    data_path_str = "D:/GIT/Python/geowordle_real_datas/us_crops/back_up_raw"
    data_path = pathlib.Path( data_path_str )
    data_df = getData(data_path_str)
    print(data_df)


