# This is a colored points genertor, which generate random instances of colored points in the plane.

import random
import miscellaneous as toolbox
import draw 
class Generator:
    def __init__(self,args):
        self.seed = args.seed[0]
        random.seed(self.seed)
        self.width = args.width[0]
        self.height = args.height[0]
        self.model = args.model[0]
        self.color_number = args.color_number[0]
        self.point_size = args.point_size
        self.output_file = args.output[0]
        self.Points = set()
        alert = f'There are {self.color_number} color classes and  size of {len(self.point_size)} classes  are given!'
        assert len(self.point_size) == self.color_number, alert
        self.digits = args.digits[0]
    def info(self):
        print(f'Width:{self.width}')
        print(f'Height:{self.height}')
        print(f'Model:{self.model}')
        print(f'numbe of points:{self.point_number}')
        print(f'numbe of colors:{self.color_number}')
        print(*self.Points,sep="")
    def output(self):
        #TODO: generate the output file name if none is given
        '''write the point set in a file, if the output streaming is not defined, we create the file name wrapping the generator informations'''
        #with open(self.output_file,'w') as fp:
        with self.output_file as fp:
            fp.write(f'c This is a instance generated by the geoWordle {self.model} Generator\n')
            fp.write(f'c with seed {self.seed}\n')
            fp.write(f'p {self.width} {self.height} {self.point_number} {self.color_number}\n')
            for p in self.Points:
                fp.write(f"{p.x} {p.y} {p.color} 0\n")
        #print(*self.Points,sep="")       
        # draw the plot and save the plot
        plot_file = self.output_file.name + "_plot"
        with open(self.output_file.name,'r') as input_file:
            problem = draw.Problem(input_file)
            problem.info()
            problem.draw(plot_file)

    
         

class UniformGenerator(Generator):
    def __init__(self,args):
        super().__init__(args)
        
        accum_size = 0
        for color in range(self.color_number):
            accum_size = accum_size + self.point_size[color]
            while  len(self.Points) < accum_size:
                x_rand = round(random.uniform(1,self.width-1),self.digits)
                y_rand = round(random.uniform(1,self.height-1),self.digits)
                self.Points.add(toolbox.Point(x_rand,y_rand,color))        
        self.point_number = accum_size
        assert(self.point_number == len(self.Points))
#FIXME: Gaussian Model
class GaussianGenerator(Generator):
    def __init__(self,args):
        super().__init__(args)
        self.peak_num = args.peak_number[0]
        self.point_size_peak = args.point_size_peak
        alert = f'There are {self.peak_num} mean classes and  size of {len(self.point_size_peak)} classes  are given!'
        assert len(self.point_size_peak) == self.peak_num, alert
        
        
        # points sum of color classes should be equal to the sum of peak classes
        color_sum = sum(self.point_size)
        peak_sum = sum(self.point_size_peak)
        alert = f' The sum of all color classes {color_sum} is not euqal to the sum of all peak classes {peak_sum} '
        assert color_sum == peak_sum, alert
        accum_size = 0
        # for each peak
        for i in range(0,self.peak_num):
                accum_size = accum_size + self.point_size_peak[i]
                toolbox.gaussian_singlepeak(self.width, self.height, accum_size,self.Points)              
        self.point_number = accum_size
        assert(self.point_number == len(self.Points))
        # TODO: color the points
        color_list =[-1 for i in range(self.point_number)]
        toolbox.classification(self.point_size,self.point_number,color_list)
        assert(len(color_list) == len(self.Points))

        index = 0
        for point in self.Points:
            point.color = color_list[index]
            index += 1         

if __name__ == "__main__":
# test point hashing function
    p = toolbox.Point(10,100,2)
    q = toolbox.Point(10,100,2)
    s = set()
    s.add(p)
    s.add(q)
    assert len(s) ==1, "Error: point hashing fucntion"
    # execute only if run as a script
    
    # input parse
    
    
    # generator init
    
    
    # build data
    
    # write out

    pass

