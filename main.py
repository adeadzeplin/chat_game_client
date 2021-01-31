from clientsocket import run_client_socket
from king_ttv_game import play_Koth
import multiprocessing


def main():
    queue_dict = {
        'queueue': multiprocessing.Queue(),
        'request_import': multiprocessing.Queue(),
        'request_export': multiprocessing.Queue()
    }

    # serverDEBUGip = 'http://192.168.1.20:3333'



    client_socket_process = multiprocessing.Process(target=run_client_socket, args=(queue_dict,))
    client_socket_process.start()
    King_of_the_hill_process = multiprocessing.Process(target=play_Koth, args=(queue_dict,))
    King_of_the_hill_process.start()

    client_socket_process.join()
    King_of_the_hill_process.join()


if __name__ == '__main__':
    main()
