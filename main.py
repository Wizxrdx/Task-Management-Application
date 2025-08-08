from src.task import TaskManager

def main():
    task_manager = TaskManager()
    while True:
        print('[1] Add a new task')
        print('[2] List all tasks')
        print('[3] update a task')
        print('[4] Mark a task as completed')
        print('[5] Delete a task')
        print('[6] Exit')

        try:
            x = int(input('Enter the number of task: '))
        except ValueError:
            print('Enter a number.')
            continue
        except:
            print('\n')
            print('\n')
            print('\n')
            continue
        
        try:
            if x == 1:
                task_manager.create_task()
            elif x == 2:
                task_manager.list_tasks()
            elif x == 3:
                task_manager.update_task()
            elif x == 4:
                task_manager.complete_task()
            elif x == 5:
                task_manager.delete_task()
            elif x == 6:
                print('6')
                break
            else:
                print('Select from the choices below.')
        except KeyboardInterrupt:
            print('Return to main')

if __name__ == '__main__':
    main()