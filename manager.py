from task import Task
from datetime import date, timedelta
from typing import Optional, Dict, List
import json
import pathlib



class TaskManager:
    
    path_to_db = "data.json"
    
    def __init__(self) -> None:
        
        data = self.read_task()
        if data:
            self.all_task = {
                int(task_id): Task(**task) for task_id, task in data.items()
            }
            self.max_id = max(self.all_task.keys())
            
        else:
            self.all_task = {}
            self.max_id = 0
        
    def read_task(self) -> Optional[Dict]:
        "Чтение задач из файла"
        
        path = pathlib.Path(".") / self.path_to_db
        if path.exists():
            try:
                with open(file=self.path_to_db, mode="r") as file:
                    data = json.load(file)
                
                return data[0]
            except json.decoder.JSONDecodeError:
                pass
        
    
    def create_task(
        self,
        title: str,
        description: str,
        category: str,
        priority: str,
        due_date: Optional[str]=None,
        status: Optional[str]=None
    ) -> None:
        "Создание задачи"
        
        if due_date is None:
            due_date = date.today() + timedelta(days=2) # type: ignore
            due_date = due_date.__str__()
        
        current_id = self.max_id + 1
        task = Task(
            id=current_id,
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority,
            status=status if status else "Не выполнена"
        )
        self.all_task[current_id] = task
        
        print("Задача успешно создана")
        
    def save_to_json(self) -> None:
        "Сохранение задачи"

        with open(file=self.path_to_db, mode="w") as file:
            json.dump(
                [
                    {
                        task_id: task for task_id, task in self.all_task.items() 
                    }
                ],
                file,
                ensure_ascii=False,
                indent=4,
                default=lambda x: x.__dict__
            )
            
    def delete_task(
        self, 
        task_id: Optional[int]=None, 
        category: Optional[str]=None
    ) -> None:
        "Здесь происходит выбор метода для удаления задачи"
        
        if task_id:
            self.delete_by_id(task_id)
        
        elif category:
            self.delete_by_category(category)
        
        else:
            print("Задача не была удалена")
    
    def delete_by_id(self, task_id: int) -> None:
        "Удаление задачи по id"
        
        del self.all_task[task_id]
        print(f"Запись с id {task_id} успешно удалена")
        
    def delete_by_category(self, category: str) -> None:
        "Удаление задачи/задач по категории"
        
        tasks = []
        for task_id, task in self.all_task.items():
            if task.category.lower() == category.lower():
                tasks.append(task_id)
        
        if tasks:
            for task_id in tasks:
                del self.all_task[task_id]
            
            print(f"Удалено {len(tasks)} записей по категории {category}")
        
        else:
            print("Ничего не было удалено")
        
    def show_all_task(self) -> None:
        "Показ всех задач"
        
        for task in self.all_task.values():
            print(task)
    
    def show_task_by_category(self, category: str) -> None:
        "Показ задач по определенной категории"
        
        for task in self.all_task.values():
            if task.category.lower() == category.lower():
                print(task)

    def edit_task(
        self,
        id: int,
        title=Optional[str],
        description=Optional[str],
        category=Optional[str],
        due_date=Optional[str],
        priority=Optional[str],
        status=Optional[str]
    ) -> None:
        "Редактирование задач"
        
        task = self.all_task[id]

        if title:
            task.title = title # type: ignore
        elif description:
            task.description = description # type: ignore
            print(f"\n{description}\n")
        elif category:
            task.category = category # type: ignore
        elif priority:
            task.priority = priority # type: ignore
        elif status:
            task.status = status # type: ignore
            
        print("Объект успешно изменен")
    
    def commands(self, panel: List[str]) -> None:
        "Выполнение команд введенных пользователем"
        
        match panel[0]:
            case "--help":
                # TODO вынести это текст отдельно
                print("""
Ввод комманды и [аргументы, ...]
Есть следующие команды:
1) create [title, description, category, priority, date, status]
  Команда create требует всех аргументов
\ttitle- название задачи
\tdescription - описание задачи
\tcategory - категория, одно слово
\tpriority - [Низкий, Средний, Высокий]
\tdate - к какому сроку должна быть выполнена [YYYY-MM-DD]
\tstatus - [Выполнена, Не выполнена]
\tВсе аргументы вводятся в кавычках.
2) show [all, category]
\tall - показать все задачи
\tcategory - по определнной категории, введите ее
3) delete [id, category]
\tid - удаление по индефикатору
\tcategory - удаление по категории
4) edit [id] [-t ['str'], -d ['str'], -c ['str'], -p ['str'], -date ['str' YYYY-MM-DD], -s ['str']]
  Аргументы после указания флага вводяться в кавычках.
  Id вводиться без флага и требуеться обязательно для ввода
\t-t - название
\t-d - описание
\t-c - категория
\t-p - приоритет
\t-date - дата выполнения
\t-s - статус выполнения
                      """)
            case "create":
                try:
                    self.create_task(
                        title=panel[1],
                        description=panel[2],
                        category=panel[3],
                        priority=panel[4],
                        due_date=panel[5],
                        status=panel[6]
                    )
                    
                except IndexError:
                    print("Не верно введены аргументы")
            
            case "show":
                try:
                    if panel[1] == "all":
                        self.show_all_task()

                    else:
                        self.show_task_by_category(panel[1])

                except IndexError:
                    print("Не верно введены аргументы")
                    
            case "delete":
                try:
                    try:
                        self.delete_task(task_id=int(panel[1]))
                        
                    except ValueError: 
                        self.delete_task(category=panel[1])
                except IndexError:
                    print("Не верно введены аргументы")
                    
            case "edit":
                try:
                    if "-t" in panel:
                        self.edit_task(
                            id=int(panel[1]),
                            title=panel[panel.index("-t") + 1] # type: ignore
                        )
                    if "-d" in panel:
                        self.edit_task(
                            id=int(panel[1]),
                            description=panel[panel.index("-d") + 1] # type: ignore
                        )
                    if "-c" in panel:
                        self.edit_task(
                            id=int(panel[1]),
                            category=panel[panel.index("-c") + 1] # type: ignore
                        )
                    if "-p" in panel:
                        self.edit_task(
                            id=int(panel[1]),
                            priority=panel[panel.index("-p") + 1] # type: ignore
                        )
                    if "date" in panel:
                        self.edit_task(
                            id=int(panel[1]),
                            due_date=panel[panel.index("-date") + 1] # type: ignore
                        )
                    if "-s" in panel:
                        self.edit_task(
                            id=int(panel[1]),
                            status=panel[panel.index("-s") + 1] # type: ignore
                        )
                    
                except IndexError:
                    print("Не верно введены аргументы")
