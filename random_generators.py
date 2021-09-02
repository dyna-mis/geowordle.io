import errno
import os
import random
import shutil
from math import ceil
from typing import TextIO
import itertools


def instance_generator(dic, point_number, color_number, width, height, number):
    dic_path = "{0}\\{1}\\{2}\\{3}\\".format( dic, str( width ),str( point_number ), str( color_number ) )
    if not os.path.exists( dic_path):
        try:
            os.makedirs( dic_path)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    for seed in range( 0, number ):
        random.seed( seed )
        file_name = "{0}{1}_{2}_{3}_{4}_{5}.txt".format( dic_path, str( width ), str( height ), str( point_number ),
                                                         str( color_number ), str( seed ) )
        print(file_name)
        with open( file_name, "w" ) as f:
            f.write( "c This is a UNIFORM distributed DIMACS file \n" )
            f.write( "c width height point_number color_number seed\n" )
            f.write( f"p {width} {height} {point_number} {color_number} {seed}\n" )
            i = 0
            x_coodinates_set = set()
            y_coodinates_set = set()
            while len( x_coodinates_set ) < point_number:
                rand_x: float = round( random.uniform( 1, width - 1 ), 2 )
                x_coodinates_set.add( rand_x )
            while len( y_coodinates_set ) < point_number:
                rand_y: float = round( random.uniform( 1, height - 1 ), 2 )
                y_coodinates_set.add( rand_y )

            co_pairs = zip( list( x_coodinates_set ), list( y_coodinates_set ) )
            for co in co_pairs:
                rand_color = random.randint( 0, color_number - 1 )
                f.write( f"{co[0]} {co[1]} {rand_color} 0\n" )
                i = i + 1
            f.close()

'''
if __name__ == '__main__':
    folder = 'D:\\GIT\\geowordle_core_cmake\\data'
    number = 10
    for e in range( 3, 11 ):
        n = 2 ** e
        instance_generator( folder, n, 2, 50, 100, number )
        instance_generator( folder, n, 2, 5000, 10000, number )
        for c_e in ( 0.05, 0.1, 0.2 ):
            c = ceil( n * c_e )
            if c > 2:
                instance_generator( folder, n, c, 50, 100,number )
                instance_generator( folder, n, c, 5000, 10000,number )
'''