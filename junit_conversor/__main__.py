import sys

from . import _convert


def main():
    if len(sys.argv[1:]) == 2:
        input, destination_file = sys.argv[1:]
    else:
        message = "Two input parameters, the input filename and output filename, have to be supplied."
        raise IndexError(message)

    _convert(input, destination_file)
    sys.stdout.write("File %s was created successfully" % destination_file)
    sys.exit(0)

if __name__ == "__main__":
    main()
