import random

def test_func(new_list):
    new_list.append(5)


def main():  
    new_list = [0, 1, 2, 3, 4]
    test_func(new_list)
    print(new_list)

if __name__ == "__main__":
    main()