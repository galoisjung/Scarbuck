import os.path


class Reducer:

    def __init__(self, offset_file):
        self.offset = offset_file

    def duplicate_writer(self, number):
        with open(self.offset, 'a') as f:
            f.write(str(number) + '\n')

    def duplicate_checker(self, number):
        if os.path.isfile(self.offset):
            with open(self.offset, 'r') as f:
                offset_list = f.read().splitlines()
            number = str(number)
            print(offset_list)
            if number in offset_list:
                print("True")
                return True
            else:
                print("False")
                return False
