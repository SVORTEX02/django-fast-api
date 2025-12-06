class Employee:
    amount=100
    def __init__(self,first_name,last_name,age):
        self.first_name=first_name
        self.last_name=last_name
        self.age=age

    def fullname(self):
        print(f"FUllName: {self.first_name+self.last_name}")
        
    def toPay(self):
        print(f"your pay:{self.amount}")
emp=Employee("Raj","sharma",23)
emp2=Employee("Patrick","James",34)

emp.fullname()
emp2.fullname()

emp.toPay()


def main_one(fn):
    def in_one():
        print("Hello this si the inner function")
        fn()
    return in_one()


@main_one
def greet():
    print("helo this is vorex ")