# draw a dimacs file
# using matplot

#include "main.h"
import argparse
import seaborn as sns
import pandas as pd
import miscellaneous as toolbox
import matplotlib.pyplot as plt
import re
import const


class InputParser(argparse.ArgumentParser):    
    def __init__(self):
        super().__init__()
        """parse the input string"""
        self.add_argument('input', metavar='input', type=argparse.FileType('r',encoding='UTF-8'), nargs= 1,
                        help='specified input file name ')
        self.add_argument('--output','-o', metavar='output_file', type=argparse.FileType('w'), nargs= 1,
                        help='specified output file name ', default= 'output_output')
        
        
        
               
class Problem():
    def __init__(self, input_file):
        '''build an instance from the DIMACS file'''
        lines = input_file.readlines()
        text = []
        for line in lines:
            #ignore all comment lines
            if line[0] == 'c':
                continue
            if line[0] == 'l':
                splitStr = re.split('\s|(?<!\d)[,.](?!\d)',line)
                for i in splitStr[1:]:
                    text.append(i)
            elif line[0] == 'p':
                splitStr = line.split()
                # adding seed information
                assert len(splitStr)== 6, 'p line Error:please check the format.txt for the correct format '
                self.width = int(splitStr[1])
                self.height = int(splitStr[2])
                self.point_number = int(splitStr[3])
                self.color_number = int(splitStr[4])
                self.Points =[]
            else:
                splitStr = line.split()
                self.Points.append(toolbox.Point(float(splitStr[0]),float(splitStr[1]),text[int(splitStr[2])]))
        # check its valid
        X = set()
        Y = set()
        for p in self. Points:
            assert(p.x not in X),p.x
            X.add(p.x)
            assert(p.y not in Y), p.y
            Y.add( p.y)
            assert(p.x < self.width)
            assert(p.y < self.height)
        assert len( X ) == len(self.Points), '{} {} points collides'.format(len( X ),  len(self.Points))
        assert len(X) == len(Y), 'points collides'
            # get information in p line
            # read edge lines one by one

        

    def info(self):
        '''printing relevent information for debug'''
        print(f'Width:{self.width}')
        print(f'Height:{self.height}')
        print(f'numbe of points:{self.point_number}')
        print(f'numbe of colors:{self.color_number}')   
        print(*self.Points,sep="")
    
    #TODO: draw the points set using matplot
    def draw(self,file_name):
        X = []
        Y = []
        C = []
        for point in self.Points:
            X.append(point.x)
            Y.append(point.y)
            C.append(point.color)

        df = pd.DataFrame(dict(x=X, y=Y, color=C))
        lm =sns.lmplot('x', 'y', data=df, hue='color', fit_reg=False,scatter_kws={'alpha': 0.5})
        lm.set(xlim=(0, self.width))
        lm.set(ylim=(0, self.height))
        #plt.show()
        plt.savefig(file_name)
    
if __name__ == "__main__":
    IP = InputParser()        
    args = IP.parse_args()
    input_file = args.input[0]
    problem = Problem(input_file)
    problem.info()
    problem.draw()
    
    