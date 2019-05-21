
# -*- coding:utf-8 -*-
# -*- coding: utf-8 -*-
import time
import cv2
import color
from threading import Thread
import Queue
#from queue import Queue
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from subprocess import *


class _Factory:

    def construct(self, uri):
        return SyncCrazyflie(uri)


class Swarm:
    """
    Runs a swarm of Crazyflies. It implements a functional-ish style of
    sequential or parallel actions on all individuals of the swarm.

    When the swarm is connected, a link is opened to each Crazyflie through
    SyncCrazyflie instances. The instances are maintained by the class and are
    passed in as the first argument in swarm wide actions.
    """

    def __init__(self, uris, factory=_Factory()):
        """
        Constructs a Swarm instance and instances used to connect to the
        Crazyflies

        :param uris: A set of uris to use when connecting to the Crazyflies in
        the swarm
        :param factory: A factory class used to create the instances that are
         used to open links to the Crazyflies. Mainly used for unit testing.
        """
        self._cfs = {}
        self._is_open = False

        for uri in uris:
            self._cfs[uri] = factory.construct(uri)

    def open_links(self):
        """
        Open links to all individuals in the swarm
        """
        if self._is_open:
            raise Exception('Already opened')

        try:
            self.parallel_safe1(lambda scf: scf.open_link())
            self._is_open = True
        except Exception as e:
            self.close_links()
            raise e

    def close_links(self):
        """
        Close all open links
        """
        for uri, cf in self._cfs.items():
            cf.close_link()

        self._is_open = False

    def __enter__(self):
        self.open_links()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_links()

 

    def parallel(self, uris,func1,func2):
        """
        Execute a function for all Crazyflies in the swarm, in parallel.
        One thread per Crazyflie is started to execute the function. The
        threads are joined at the end. Exceptions raised by the threads are
        ignored.

        For a description of the arguments, see sequential()

        :param func:
        :param args_dict:
        """
        try:
            self.parallel_safe(uris,func1,func2)
        except Exception:
            pass

    def parallel_safe(self, uris,func1,func2):
        """
        Execute a function for all Crazyflies in the swarm, in parallel.
        One thread per Crazyflie is started to execute the function. The
        threads are joined at the end and if one or more of the threads raised
        an exception this function will also raise an exception.

        For a description of the arguments, see sequential()

        :param func:
        :param args_dict:
        """
        # q = Queue.Queue()
        q1 = Queue.Queue()
        q2 = Queue.Queue()

        threads = []
        #线程1，
        scf1=self._cfs[uris[0]]
        thread1 = Thread(target=func1, args=(q1,scf1))
        threads.append(thread1)
        thread1.start()

        #线程2，
        scf2=self._cfs[uris[1]]
        thread2 = Thread(target=func2, args=(q2,scf2))
        threads.append(thread2)
        thread2.start()

        # 线程3，
        thread3 = Thread(target=self.funcexe, args=(q1,q2, ))
        threads.append(thread3)
        thread3.start()

        for thread in threads:
            thread.join()


    ####################################################################
    def func(self,q1,q2, height=240, width=320):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, height)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, width)
        time.sleep(2)  # 必须要此步骤，否则失败

        while (1):
            ret, rgb = cap.read()
            if ret == True:

                hsi = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)  # RGB to HSI
                [green, blue, purple] = color.multicolor_center(hsi, height, width)  # x是行,y是列
                q1.put([green, blue, purple])
                q2.put([green, blue , purple])
                print[green, blue, purple]
                #time.sleep(0.1)
            else:
                break
        q1.put([[-1, -1], [-1, -1]])
        q2.put([[-1, -1], [-1, -1]])
        cap.release()
        print("producer done")


    def funcexe(self,q1,q2):
        time.sleep(3)
        proc = Popen('G:\Color_New\Color_New\\x64\Debug\Color_New.exe', bufsize=1024, stdin=PIPE, stdout=PIPE)
        (fin, fout) = (proc.stdin, proc.stdout)

        while (1):
            n = 0
            gbp = [[], [], []]  # green,blue,purple
            while (n < 6):
                a = fout.readline()
                # print (a)
                # print (type(a))
                if a:
                    int1 = int(a)
                    if n < 2:
                        gbp[0].append(int1)
                    else:
                        if n < 4:
                            gbp[1].append(int1)
                        else:
                            gbp[2].append(int1)
                n = n + 1
                # print (type(int1))
            print (gbp)
            q1.put(gbp)
            q2.put(gbp)

    ####################################################################
    def parallel1(self, func, args_dict=None):
        """
        Execute a function for all Crazyflies in the swarm, in parallel.
        One thread per Crazyflie is started to execute the function. The
        threads are joined at the end. Exceptions raised by the threads are
        ignored.

        For a description of the arguments, see sequential()

        :param func:
        :param args_dict:
        """
        try:
            self.parallel_safe1(func, args_dict)
        except Exception:
            pass

    def parallel_safe1(self, func, args_dict=None):
        """
        Execute a function for all Crazyflies in the swarm, in parallel.
        One thread per Crazyflie is started to execute the function. The
        threads are joined at the end and if one or more of the threads raised
        an exception this function will also raise an exception.

        For a description of the arguments, see sequential()

        :param func:
        :param args_dict:
        """
        threads = []

        reporter = self.Reporter()

        for uri, scf in self._cfs.items():
            args = [func, reporter] + \
                self._process_args_dict(scf, uri, args_dict)

            thread =Thread(target=self._thread_function_wrapper, args=args)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if reporter.is_error_reported():
            raise Exception('One or more threads raised an exception when '
                            'executing parallel task')

    def _thread_function_wrapper(self, *args):
        try:
            func = args[0]
            reporter = args[1]
            func(*args[2:])
        except Exception:
            reporter.report_error()

    def _process_args_dict(self, scf, uri, args_dict):
        args = [scf]

        if args_dict:
            args += args_dict[uri]

        return args
    class Reporter:

        def __init__(self):
            self.error_reported = False

        def report_error(self):
            self.error_reported = True

        def is_error_reported(self):
            return self.error_reported







