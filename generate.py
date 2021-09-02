import argparse
import math
import pathlib
import string

from numpy import floor

import generators
import miscellaneous as toolbox
import errno
import os
import random
import shutil
from math import ceil
import draw
from typing import TextIO
import itertools
import numpy as np
import const

# to use it to generate uniform points, just do generator.py <width> <height> <model> <seed> <color_number> <point_size> [output] [decimal numbers]
# to use it to generate gaussian points, just do generator.py <width> <height> <model>
# <seed> <color_number> <point_size> [output][peak_number][point_size_peak] [decimal numbers]
# TODO: one peak, one color
# Example run configuration for uniform generator: 500 800 UNIFORM 0 3 5 5 2 -o output -d 2

# Example run configuration for gaussian generator: 500 800  GAUSSIAN 0 2 5   -o output -p 2 -ps 9 1 -d 2
# width : width of plane
# height: height of plane
# point_number: number of points in total (Gaussian, pre-)/each color class(UNIFORM)
# color_size: number of colors
# model: uniform, gaussian, twitter_data_generator
# output: name of output file
# seed: Seed used in random number generator (for reproducibility)
# peak_number: number of normal distributions in the layout
# point_size_peak: list of sizes in differnt gaussian distributions



small_size = [20, 30, 40, 50, 60, 70, 80, 90, 100]
large_size =[200, 300, 400, 500, 600, 700, 800, 900, 1000]

color_numbers = [2, 3, 4, 8, 16]
instance_number = 10
label_len_min = 3
label_len_max = 10
diviation_control = 0.7


class InputParser( argparse.ArgumentParser ):

    def __init__(self):
        super().__init__()
        """parse the input string"""
        self.add_argument( 'width', metavar='width', type=int, nargs=1,
                           help='width of plane' )
        self.add_argument( 'height', metavar='height', type=int, nargs=1,
                           help='height of plane' )
        # self.add_argument('--sum','-s', dest='accumulate', action='store_const',
        #                const=sum, default=max,
        #                help='sum the integers (default: find the max)')  
        self.add_argument( 'model', metavar='model', type=lambda model: toolbox.Model[model],
                           choices=list( toolbox.Model ), nargs=1,
                           help='generator model: uniform, gaussian, twitter_data_generator' )
        self.add_argument( 'seed', metavar='seed', type=int, nargs=1,
                           help='seed used in random number generator' )
        self.add_argument( 'color_number', metavar='color_number', type=int, nargs=1,
                           help='color_number of plane' )

        self.add_argument( 'point_size', metavar='point_size', type=int, nargs='+',
                           help='point_size of plane in each color class/total' )
        self.add_argument( '--output', '-o', metavar='output_file', type=argparse.FileType( 'w' ), nargs=1,
                           help='specified output file name ', default='output' )
        # for gaussian distribution, we need peak location, variants and number in each peak
        self.add_argument( '--peak_number', '-p', metavar='peak_number', type=int, choices=range( 1, 100 ), nargs=1,
                           default=3,
                           help='specified output file name ' )
        self.add_argument( '--point_size_peak', '-ps', metavar='point_size_peak', type=int, nargs='+',
                           help='point_size of plane in each peak class' )
        self.add_argument( '--digits', '-d', metavar='digits', type=int, nargs='+',
                           help='digits after the decimal point' )


def generate_command_line():
    IP = InputParser()
    args = IP.parse_args()
    print( args )
    # case1: uniform generator
    if args.model[0] == toolbox.Model.UNIFORM:
        Generator = generators.UniformGenerator( args )
    if args.model[0] == toolbox.Model.GAUSSIAN:
        Generator = generators.GaussianGenerator( args )
    Generator.output()

def get_texts_random(color_number):
    list = []
    letters = [i for i in string.ascii_lowercase]
    for q in range(color_number):
        n = random.randrange(label_len_min, label_len_max)
        random_list = random.sample(letters, n)
        str1 = ""

        list.append(str1.join(random_list))
    return list

def generate_uniform_branch(dic, point_number, color_number, width, height, file_number, digits):
    dic_path = dic /str( color_number )
    dic_path.mkdir( parents=True, exist_ok=True )
    for seed in range( 0, file_number ):
        random.seed( seed )
        file_name = "uniform_{0}_{1}_{2}.txt".format(str( point_number ),
                                                                 str( color_number ), str( seed ) )
        texts = get_texts_random(color_number)
        text_str = ','.join( [str( elem ) for elem in texts] )
        file_path = dic_path / file_name;
        with file_path.open("w") as f:
            f.write( "c This is a UNIFORM distributed DIMACS file \n" )
            f.write( "c width height point_number color_number seed\n" )
            f.write(f"l {text_str}\n")
            f.write( f"p {width} {height} {point_number} {color_number} {seed}\n" )

            points_x = set()
            while len( points_x ) < point_number:
                x_rand = round( random.uniform( 1, width - 1 ), digits )
                points_x.add( x_rand )
            points_y = set()
            while len( points_y ) < point_number:
                y_rand = round( random.uniform( 1, height - 1 ), digits )
                points_y.add( y_rand )
            list_x = list( points_x )
            list_y = list( points_y )
            random.shuffle( list_x )
            random.shuffle( list_y )
            for i in range( point_number ):
                color = random.randint( 0, color_number - 1 )
                f.write( f"{list_x[i]} {list_y[i]} {color} 0\n" )
            f.close()
        '''
        if os.name == 'nt':
            plot_file = dic_path / (file_name+"_plot.png")
            with open( file_path, 'r' ) as f:
                problem = draw.Problem( f )
                problem.draw( plot_file )
                f.close()
        '''

## 2 peaks, each peak 20% 80%, ratios [20%, 80%]
def generate_1D_gaussian(point_numbers, peaks, width, sigma_x, digits):
    sum = 0
    count = 0
    coordinates_set = set()
    coordinates_list = []
    coordinates_set_per_peak = set()
    for i in range( peaks ):

        coordinates_set_per_peak = set()
        count = point_numbers[i]
        # generate peak
        mean_x = random.uniform( width * 0.1, width * 0.9 )
        sigma = sigma_x[i] * width* diviation_control

        while len( coordinates_set_per_peak ) < count:
            s = round( np.random.normal( mean_x, sigma, 1 )[0], digits)
            if 0 < s < width:
                if s not in coordinates_set:
                    coordinates_set.add( s )
                    coordinates_set_per_peak.add( s )

        assert len( coordinates_set_per_peak ) == count
        list_x = list( coordinates_set_per_peak )
        random.shuffle( list_x )
        assert len( list_x ) == count
        assert sum == len( coordinates_list )
        coordinates_list += list_x
        sum += count
        assert sum == len( coordinates_list ), f"{sum}, {len( coordinates_list )}, {len( list_x )}, {count}"
    return coordinates_list, sum


def str_gen(list_str):
    name = ""
    for e in list_str:
        name += str( e )
        name += "_"
    name += "0"
    return name


## hard coding peak ratios
def generate_gaussian_branch(dic, point_number, color_number, width, height, file_number, digits):
    dic_path = dic / str( color_number )
    dic_path.mkdir( parents=True, exist_ok=True )
    for seed in range( 0, file_number ):
        np.random.seed( seed )
        file_name = "gaussian_{0}_{1}_{2}.txt".format( str( point_number ),str( color_number ), str(seed))
        file_path = dic_path / file_name
        ## generate points
        ## generate points per peak
        config = generate_gaussian_configuration(point_number,color_number)
        ratios = config["ratio"]
        sigma_x = config["sigma_x"]
        sigma_y = config["sigma_y"]
        list_x, sum_x = generate_1D_gaussian( ratios, color_number, width, sigma_x,digits )
        list_y, sum_y = generate_1D_gaussian( ratios, color_number, width, sigma_y,digits )
        assert sum_x == sum_y, "sum_x and sum_y different"
        assert sum_x == len( list_x )
        texts = get_texts_random(color_number)
        text_str = ','.join( [str( elem ) for elem in texts] )
        with file_path.open( "w", encoding ="utf-8" ) as f:
            f.write( "c This is a Gaussian distributed DIMACS file \n" )
            f.write( "c width height point_number color_number seed\n" )
            f.write( f"c ratios: {str( ratios )}\n" )
            f.write( f"c x: {str_gen( sigma_x )}, y: {str_gen( sigma_y )}\n" )
            f.write(f"l {text_str}\n")
            f.write( f"p {width} {height} {sum_x} {color_number} {seed}\n" )
            start = 0
            count = 0
            for i in range(color_number):
                count += ratios[i]
                color = i
                for j in range( start, count ):
                    assert j < sum_x
                    f.write( f"{list_x[j]} {list_y[j]} {color} 0\n" )
                start = count
            f.close()
        '''
        if os.name == 'nt':
            plot_file = dic_path / (file_name+"_plot.png")
            with open( file_path, 'r' ) as f:
                problem = draw.Problem( f )
                problem.draw( plot_file )
                f.close()
        '''



#ratios = [[0.4, 0.6], [0.3, 0.3, 0.4], [0.3, 0.3, 0.2, 0.2], [0.3, 0.2, 0.1, 0.2, 0.2]]
#sigma_x = [[0.2, 0.3], [0.1, 0.1, 0.3], [0.2, 0.2, 0.1, 0.1], [0.3, 0.2, 0.1, 0.1, 0.1]]
#sigma_y = [[0.1, 0.1], [0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1, 0.1]]
#sigma_x_large = [[0.2, 0.3], [0.2, 0.2, 0.5], [0.3, 0.3, 0.4, 0.4], [0.5, 0.3, 0.7, 0.4, 0.2]]
#sigma_y_large = [[0.1, 0.7], [0.5, 0.2, 0.3], [0.6, 0.4, 0.2, 0.2], [0.3, 0.2, 0.2, 0.2, 0.1]]
def make_instances(folder_name, instance_size):
    if os.name == 'nt':
        data_path = pathlib.Path( 'D:/GIT/C++/geowordle_core_cmake/data' )
    else:
        data_path = pathlib.Path( "/home/guangping/dev/data" )

    uniform_folder = data_path /folder_name/'Uniform'
    gaussian_folder = data_path /folder_name/'Gaussian'

    for c in color_numbers:
        generate_uniform_branch( uniform_folder, instance_size, c, 1000, 1000, instance_number, 4)
        generate_gaussian_branch( gaussian_folder, instance_size, c, 1000, 1000, instance_number, 4)


def random_sum_list(point_number, size):
    numbers = list(np.random.dirichlet(np.ones(size), size=point_number-size)[0])
    sum = 0
    tem_list = [1]* (size-1)
    index = 0
    for l in numbers[:-1]:
        n = int(floor((point_number-size) *l))
        tem_list[index] += n
        sum += tem_list[index]
        index += 1
    tem_list.append(point_number-sum)
    assert(len(tem_list) == size)
    check_sum = 0
    for l in tem_list:
        check_sum += l
        assert( l > 0)

    assert(check_sum == point_number),check_sum

    return tem_list


def generate_gaussian_configuration( point_number,color_number):
    configuration = {}
    configuration["ratio"] = random_sum_list(point_number,color_number)
    configuration["sigma_x"] = []
    configuration["sigma_y"] = []
    for i in range(color_number):
        n = random.randrange(3, 9)
        configuration["sigma_x"].append(0.1*n)
        configuration["sigma_y"].append(0.1*n)
    print(configuration)
    return configuration


def make_instances_set(folder_name, instance_sizes):
    if os.name == 'nt':
        data_path = pathlib.Path( 'D:/GIT/C++/geowordle_core_cmake/data' )
    else:
        data_path = pathlib.Path( "/home/guangping/dev/data" )

    uniform_folder = data_path /folder_name/'Uniform'
    gaussian_folder = data_path /folder_name/'Gaussian'

    for instance_size in instance_sizes:
        for c in color_numbers:
            generate_uniform_branch( uniform_folder, instance_size, c, 1000, 1000, instance_number, 4)
            generate_gaussian_branch( gaussian_folder, instance_size, c, 1000, 1000, instance_number, 4)
if __name__ == "__main__":

# make small instances 50
    #make_instances_set("small", small_size)

# make middle-size instances  500
# make large instances   1000
    #make_instances_set("large", large_size)
    #make_instances_set("small", range(20,1000,10))
    make_instances_set("exp2", [50, 100])


    '''
    data_path = pathlib.Path('D:/GIT/C++/geowordle_core_cmake/data/small/Gaussian/2/gaussian_20_2_5.txt')

    plot_file = pathlib.Path('D:/GIT/C++/geowordle_core_cmake/data/small/Gaussian/2/gaussian_20_2_5.txt_plot.png')
    with open(data_path, 'r') as f:
        problem = draw.Problem(f)
        problem.draw(plot_file)
        f.close()
    '''

