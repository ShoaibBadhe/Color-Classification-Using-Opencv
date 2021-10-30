# importing required modules
import cv2
import pandas as pd
import argparse
import math

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, default= "images/Sample1.png", help="Path to the image")
args = vars(ap.parse_args())

# Reading the image with opencv
img = cv2.imread(args['image'])

# resize img
img = cv2.resize(img, (550, 350))

# declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('Colors.csv', names=index, header=None)


# function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G -
                                                int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


def isLight(b,g,r):
    b= int(b)
    g= int(g)
    r= int(r)
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if (hsp>127.5):
        return True
    else:
        return False

cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('image', draw_function)
d,e,f = img[300,50]
name_disp_color = isLight(d,e,f)
orig_image = img.copy()

while True:
    cv2.imshow("image", img)
    if clicked:
        img = orig_image.copy()
        j,k,l = img[ypos,xpos]
        pointer_color = isLight(j,k,l)
        if pointer_color:
            cv2.circle(img, (xpos,ypos),3,(0,0,0),-1)
        else:
            cv2.circle(img, (xpos,ypos),3,(255,255,255),-1)
        text = getColorName(r, g, b)

       # For very light colours we will display text in black colour
        if name_disp_color:
            cv2.putText(img, text, (50, 320), 2, 0.9,
                        (0, 0, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(img, text, (50, 320), 2, 0.9,
                        (255, 255, 255), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
