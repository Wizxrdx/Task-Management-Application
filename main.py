def main():
    while True:
        print('[1] Add a new task')
        print('[2] List all tasks')
        print('[3] update a task')
        print('[4] Mark a task as completed')
        print('[5] Delete a task')

        try:
            x = int(input('Enter the number of task: '))
        except ValueError:
            print('Enter a number.')
            continue

        if x == 1:
            print('1')
        elif x == 2:
            print('2')
        elif x == 3:
            print('3')
        elif x == 4:
            print('4')
        elif x == 5:
            print('5')
        else:
            print('Select from the choices below.')


if __name__ == '__main__':
    main()