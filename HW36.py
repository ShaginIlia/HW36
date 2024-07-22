import threading
import time
from queue import Queue


class Table:
    def __init__(self, number, is_busy=False):
        self.number = int(number)
        self.is_busy = is_busy
        self.lock = threading.Lock()


class Customer(threading.Thread):
    def __init__(self, customer_count, table_number):
        threading.Thread.__init__(self)
        self.customer_count = customer_count
        self.table_number = table_number

    def run(self):
        with self.table.lock:
            print(f'Гость {self.customer_count} сел за столик номер {self.table_number}')
            time.sleep(5)
            print(f'Гость {self.customer_count} ушёл')
            self.table.is_busy = False


class Kafe:
    def __init__(self, tables):
        self.queue = Queue()
        self.tables = tables

    def customer_arrival(self):
        customer_count = 0
        while True:
            customer_count += 1
            self.queue.put(customer_count)
            print(f'Гость {customer_count} прибыл и добавлен в очередь')
            time.sleep(2)

    def serve_customer(self):
        while True:
            if not self.queue.empty():
                customer_count = self.queue.get()
                for table in self.tables:
                    if not table.is_busy:
                        table.is_busy = True
                        cust = Customer(customer_count, table.number)
                        cust.table = table
                        cust.start()
                        break
                else:
                    print(f'Все столики заняты. Гость {customer_count} в очереди')
            time.sleep(1)


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Kafe(tables)

customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

serve_customer_thread = threading.Thread(target=cafe.serve_customer)
serve_customer_thread.start()




