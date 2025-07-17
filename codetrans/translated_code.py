import json
import uuid
import asyncio

class IEntity:
    def __init__(self):
        self.Id = uuid.uuid4()

class Employee(IEntity):
    def __init__(self, name, department, salary):
        super().__init__()
        self.Name = name
        self.Department = department
        self.Salary = salary

    def to_dict(self):
        return {
            'Id': str(self.Id),
            'Name': self.Name,
            'Department': self.Department,
            'Salary': self.Salary
        }

    @classmethod
    def from_dict(cls, data):
        employee = cls(data['Name'], data['Department'], data['Salary'])
        employee.Id = uuid.UUID(data['Id'])
        return employee


class EmployeeNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)

class EmployeeManager:
    def __init__(self):
        self.employees = []

    def add_employee(self, emp):
        self.employees.append(emp)

    def get_highest_paid_employee(self, department):
        filtered_employees = [e for e in self.employees if e.Department == department]
        if not filtered_employees:
            raise EmployeeNotFoundException(f"No employee found in {department}")
        
        highest_paid = max(filtered_employees, key=lambda e: e.Salary)
        return highest_paid

    async def save_to_file_async(self, file_path):
        employee_dicts = [emp.to_dict() for emp in self.employees]
        json_data = json.dumps(employee_dicts, indent=4)
        
        with open(file_path, 'w') as f:
            f.write(json_data)

    async def load_from_file_async(self, file_path):
        try:
            with open(file_path, 'r') as f:
                json_data = f.read()
                employee_dicts = json.loads(json_data)
                self.employees = [Employee.from_dict(data) for data in employee_dicts]
        except FileNotFoundError:
            pass

async def main():
    manager = EmployeeManager()

    manager.add_employee(Employee("Alice", "HR", 70000))
    manager.add_employee(Employee("Bob", "IT", 90000))
    manager.add_employee(Employee("Charlie", "IT", 85000))

    try:
        top_it = manager.get_highest_paid_employee("IT")
        print(f"Top IT Employee: {top_it.Name}, Salary: {top_it.Salary}")
    except EmployeeNotFoundException as ex:
        print(ex)

    file_path = "employees.json"
    await manager.save_to_file_async(file_path)
    print("Employees saved to file.")

if __name__ == "__main__":
    asyncio.run(main())