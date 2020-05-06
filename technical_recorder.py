import psutil

def ram_measure():
    ram = psutil.virtual_memory()
    return ram.percent

if __name__ == "__main__":
    print(ram_measure())

