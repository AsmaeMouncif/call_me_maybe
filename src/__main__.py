import sys

def main():
    for index, arg in enumerate(sys.argv):
        if arg == "--input":
            print(sys.argv[index + 1])

if __name__ == "__main__":
    main()
