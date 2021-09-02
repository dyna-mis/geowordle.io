import numpy as np
from enum import Enum
import random
from typing import List


# TODO: understande how the covariance defined, By now,
class Model( Enum ):
    UNIFORM = 1
    GAUSSIAN = 2
    Twitter = 3

    def __str__(self):
        return self.name


class Point:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.color = c

    def __repr__(self):
        return f"{self.x}, {self.y}, {self.color}\n"

    def __str__(self):
        return f"{self.x}, {self.y}, {self.color}\n"

    def __hash__(self):
        return hash(self.x)

    def __eq__(self, other):
        return self.generall( other )

    def generall(self, q):
        """ check if two points have the same coordinates"""
        return self.x == q.x or self.y == q.y

    def collision(self, q):
        """ check if two points have the same coordinates"""
        return self.x == q.x and self.y == q.y

    def x_parallel(self, q):
        ''' check if two points have the same x_coordinates'''
        return self.x == q.x

    def y_parallel(self, q):
        ''' check if two points have the same y_coordinates'''
        return self.y == q.y

    def colinear(self, q, r):
        '''check if three points are collinear '''
        # TODO: Implement the colinear checking function
        pass


def random_2D_covariance_matrix(width, height):
    x_11 = random.uniform( 0, width / 10 )
    x_12 = random.uniform( 0, width / 10 )
    y_21 = random.uniform( 0, height / 10 )
    y_22 = random.uniform( 0, height / 10 )
    A = [[x_11, x_12],
         [y_21, y_22]]
    # B is a pseudo-random covariance matrix
    B = np.dot( A, np.transpose( A ) )
    return B


# the size is wanted size after adding new points
def gaussian_singlepeak(width, height, size, points):
    mean_x = random.uniform( 0, width )
    mean_y = random.uniform( 0, height )
    cov = random_2D_covariance_matrix( width, height )
    while len( points ) < size:
        parray = np.random.multivariate_normal( (mean_x, mean_y), cov, 1 )[0]
        # print(parray)
        point = Point( parray[0], parray[1], 0 )
        # check if the point with positive coordinates
        if point.x < 0 or point.y < 0:
            continue
        points.add( point )

    # partional partition


def classification(portion_sizes, size, color_list):
    color_index = 0
    colored_size = 0;
    accum_size = 0;
    for portion_size in portion_sizes:
        accum_size += portion_size
        while colored_size < accum_size:
            index = np.random.randint( size )
            # print(f'index: {index}')
            while color_list[index] != -1:
                # print(f'index: {index}')
                index = (index + 1) % size
            color_list[index] = color_index
            colored_size += 1
        color_index = color_index + 1
    assert colored_size == accum_size
    return list


if __name__ == "__main__":
    points = set()
    gaussian_singlepeak( 10, 10, 50, points )
