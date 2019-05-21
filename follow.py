

import cflib.crtp
from swarm_modified import Swarm

import fun3

import logging

logging.basicConfig(level=logging.ERROR)
# Change uris according to your setup
URI0 = 'radio://0/70/250K'
URI1 = 'radio://0/90/250K'
uris = [URI0, URI1]

#_sentinel = object()



if __name__ == '__main__':

    cflib.crtp.init_drivers(enable_debug_driver=False)
        
    with Swarm(uris) as swarm:
        swarm.parallel1(fun3.reset_estimator)
        swarm.parallel(uris,fun3.func3,fun3.func4)
