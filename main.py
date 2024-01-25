from multiprocessing import Process, Value
import assets


if __name__ == '__main__':
    connecting = Value('i', 0)
    start = Value('i', 0)

    p = Process(target=assets.GAME, args=(connecting, start))
    p.start()

    i = 0
    while(True):
        if (connecting.value <= 5) and (i != connecting.value):
            p = Process(target=assets.PLAYER)
            p.start()
            print(connecting.value)
            i += 1 
        elif connecting.value == 5:
            break