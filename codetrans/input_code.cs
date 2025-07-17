using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;

interface IEntity
{
    Guid Id { get; }
}

class Employee : IEntity
{
    public Guid Id { get; } = Guid.NewGuid();
    public string Name { get; set; }
    public string Department { get; set; }
    public double Salary { get; set; }
}

class EmployeeNotFoundException : Exception
{
    public EmployeeNotFoundException(string message) : base(message) { }
}

class EmployeeManager
{
    private List<Employee> employees = new();

    public void AddEmployee(Employee emp) => employees.Add(emp);

    public Employee GetHighestPaidEmployee(string department)
    {
        var emp = employees
            .Where(e => e.Department == department)
            .OrderByDescending(e => e.Salary)
            .FirstOrDefault();

        return emp ?? throw new EmployeeNotFoundException($"No employee found in {department}");
    }

    public async Task SaveToFileAsync(string filePath)
    {
        var json = JsonSerializer.Serialize(employees);
        await File.WriteAllTextAsync(filePath, json);
    }

    public async Task LoadFromFileAsync(string filePath)
    {
        if (!File.Exists(filePath)) return;

        var json = await File.ReadAllTextAsync(filePath);
        employees = JsonSerializer.Deserialize<List<Employee>>(json) ?? new List<Employee>();
    }
}

class Program
{
    static async Task Main()
    {
        var manager = new EmployeeManager();

        manager.AddEmployee(new Employee { Name = "Alice", Department = "HR", Salary = 70000 });
        manager.AddEmployee(new Employee { Name = "Bob", Department = "IT", Salary = 90000 });
        manager.AddEmployee(new Employee { Name = "Charlie", Department = "IT", Salary = 85000 });

        try
        {
            var topIT = manager.GetHighestPaidEmployee("IT");
            Console.WriteLine($"Top IT Employee: {topIT.Name}, Salary: {topIT.Salary}");
        }
        catch (EmployeeNotFoundException ex)
        {
            Console.WriteLine(ex.Message);
        }

        string filePath = "employees.json";
        await manager.SaveToFileAsync(filePath);
        Console.WriteLine("Employees saved to file.");
    }
}
