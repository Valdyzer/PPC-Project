from multiprocessing import Process
import assets


if __name__ == '__main__':
    p = Process(target=assets.GAME)
    p.start()