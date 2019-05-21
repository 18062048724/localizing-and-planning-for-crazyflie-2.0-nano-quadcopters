# -*- coding: cp936 -*-
import cv2
import numpy as np
def blue_center(hsi,height,width):
    
    #读取一副图像，输出中心在图像中的行列
    count_blue=0.0
    count_raw=0
    count_col=0
    #cv2.namedWindow("1")
    #cv2.namedWindow("2")
    #cv2.namedWindow("3")
    #(B, G, R) = cv2.split(rgb)  # 提取R、G、B分量
    (H,S,V) = cv2.split(hsi)#提取H、S、V分量
    for i in range(height):
        for j in range(width):
            if ((S[i][j]<0.3*255) | (V[i][j]<0.48*255) ):
                H[i][j]=0
            if ( (H[i][j] > 0.57 * 180 )&(H[i][j]< 0.61 * 180)):
                #H[i][j] = 0.9 * 180
                count_blue=count_blue+1
		count_raw += i
		count_col += j
		
            #else:
                #H[i][j]= 0
    
    if count_blue<10.0:
        x=-1
        y=-1
    else:
        xx=count_raw / count_blue
        yy=count_col / count_blue
        x=round(0.895*xx+12.63,2)
        y=round(0.895*yy+12.63,2)
    
    #cv2.imshow('1', H)
    #cv2.imshow('2', S)
    #cv2.imshow('3', V)        
    return [x,y]#打印灰度值
            

def red_center(hsi,height,width):
    

    count_red=0
    count_raw=0
    count_col=0
    #cv2.namedWindow("1")
    #cv2.namedWindow("2")
    #cv2.namedWindow("3")
    (H,S,V) = cv2.split(hsi)#提取H、S、V分量
    for i in range(height):
        for j in range(width):
            if ((S[i][j]<0.3*255) | (V[i][j]<0.48*255)):
                H[i][j]=0
            if ( (H[i][j] > 0.93 * 180 )&(H[i][j]< 0.97 * 180)):
                #H[i][j] = 0.9 * 180
                count_red=count_red+1
		count_raw += i
		count_col += j
		
            #else:
                #H[i][j]= 0
    
    if count_red==0:
        x=-1
        y=-1
    else:
        x=round(count_raw / count_red,2)
        y=round(count_col / count_red,2)
    
    #cv2.imshow('1', H)
    #cv2.imshow('2', S)
    #cv2.imshow('3', V)        
    return [x,y]#打印灰度值
            


def green_center(hsi,height,width):
    
    #读取一副图像，输出中心在图像中的行列
    count_green=0
    count_raw=0
    count_col=0
    #cv2.namedWindow("1")
    #cv2.namedWindow("2")
    #cv2.namedWindow("3")
    (H,S,V) = cv2.split(hsi)#提取H、S、V分量
    for i in range(height):
        for j in range(width):
            if ((S[i][j]<0.3*255) | (V[i][j]<0.48*255)):
                H[i][j]=0
            if ( (H[i][j] > 0.38 * 180 )&(H[i][j]< 0.45 * 180)):
                #H[i][j] = 0.9 * 180
                count_green=count_green+1
		count_raw += i
		count_col += j
		
            #else:
                #H[i][j]= 0
    
    if count_green==0:
        x=-1
        y=-1
    else:
        x=round(count_raw / count_green,2)
        y=round(count_col / count_green,2)
    
    #cv2.imshow('1', H)
    #cv2.imshow('2', S)
    #cv2.imshow('3', V)        
    return [x,y]#打印灰度值   
   


def multicolor_center(hsi,height,width):
    
    #读取一副图像，输出中心在图像中的行列
    count_red=0
    count_green=0
    count_blue=0
    count_purple = 0
    count_y=0
    count_raw_y=0
    count_col_y=0
    count_raw_purple = 0
    count_col_purple = 0
    count_raw_green=0
    count_col_green=0
    count_raw_red=0
    count_col_red=0
    count_raw_blue=0
    count_col_blue=0
    #cv2.namedWindow("1")
    #cv2.namedWindow("2")
    #cv2.namedWindow("3")
    (H,S,V) = cv2.split(hsi)#提取H、S、V分量
    for i in range(height):
        for j in range(width):
            if ((S[i][j]<0.3*255) | (V[i][j]<0.48*255)):
                H[i][j]=0
            #绿色
            if ( (H[i][j] > 0.38 * 180 )&(H[i][j]< 0.45 * 180)):
                count_green=count_green+1
                count_raw_green += i
                count_col_green += j

	    #蓝色
	    if ( (H[i][j] > 0.57 * 180 )&(H[i][j]< 0.61 * 180)):
                count_blue=count_blue+1
		count_raw_blue += i
		count_col_blue += j
            '''
	    #红色
	    if ( (H[i][j] > 0.93* 180 )&(H[i][j]< 0.97 * 180)):
                count_red=count_red+1
                count_raw_red += i
		count_col_red += j
		'''
	    #紫色
            if ((H[i][j] > 0.65 * 180) & (H[i][j] < 0.75 * 180)):
                count_purple = count_purple + 1
                count_raw_purple += i
                count_col_purple += j
            '''
		
            #黄色
            if ((H[i][j] > 0.15 * 180) & (H[i][j] < 0.17 * 180)):
                count_y = count_y + 1
                count_raw_y += i
                count_col_y += j
            '''
    
    if count_green<2:
        x1=-1
        y1=-1
    else:
        x1=round(count_raw_green/ float(count_green),2)
        y1=round(count_col_green/ float(count_green),2)

    if count_blue<10:
        x2=-1
        y2=-1
    else:
        x2=round((count_raw_blue / float(count_blue))*0.914+10.2,2)
        y2=round((count_col_blue/ float(count_blue))*0.914+13.76,2)
    '''

    if count_red<5:
        x3=-1
        y3=-1
    else:
        x3=round((count_raw_red / float(count_red))*1.11-13.33,2)
        y3=round((count_col_red / float(count_red))*1.11-20,2)
    '''
    if count_purple<10:
        x4=-1
        y4=-1
    else:
        x4=round((count_raw_purple/ float(count_purple))*0.914+10.2,2)
        y4=round((count_col_purple/ float(count_purple))*0.914+13.76,2)
    '''
    if count_y<10:
        x5=-1
        y5=-1
    else:
        x5=round((count_raw_y/ float(count_y))*1.11-13.33,2)
        y5=round((count_col_y/ float(count_y))*1.11-20,2)

    #cv2.imshow('1', H)
    #cv2.imshow('2', S)
    #cv2.imshow('3', V)
    
    print ("green: ",[x1,y1],"count_green: ",count_green,
           "blue: ",[x2,y2],"count_blue: ",count_blue,
           "red: ",[x3,y3],"count_red: ",count_red,
           "purple: ",[x4,y4],"count_purple: ",count_purple,
           "yellow: ",[x5,y5],"count_y: ",count_y)#打印
    '''
    #return [[x1,y1],[x2,y2],[x3,y3]]
    return [[x1, y1], [x2, y2], [x4,y4]]
    #print([[x1, y1], [x2, y2]])

