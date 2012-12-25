import time

class SystemTimeSource():
    def get_time(self):
        return int(time.time())


if __name__ == "__main__":
    t = SystemTimeSource()
    print t.get_time()

