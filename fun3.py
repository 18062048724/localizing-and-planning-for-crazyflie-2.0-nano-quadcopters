# coding:utf-8
from math import *
import time
from cflib.positioning.motion_commander import MotionCommander


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')
    time.sleep(2)

def func3(in_q, scf):
    # cf = scf.cf
    with MotionCommander(scf) as mc:
        time.sleep(0.5)
        actiontime = time.time() + 8
        k0 = 0.0045
        k1 = 0.001
        k2 = 0.0013
        # 一次性飞到指定地点附近
        '''
        while (1):
            [green1, blue1,_] = in_q.get()
            if (green1 == [-1, -1]) | (blue1 == [-1, -1]):
                continue
            else:
                delta_raw = blue1[0] - (green1[0] + 85)
                delta_col = green1[1] - blue1[1]
                # lon = sqrt(delta_raw ** 2 + delta_col ** 2)
                mc.move_distance(round(k0 * delta_col, 3), round(k0 * delta_raw, 3), 0)
                mc.stop()
                break
        '''
        # 飞往转圈起点，微调位置
        while (1):
            # 到达转圈起点则进入转圈循环
            if time.time() > actiontime:
                print("destination reached")
                #mc.circle_left(0.3, velocity=0.1, angle_degrees=360 * 16)
                break
            #没有到达继续微调位置
            else:
                [green1, blue1, _] = in_q.get()
                print["fly to startpoint",green1, blue1]
                if (green1 == [-1, -1]) | (blue1 == [-1, -1]):
                    continue
                else:
                    # 转圈起点在绿色快右边0.3m处，往左转圈
                    delta_raw = blue1[0] - (green1[0] + 67)
                    delta_col = green1[1] - blue1[1]
                    if (delta_raw > -5) & (delta_raw < 5) & (delta_col > -5) & (delta_col < 5):
                        mc.stop
                    if (delta_raw > -10) & (delta_raw < 10) & (delta_col > -10) & (delta_col < 10):
                        mc.move_distance(round(k2 * delta_col, 3), round(k2 * delta_raw, 3), 0)
                    else:
                        mc.move_distance(round(k1 * delta_col, 3), round(k1 * delta_raw, 3), 0)
        #开始转圈
        m = 1
        while (1):
            [green1, blue1, _] = in_q.get()
            #print["circling",green1, blue1]
            if (green1 == [-1, -1]) | (blue1 == [-1, -1]):
                continue
            else:
                raw = green1[0] + 67 * cos(m * pi /24)
                col = green1[1] + 67 * sin(m * pi / 24)
                delta_raw = blue1[0] - raw
                delta_col = col - blue1[1]
                mc.move_distance(round(k0 * delta_col, 3), round(k0 * delta_raw, 3), 0,0.2)
                m += 1



def func4(in_q, scf):
    #第二架晚起飞10秒
    starttime = time.time() + 12
    # 把积累的多的数据都清空
    while (time.time() <= starttime):
        [_, _, _] = in_q.get()
        time.sleep(0.5)

    with MotionCommander(scf) as mc:
        time.sleep(1)
        k0 = 0.0045  # 1/224，
        k1 = 0.001
        k2 = 0.0013
        '''
        while (1):
            [green1,blue1, purple1] = in_q.get()
            if (green1 == [-1, -1]) | (purple1 == [-1, -1])|(blue1 == [-1, -1]):
                continue
            else:
                delta_r = blue1[0] - green1[0]
                delta_c = green1[1] - blue1[1]
                if (delta_r<0) & (delta_c<0):
                    delta_raw = purple1[0] - (green1[0] + 85)
                    delta_col = green1[1] - purple1[1]
                    # lon = sqrt(delta_raw ** 2 + delta_col ** 2)
                    mc.move_distance(round(k0 * delta_col, 3), round(k0 * delta_raw, 3), 0,0.4)
                    #mc.stop()
                    break
                else:
                    mc.stop()
        '''
        # 把积累的多的数据都清空
        for _ in range(8):
            [_, _, _] = in_q.get()
        #第一架飞过1/4圆后退出循环，第二架才开始转圈
        while (1):
            # Get some data
            [green1, blue1, purple1] = in_q.get()
            #print("receive", [green1, blue1, purple1])
            if (green1 == [-1, -1]) | (purple1 == [-1, -1]) | (blue1 == [-1, -1]):
                continue
            else:
                if (blue1[0] - green1[0] < 0) & (green1[1] - blue1[1] > 0):
                    print("the second plane start circling")
                    break
                else:
                    #第二架转圈起点也是绿色块右边0.3米处
                    delta_raw = purple1[0] - (green1[0] + 67)
                    delta_col = green1[1] - purple1[1]
                    delta=sqrt((blue1[0]-purple1[0])**2+(blue1[1]-purple1[1])**2)
                    if ((delta_raw > -5) & (delta_raw < 5) & (delta_col > -5) & (delta_col < 5))|(delta<56):
                        mc.stop
                    if (delta_raw > -10) & (delta_raw < 10) & (delta_col > -10) & (delta_col < 10):
                        mc.move_distance(round(k2 * delta_col, 3), round(k2 * delta_raw, 3), 0)
                    else:
                        mc.move_distance(round(k1 * delta_col, 3), round(k1 * delta_raw, 3), 0)
        #开始转圈
        m = 1
        while (1):
            [green1, blue1, purple1] = in_q.get()
            print("receive", [green1, blue1, purple1])
            if (green1 == [-1, -1]) | (purple1 == [-1, -1]) | (blue1 == [-1, -1]):
                continue
            else:
                delta=sqrt((blue1[0] - purple1[0]) ** 2 + (blue1[1] - purple1[1]) ** 2)
                if (delta>56):
                    raw = green1[0] + 67 * cos(m * pi / 24)
                    col = green1[1] + 67 * sin(m * pi / 24)
                    delta_raw = purple1[0] - raw
                    delta_col = col - purple1[1]
                    mc.move_distance(round(k0 * delta_col, 3), round(k0 * delta_raw, 3), 0,0.2)
                    m += 1



def func5(in_q, scf):

    while (1):
        [_, _, _] = in_q.get()
        time.sleep(0.5)