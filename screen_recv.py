from socket import socket
from zlib import decompress
import time
import pygame

WIDTH = 1280
HEIGHT = 720

def recvall(conn, length):
    """ Retreive all pixels. """

    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf


def main(host='192.168.1.162', port=5000):
    pygame.init()
    pygame.display.set_allow_screensaver(True)
    # Set the display mode to fullscreen
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    watching = True    

    while True:
        try:
            sock = socket()
            sock.connect((host, port))
            while watching:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        watching = False
                        break
    
                # Retreive the size of the pixels length, the pixels length and pixels
                size_len = int.from_bytes(sock.recv(1), byteorder='big')
                size = int.from_bytes(sock.recv(size_len), byteorder='big')
                pixels = decompress(recvall(sock, size))
    
                # Create the Surface from raw pixels
                img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')
    
                # Display the picture
                screen.blit(img, (0, 0))
                pygame.display.flip()
                clock.tick(60)
        except Exception as e:
            print(e)
            time.sleep(1)
            pass
        finally:
            sock.close()

    


if __name__ == '__main__':
    main()
