import pygame
import os
import math
import time
from matrix import *

os.environ["SDL_VIDEO_CENTERED"]='1'
width, height = 1920, 1080
black, white, blue = (20, 20, 20), (230, 230, 230), (0, 154, 255)

#pygame
pygame.init()
pygame.display.set_caption("3D Cube")
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 300


angle = 0
cube_position = [width//2, height//2]
scale = 600
speed = 0.005

#iterating through all the points change to something else if needed
points = [n for n in range(8)]

neg_one = -1
one = 1

points[0] = [[neg_one], [neg_one], [one]]
points[1] = [[one], [neg_one], [one]]
points[2] = [[one], [one], [one]]
points[3] = [[neg_one], [one], [one]]
points[4] = [[one], [neg_one], [neg_one]]
points[5] = [[one], [neg_one], [neg_one]]
points[6] = [[one], [one], [neg_one]]
points[7] = [[neg_one], [one], [neg_one]]

pt0_x = neg_one
pt1_x = one
pt2_x = one
pt3_x = neg_one
pt4_x = neg_one
pt5_x = one
pt6_x = one
pt7_x = neg_one

def connect_point(i, j, k):
    a = k[i]
    b = k[j]
    pygame.draw.line(screen, black, (a[0], a[1]), (b[0], b[1]), 4)


def toRun(x_temp, y_temp, x_dir_change):
    global angle
    global neg_one
    global one
    global pt0_x
    global pt1_x
    global pt2_x
    global pt3_x
    global pt4_x
    global pt5_x
    global pt6_x
    global pt7_x
    index = 0
    one += x_temp
    neg_one -= y_temp

    print(str(one) + " " + str(neg_one))
    pt0_x += x_dir_change - y_temp
    pt1_x += x_dir_change + x_temp
    pt2_x += x_dir_change + x_temp
    pt3_x += x_dir_change - y_temp
    pt4_x += x_dir_change - y_temp
    pt5_x += x_dir_change + x_temp
    pt6_x += x_dir_change + x_temp
    pt7_x += x_dir_change - y_temp
    
    points[0] = [[pt0_x], [neg_one], [one]]
    points[1] = [[pt1_x], [neg_one], [one]]
    points[2] = [[pt2_x], [one], [one]]
    points[3] = [[pt3_x], [one], [one]]
    points[4] = [[pt4_x], [neg_one], [neg_one]]
    points[5] = [[pt5_x], [neg_one], [neg_one]]
    points[6] = [[pt6_x], [one], [neg_one]]
    points[7] = [[pt7_x], [one], [neg_one]]
        
    projected_points = [j for j in range(len(points))]

    rotation_x = [[1,0,0],
                 [0, math.cos(angle), -math.sin(angle)],
                 [0, math.sin(angle), math.cos(angle)]]

    rotation_y = [[math.cos(angle), 0, -math.sin(angle)],
                 [0, 1, 0],
                 [math.sin(angle), 0, math.cos(angle)]]

    rotation_z = [[math.cos(angle), -math.sin(angle), 0],
                 [math.sin(angle), math.cos(angle), 0],
                 [0, 0, 1]]

    for point in points:
        rotated_2d = matrix_multiplication(rotation_y, point)
        rotated_2d = matrix_multiplication(rotation_x, rotated_2d)
        rotated_2d = matrix_multiplication(rotation_z, rotated_2d)

        distance = 5

        z = 1/(distance - rotated_2d[2][0])
        projection_matrix = [[z, 0, 0],
                            [0, z, 0]]
        projected2d = matrix_multiplication(projection_matrix, rotated_2d)

        x = int(projected2d[0][0] * scale) + cube_position[0]
        y = int(projected2d[1][0] * scale) + cube_position[1]

        projected_points[index] = [x, y]
        pygame.draw.circle(screen, blue, (x,y), 10)
        index += 1

    for m in range(4):
        connect_point(m, (m+1)%4, projected_points)
        connect_point(m+4, (m+1)%4+4, projected_points)
        connect_point(m, m+4, projected_points)

    angle += speed
    pygame.display.update()

######
run = True
count = 0
count_2 = 0
while run:
    clock.tick(fps)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    toRun(0, 0, 0)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if(count < 2):
            count+=1

    if(count > 0):
        for i in range(50):
            toRun(0.02, 0.02, 0)
            screen.fill(white)

        for i in range(50):
            toRun(-0.02, -0.02, 0)
            screen.fill(white)
            count = 0

    if event.type == pygame.KEYDOWN:
        if(event.key == pygame.K_UP):
            if(count_2 < 2):
                count_2+=1
        
    if(count_2 > 0):
        for i in range(50):
            toRun(0, 0, i/200)
            screen.fill(white)

        for i in range(50):
            toRun(0, 0, -i/100)
            screen.fill(white)

        for i in range(50):
            toRun(0, 0, i/200)
            screen.fill(white)
            count_2 = 0

    ##toRun(-0.1, 0.1)
    ##toRun(0, 0)

pygame.quit()
