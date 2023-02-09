import time

def timer(state):
    print("Starting timer!")
    secs = 0

    while True:
        time.sleep(1)
        secs += 1

        if state.empty():  # More accuracy within thread for timer
            break
        else:
            print(f"{secs} seconds...")