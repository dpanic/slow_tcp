import os
__DIR__ = os.path.dirname(os.path.realpath(__file__))


c = {
    'max_threads': 256,
    'listen_ports': [
        4443,
    ],
    'connection_delay': 5,
    'max_thread_alive': 50
}
