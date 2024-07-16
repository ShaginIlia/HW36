import threading
import time
from queue import Queue


class Table:
    def __init__(self, number, is_busy=False):
        self.number = int(number)
        self.is_busy = is_busy


class Customer(threading.Thread):
    def __init__(self, customer_count):
        threading.Thread.__init__(self)
        self.customer_count = customer_count

    def run(self):
        print('Гость на обслуживании')


class Kafe:


    def __init__(self, tables):
        self.queue = Queue()
        self.tables = tables


    def customer_arrival(self):
        customer_count = 0
        while True:
            cust = Customer(customer_count)
            customer_count += 1
            self.queue.put(cust)
            print(f'Гость {customer_count} прибыл. ')
            time.sleep(1)

    def serve_customer(self, cust):
        for table in self.tables:
            if not table.is_busy:
                print(f'Гость садиться за свободный столик номер')
                table.is_busy = True
                cust.start()
                time.sleep(5)
                table.is_busy = False
                print(f'Гость ушёл')
                break
            else:
                print('Все столики заняты. Гость в очереди')


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Kafe(tables)

customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

while True:
    if not cafe.queue.empty():
        customer = cafe.queue.get()
        cafe.serve_customer(customer)







