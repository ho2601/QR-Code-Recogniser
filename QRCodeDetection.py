
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import math
import imageIO
import imageIO.png

class Queue:
   def __init__(self):
       self.items=[]
  
   def isEmpty(self):
       return self.items==[]
      
   def enqueue(self, item):
       self.items.insert(0,item)
      
   def dequeue(self):
       return self.items.pop()
      
   def size(self):
       return len(self.items)

def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array

def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)

def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    lst = []
    for i in range(len(pixel_array_r)):
        newLst = []
        for k in range(len(pixel_array_r[i])):
            newLst += [(round(0.299 * pixel_array_r[i][k] + 0.587 * pixel_array_g[i][k] + 0.114 * pixel_array_b[i][k]))]
        lst.append(newLst)
    return lst

def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    qMin = 255
    qMax = 0
    output = []
    
    #Minimum loop
    for i in range(len(pixel_array)):
        minimum = abs(min(pixel_array[i]))
        if (qMin > minimum):
            qMin = minimum
    
    #Maximum loop
    for i in range(len(pixel_array)):
        maximum = abs(max(pixel_array[i]))
        if (qMax < maximum):
            qMax = maximum
            
    for i in range(0, image_height):
        lst = []
        for j in range(0, image_width):
            if round(qMax - qMin) == 0:
                lst += [0]
            else:
                lst.append(round((pixel_array[i][j] - qMin) * (255) / (qMax - qMin)) + 0)
        output.append(lst)
    return output
                
def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    x = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            x[i][j] = (pixel_array[i -1][j + 1]  + (pixel_array[i + 1][j - 1] *-1) + pixel_array[i - 1][j - 1] + (pixel_array[i - 1][j] * 2) + (pixel_array[i + 1][j] * -2) + (pixel_array[i + 1][j + 1] *-1)) / 8
    return x

def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    x = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            x[i][j] = ((pixel_array[i + 1][j - 1] * -1) + pixel_array[i - 1][j + 1] + (pixel_array[i - 1][j - 1] * -1) + (pixel_array[i][j - 1] * -2) +  + (pixel_array[i][j + 1] * 2) + pixel_array[i + 1][j + 1]) /8
    return x     
    
def edgeMagnitude(pixel_array, image_width, image_height, verticle, horizontal):
    x = createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for y in range(image_width):
            x[i][y] = abs(math.sqrt((verticle[i][y] ** 2) + (horizontal[i][y] ** 2)))
    return x

def computeBoxAveraging3x3(pixel_array, image_width, image_height):
    x= createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(1, image_height - 1):
        for j in range(1, image_width - 1):
            if (i == image_height - 1) or (j == image_width - 1):
                pass
            else:
                x[i][j] = (pixel_array[i - 1][j - 1]) + (pixel_array[i - 1][j]) + (pixel_array[i - 1][j + 1]) + (pixel_array[i][j - 1]) + (pixel_array[i][j]) + (pixel_array[i][j + 1]) + (pixel_array[i + 1][j - 1]) + (pixel_array[i + 1][j]) + (pixel_array[i + 1][j + 1]) / 9
    return scaleTo0And255AndQuantize(x, image_width, image_height) 

def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    for i in range(image_height):
        for j in range(image_width):
            if pixel_array[i][j] < threshold_value:
                pixel_array[i][j] = 0
            else:
                pixel_array[i][j] = 255
    return pixel_array

def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    lst = []
    for i in range(0, image_height):
        lst.append([]);
        for j in range(image_width):
            if (j == 0) or (j == image_width - 1) or (i == 0) or (i == image_height - 1):
                lst[i].append(0);
            elif ((pixel_array[i + 1][j - 1] > 0) and (pixel_array[i + 1][j] > 0) and (pixel_array[i + 1][j + 1] > 0)and pixel_array[i - 1][j - 1] > 0) and (pixel_array[i - 1][j] > 0) and (pixel_array[i - 1][j + 1] > 0) and (pixel_array[i][j - 1] > 0) + (pixel_array[i][j] > 0) and (pixel_array[i][j + 1] > 0):
                lst[i].append(1);
            else:
                lst[i].append(0);
    return lst;

def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    lst = [];
    for i in range(0, image_height):
        lst.append([]);
        for j in range(image_width):
            if (j == image_width - 1) or (i == image_height - 1):
                #Top Row
                try:
                    topLeft = pixel_array[i-1][j-1]
                except:
                    topLeft = 0
                    
                try:
                    topMid = pixel_array[i-1][j]
                except:
                    topMid = 0
                    
                try:
                    topRight = pixel_array[i-1][j+1]
                except:
                    topRight = 0
                    
                #Middle Row
                try:
                    midLeft = pixel_array[i][j-1]
                except:
                    midLeft = 0
                    
                try:
                    midMid = pixel_array[i][j]
                except:
                    midMid = 0
                    
                try:
                    midRight = pixel_array[i][j+1]
                except:
                    midRight = 0
                    
                #Bottom Row
                try:
                    bottomLeft = pixel_array[i+1][j-1]
                except:
                    bottomLeft = 0
                    
                try:
                    bottomMid = pixel_array[i+1][j]
                except:
                    bottomMid = 0
                    
                try:
                    bottomRight = pixel_array[i+1][j+1]
                except:
                    bottomRight = 0
                    
                #Top Check

                if (topLeft != 0) or (topMid != 0) or (topRight != 0):
                    lst[i].append(1);
                    
                #Middle Check
                elif (midLeft != 0) or (midMid != 0) or (midRight != 0):
                    lst[i].append(1);
                    
                #Bottom Check
                elif (bottomLeft != 0) or (bottomMid != 0) or (bottomRight != 0):
                    lst[i].append(1);
                    
                else:
                    lst[i].append(0);
                
            elif ((pixel_array[i + 1][j - 1] != 0) or (pixel_array[i + 1][j] != 0) or (pixel_array[i + 1][j + 1] != 0) or pixel_array[i - 1][j - 1] != 0) or (pixel_array[i - 1][j] != 0) or (pixel_array[i - 1][j + 1] != 0) or (pixel_array[i][j - 1] != 0) + (pixel_array[i][j] != 0) or (pixel_array[i][j + 1] != 0):
                lst[i].append(1);
                
            else:
                lst[i].append(0);
                
    return lst;

def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    x = createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0)
    visited = createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0)
    q = Queue()
    dict = {}
    k = 1
    for i in range(image_height):
        for j in range(image_width):
            c = 0
            if pixel_array[i][j] == 1 and visited[i][j] != 1:
                q.enqueue((i, j))
            while q.isEmpty() == False:
                c += 1
                current = q.dequeue()
                x_value = current[0]
                y_value = current[1]
                x[x_value][y_value] = k
                visited[x_value][y_value] = 1

                #above pixel
                if x_value-1 > 0 and pixel_array[x_value - 1][y_value] == 1 and visited[x_value - 1][y_value] == 0:
                    q.enqueue((x_value - 1,y_value))
                    visited[x_value - 1][y_value] = 1

                #below pixel
                if x_value + 1 < image_height and pixel_array[x_value + 1][y_value] == 1 and visited[x_value + 1][y_value] == 0:
                    q.enqueue((x_value + 1,y_value))
                    visited[x_value + 1][y_value] = 1

                #left pixel
                if y_value - 1 > 0 and pixel_array[x_value][y_value - 1] == 1 and visited[x_value][y_value - 1] == 0:
                    q.enqueue((x_value, y_value - 1))
                    visited[x_value][y_value - 1] = 1

                #right pixel
                if y_value + 1 < image_width and pixel_array[x_value][y_value + 1] == 1 and visited[x_value][y_value + 1] == 0:
                    q.enqueue((x_value, y_value + 1))
                    visited[x_value][y_value + 1] = 1
            dict[k] = c
            k += 1
            visited[i][j] = 1
    return x, dict

def final_component(p1,  image_width, image_height, key):
    x = createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0)
    for i in range(image_height):
        for j in range(image_width):
            if p1[i][j] == key:
                x[i][j] = 1
    return x

def calculateboxbound(fcomp, image_width, image_height):
    minx, miny, maxx, maxy = image_height, image_width, 0, 0
    for i in range(image_height):
        for j in range(image_width):
            if fcomp[i][j] == 1:
                if minx > j:
                    minx = j
                if miny > i:
                    miny = i
                if maxx < j:
                    maxx = j
                if maxy < i:
                    maxy = i
    return minx, maxx, miny, maxy
    
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for i in range(h):
        row = []
        for j in range(w):
            triple = []
            triple.append(r[i][j])
            triple.append(g[i][j])
            triple.append(b[i][j])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage


# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage
    

# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()

def main():
    filename = "./images/covid19QRCode/poster1small.png"
    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)
    greyScale = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b,image_width, image_height)
    horizontalEdge = computeHorizontalEdgesSobelAbsolute(greyScale, image_width, image_height)
    verticalEdge = computeVerticalEdgesSobelAbsolute(greyScale, image_width, image_height)
    mag = edgeMagnitude(greyScale, image_width, image_height, verticalEdge, horizontalEdge)
    smoothEdge = computeBoxAveraging3x3(mag, image_width, image_height)
    for i in range(7):
        smoothEdge = computeBoxAveraging3x3(smoothEdge, image_width, image_height)
    threshholding = computeThresholdGE(smoothEdge, 70, image_width, image_height)
    cd = computeDilation8Nbh3x3FlatSE(threshholding, image_width, image_height)
    ce = computeErosion8Nbh3x3FlatSE(cd, image_width, image_height)


    p_array, a_dict =  computeConnectedComponentLabeling(ce, image_width, image_height)
    max_pixels = max(a_dict.values())
    keys = [i for i, j in a_dict.items() if j == max_pixels]
    f_key = keys[0]
    finalComp = final_component(p_array,  image_width, image_height, f_key)

    xmin, xmax, ymin, ymax = calculateboxbound(finalComp, image_width, image_height)
    start_p = (xmin, ymin)
    width = ymax - ymin
    height = xmax - xmin
    pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r,px_array_g,px_array_b,image_width,image_height))

    # pyplot.imshow(threshholding, cmap="gray")
    
    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle( start_p, width, height, linewidth=3, edgecolor='g', facecolor='none' )
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()

if __name__ == "__main__":
    main()