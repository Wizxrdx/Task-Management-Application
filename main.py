from src.task_manager import get_task_manager
from src.database import get_db

def main():
    try:
        db = get_db()
    except Exception as e:
        exit(e)

    task_manager = get_task_manager(db)

    while True:
        print('[1] Add a new task')
        print('[2] List all tasks')
        print('[3] update a task')
        print('[4] Mark a task as completed')
        print('[5] Start a task')
        print('[6] Delete a task')
        print('[7] Exit')

        try:
            choice = int(input('Enter the number of task: '))
        except ValueError:
            print('Enter a number.')
            continue
        except:
            print('\n')
            print('\n')
            print('\n')
            continue
        
        try:
            match choice:
                case 1:
                    task_manager.create_task()
                case 2:
                    task_manager.list_tasks()
                case 3:
                    task_manager.update_task()
                case 4:
                    task_manager.complete_task()
                case 5:
                    task_manager.start_task()
                case 6:
                    task_manager.delete_task()
                case 7:
                    print('Exiting...')
                    break
                case _:
                    print('Select from the choices below.')
        except KeyboardInterrupt:
            print('Return to main')

if __name__ == '__main__':
    main()