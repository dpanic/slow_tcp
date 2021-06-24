#!/usr/bin/python3

import os
__DIR__ = os.path.dirname(os.path.realpath(__file__))
import time
import socket
import sys

import config
from modules import threading_control
from modules import logger
import _thread as thread


class HoneyPot:

    def __init__(self):
        logger.dump('SLOW TCP v1', 'debug')

        # configuration part
        self.max_threads = config.c['max_threads']
        self.max_live_time = 0

        # this defines timeout
        self.max_thread_alive = config.c['max_thread_alive']

        # references
        self.ref_tc = threading_control.threading_control(self.max_live_time, max_threads=self.max_threads)

    #
    # Client connection
    #

    def client(self, port, connection, addr):
        self.ref_tc.inc_threads()

        connection.settimeout(30.0)
        logger.dump('delaying {!r} seconds'.format(config.c['connection_delay']), 'info')
        time.sleep(config.c['connection_delay'])
        data = connection.recv(4 * 1024)

        logger.dump('received {!r}'.format(data), 'debug')
        if not data:
            print('no more data from', connection)

        connection.sendall(b'OK\r\n')
        self.ref_tc.dec_threads()
        logger.dump('Closing socket', 'info')

    #
    # Main thread
    #
    def run(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = '0.0.0.0'

        try:
            s.bind((host, port))
        except BaseException:
            logger.dump('%s:%s error listening! %s' % (host, port, sys.exc_info()), 'error')
            try:
                s.close()
            except BaseException:
                pass
            return False

        logger.dump('%s:%s started!' % (host, port), 'info')
        s.listen(self.max_threads)

        while True:
            self.ref_tc.wait_threads()
            connection, addr = s.accept()
            logger.dump("<- %s" % (str(addr)), 'good')
            thread.start_new_thread(self.client, (port, connection, addr))

        s.close()

    #
    # Long run
    #
    def long_run(self):
        while True:
            time.sleep(60)


if __name__ == '__main__':

    hpot = HoneyPot()
    for port in config.c['listen_ports']:
        thread.start_new_thread(hpot.run, (port,))

    hpot.long_run()
