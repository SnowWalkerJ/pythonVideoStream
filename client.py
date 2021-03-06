#!/usr/bin/env python
import os
import subprocess
import sys

from compression.compressor import Compressor
from config.config import Config
from transport.client.UdpSocket import UdpSocket

# from encryption.encryptor import Encryptor
from camera.camera import Camera

sys.path.insert(0, os.getcwd())
import time


def main():
    # Clear the screen
    subprocess.call('clear', shell=True)
    config_object = Config(os.getcwd() + '/config/config.ini').raw_config_object
    transport = UdpSocket(config_object)
    camera = Camera(config_object)

    if config_object['COMPRESSION']['switch'] == 'On':
        compressor = Compressor(config_object)
        transport.add_compression(compressor)

    if config_object['ENCRYPTION']['switch'] == 'On':
        # encryptor = Encryptor(config_object)
        # transport.add_encryption(encryptor)
        pass

    try:
        while True:
            time.sleep(float(config_object['QUALITY']['delay']))
            image = camera.get_frame()
            transport.send_data(image)

    except LookupError as e:
        print(e)
        sys.exit(2)

    except KeyboardInterrupt:
        print('keyboard interruption')
        sys.exit(1)


if __name__ == "__main__":
    main()
