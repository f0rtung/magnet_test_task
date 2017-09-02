def read_file(file_path):
    try:
        with open(file_path) as file:
            return "".join(file.readlines())
    except OSError as err:
        print(err)
