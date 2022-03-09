from multiprocessing import Process, Queue, Pipe
import time
import datetime
import codecs


def process_a(q, pipe):
    while True:
        msg = q.get()
        time.sleep(5)
        pipe.send(msg.lower())


def process_b(input_pipe, output_pipe):
    while True:
        output_pipe.send(codecs.encode(input_pipe.recv(), "rot_13"))


if __name__ == "__main__":
    to_b, from_a = Pipe()
    to_main, from_b = Pipe()
    queue = Queue()

    Process(target=process_a, args=(queue, to_b), daemon=True).start()
    Process(target=process_b, args=(from_a, to_main), daemon=True).start()

    with open("artifacts/hard.txt", "w") as f:
        while True:
            message = input(">>> ")
            if message == 'q':
                f.write(f'{datetime.datetime.now().isoformat()} exit\n')
                break

            f.write(f'{datetime.datetime.now().isoformat()} receive `{message}`\n')
            queue.put(message)
            message = from_b.recv()
            f.write(f'{datetime.datetime.now().isoformat()} done `{message}`\n')
            print(message)
