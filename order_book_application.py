class Task:
    task_id = 0
    @classmethod
    def new_id(cls) -> int:
        cls.task_id += 1
        return cls.task_id

    def __init__(self, description: str, programmer: str, workload: int) -> None:
        self.__description = description
        self.__programmer = programmer
        self.__workload = workload
        self.__finished = False
        self.__id = Task.new_id()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def description(self) -> str:
        return self.__description

    @property
    def programmer(self) -> str:
        return self.__programmer

    @property
    def workload(self) -> int:
        return self.__workload

    def is_finished(self) -> bool:
        return self.__finished

    def mark_finished(self) -> None:
        self.__finished = True

    def __str__(self) -> str:
        return f"{self.id}: {self.description} ({self.workload} hours), programmer {self.programmer} {'' if self.is_finished() else 'NOT '}FINISHED"

class OrderBook:
    def __init__(self) -> None:
        self.__orders = {}

    @property
    def orders(self) -> dict:
        return self.__orders
    
    def add_order(self, description: str, programmer: str, workload: int) -> None:
        """Add a new order to the OrderBook"""
        order = Task(description, programmer, workload)
        self.orders[order.id] = order

    def all_orders(self) -> list:
        """Return a list of all the tasks stored in the OrderBook"""
        return list(self.orders.values())

    def programmers(self) -> list:
        """Return a list of the names of all the programmers with tasks stored in the OrderBook
        The list contains each programmer only once using a set"""
        return list({order.programmer for order in self.all_orders()})
        
    def mark_finished(self, id: int) -> None:
        """Take the id of the task as argument and mark the relevant task as finished
        If there is no task with the given id, raise a ValueError exception"""
        if id in self.orders:
            self.orders[id].mark_finished()
        else:
            raise ValueError("There is not any order with that id.")
    
    def finished_orders(self) -> list:
        """Return a list containing the finished tasks from the OrderBook"""
        return [order for order in self.all_orders() if order.is_finished()]

    def unfinished_orders(self) -> list:
        """Return a list containing the unfinished tasks from the OrderBook"""
        return [order for order in self.all_orders() if not order.is_finished()]
    
    def status_of_programmer(self, programmer: str) -> tuple:
        """
        Return the number of finished and unfinished tasks the programmer has assigned to them, along with the estimated hours in both categories
        """
        if programmer not in self.programmers():
            raise ValueError(f"{programmer} does not have a task")
        
        count_finished = 0
        count_unfinished = 0
        workload_finished = 0
        workload_unfinished = 0

        for order in self.all_orders():
            if order.programmer == programmer:
                if order.is_finished():
                    count_finished += 1
                    workload_finished += order.workload
                else:
                    count_unfinished += 1
                    workload_unfinished += order.workload
        
        return (
            count_finished,
            count_unfinished,
            workload_finished,
            workload_unfinished,
        )

class Application:
    def __init__(self) -> None:
        self.__book = OrderBook()
    
    @property
    def book(self) -> OrderBook:
        return self.__book

    def help(self) -> None:
        print("commands:")
        print("0 exit")
        print("1 add order")
        print("2 list finished tasks")
        print("3 list unfinished tasks")
        print("4 mark task as finished")
        print("5 programmers")
        print("6 status of programmer")
    
    def add_order(self) -> None:
        description = input("description: ")
        data = input("programmer and workload estimate: ")
        try:
            programmer, workload = data.split()
            self.book.add_order(description, programmer, int(workload))
        except ValueError:
            print("erroneous input")
        else:
            print("added!")

    def finished_orders(self) -> None:
        finished_orders = self.book.finished_orders()
        if len(finished_orders) == 0:
            print("no finished tasks")
        else:
            for order in finished_orders:
                print(order)
       
    def unfinished_orders(self) -> None:
        unfinished_orders = self.book.unfinished_orders()
        if len(unfinished_orders) == 0:
            print("no unfinished tasks")
        else:
            for order in unfinished_orders:
                print(order)
                         
    def mark_finished(self) -> None:
        try:
            id = int(input("id:"))
            self.book.mark_finished(id=id)
        except ValueError:
            print("erroneous input")
        else:
            print("marked as finished")

    def programmers(self) -> None:
        for programmer in self.book.programmers():
            print(programmer)

    def status_of_programmer(self) -> None:
        programmer = input("programmer: ")
        try:
            status =self.book.status_of_programmer(programmer)
        except ValueError:
            print("erroneous input")
        else:    
            template = "tasks: finished {} not finished {}, hours: done {} scheduled {}"
            print(template.format(*status))

    def execute(self) -> None:
        self.help()

        while True:
            print()
            command = input("command: ")
            if command == "1":
                self.add_order()
            elif command == "2":
                self.finished_orders()
            elif command == "3":
                self.unfinished_orders()
            elif command == "4":
                self.mark_finished()
            elif command == "5":
                self.programmers()
            elif command == "6":
                self.status_of_programmer()
            elif command == "0":
                break
            else:
                self.help()

Application().execute()
