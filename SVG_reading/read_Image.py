# import matplotlib.pyplot as plt
from svgpathtools import svg2paths
import numpy as np
from Configer import configer

class drawSVG:
    def __init__(self, svgFile, is_quiet=False):
        self.svgFile = svgFile 
        self.paths, self.attributes = svg2paths(svgFile)
        # self.fig, self.ax = plt.subplots()
        self.penState = 0 #pen up/down
        data = configer.get("SVG_reader_setup")
        self.sample_amount = data["curve_sample_amount"]
        self.__is_quiet = is_quiet


    def plot(self):
        result = []
        shapeN = 1  # for debugging seperating number of shapes
        if not self.__is_quiet:
            print (self.penState)
        result.append(self.penState)


        for path in self.paths: # path is just a complete shape
            if not self.__is_quiet:
                print(f"Shape{shapeN}")
    
            shapeN += 1   
            penState = 0
            if not self.__is_quiet:
                print(penState)
            result.append(penState)


            for segment in path:  #segment of a shape 
        
        
                samplePoints = np.linspace(0, 1, num=self.sample_amount) #sample points (need more sample points for curves)

                points = [segment.point(t) for t in samplePoints]



                x_coords = [p.real for p in points]
                y_coords = [p.imag for p in points] # y is flipped because matplotlib handles y valuse differently 



                for i in range(len(x_coords)): #printing x,y vals
                    if not self.__is_quiet:
                        print(int(x_coords[i]), int(y_coords[i])) #using bottom right (4th quad)
                    result.append((int(x_coords[i]), int(y_coords[i])))
                    if i == 0:
                        result.append(1)


                # self.ax.plot(x_coords, y_coords, 'k')

        #if we are on last segment of shape
            self.penState = 0 #penup
            if not self.__is_quiet:
                print(self.penState)
            result.append(self.penState)

        if not self.__is_quiet:
            print(result)

        # self.ax.set_aspect('equal')

        # self.ax.invert_yaxis()
        #self.ax.axis("off")
        # plt.show()


        return result

if __name__ == "__main__":
    draw = drawSVG("shapes.svg", False)
    draw.plot()