# Python Scripting Interview Questions & Answers

## 🐍 **Python Fundamentals**

### 1. What is Python and what are its key features?

**Answer:**
Python is a high-level, interpreted programming language known for its simplicity and readability.

**Key Features:**
- **Interpreted**: No compilation needed
- **Dynamic typing**: Variable types determined at runtime
- **Object-oriented**: Supports OOP principles
- **Extensive libraries**: Large standard library
- **Cross-platform**: Runs on Windows, Linux, macOS
- **Readable syntax**: Easy to learn and maintain
- **Versatile**: Web development, automation, data science, DevOps

**Use Cases in DevOps:**
- Automation scripts
- Configuration management
- CI/CD pipelines
- Infrastructure automation
- Monitoring and alerting
- API development

---

### 2. What are Python data types?

**Answer:**
**Basic Data Types:**
```python
# Numbers
integer = 42
float_num = 3.14
complex_num = 3 + 4j

# Strings
string = "Hello, World!"
multiline = """Multi-line
string"""

# Boolean
is_true = True
is_false = False

# None
value = None
```

**Collection Types:**
```python
# List (mutable, ordered)
my_list = [1, 2, 3, "hello"]
my_list.append(4)
my_list[0] = 10

# Tuple (immutable, ordered)
my_tuple = (1, 2, 3, "hello")
# my_tuple[0] = 10  # Error: tuples are immutable

# Dictionary (mutable, key-value pairs)
my_dict = {"name": "John", "age": 30}
my_dict["city"] = "NYC"

# Set (mutable, unordered, unique)
my_set = {1, 2, 3, 4}
my_set.add(5)
```

**Type Checking:**
```python
type(variable)           # Get type
isinstance(variable, int)  # Check type
```

---

### 3. How do you work with strings in Python?

**Answer:**
**String Operations:**
```python
# Concatenation
str1 = "Hello"
str2 = "World"
result = str1 + " " + str2  # "Hello World"

# Formatting
name = "John"
age = 30
# f-strings (Python 3.6+)
message = f"My name is {name} and I'm {age} years old"

# format() method
message = "My name is {} and I'm {} years old".format(name, age)

# % formatting (legacy)
message = "My name is %s and I'm %d years old" % (name, age)

# String methods
text = "Hello World"
text.upper()            # "HELLO WORLD"
text.lower()            # "hello world"
text.split()            # ["Hello", "World"]
text.replace("World", "Python")  # "Hello Python"
text.strip()            # Remove whitespace
```

**String Slicing:**
```python
text = "Hello World"
text[0]                 # 'H'
text[0:5]               # 'Hello'
text[:5]                # 'Hello'
text[6:]                # 'World'
text[-1]                # 'd' (last character)
```

---

### 4. How do you work with lists and dictionaries?

**Answer:**
**Lists:**
```python
# Create list
my_list = [1, 2, 3, 4, 5]

# Access elements
my_list[0]              # 1
my_list[-1]             # 5 (last element)

# Modify
my_list[0] = 10
my_list.append(6)      # Add to end
my_list.insert(0, 0)    # Insert at index
my_list.remove(3)       # Remove value
my_list.pop()           # Remove and return last
my_list.pop(0)          # Remove at index

# List operations
len(my_list)            # Length
my_list + [7, 8]        # Concatenate
[1, 2] * 3              # Repeat: [1, 2, 1, 2, 1, 2]

# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]
```

**Dictionaries:**
```python
# Create dictionary
my_dict = {"name": "John", "age": 30, "city": "NYC"}

# Access
my_dict["name"]         # "John"
my_dict.get("name")     # "John"
my_dict.get("email", "N/A")  # Default if key missing

# Modify
my_dict["age"] = 31
my_dict["email"] = "john@example.com"
my_dict.update({"country": "USA"})

# Remove
del my_dict["city"]
value = my_dict.pop("age")

# Iterate
for key, value in my_dict.items():
    print(f"{key}: {value}")

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}
```

---

### 5. How do you use control flow in Python?

**Answer:**
**Conditionals:**
```python
# if/elif/else
age = 20
if age < 18:
    print("Minor")
elif age < 65:
    print("Adult")
else:
    print("Senior")

# Ternary operator
status = "Adult" if age >= 18 else "Minor"

# Multiple conditions
if age >= 18 and age < 65:
    print("Working age")
```

**Loops:**
```python
# for loop
for i in range(5):
    print(i)

for item in [1, 2, 3, 4, 5]:
    print(item)

# while loop
count = 0
while count < 5:
    print(count)
    count += 1

# Loop control
for i in range(10):
    if i == 5:
        break           # Exit loop
    if i % 2 == 0:
        continue        # Skip iteration
    print(i)

# enumerate
for index, value in enumerate(['a', 'b', 'c']):
    print(f"{index}: {value}")
```

---

### 6. How do you define and use functions in Python?

**Answer:**
**Function Definition:**
```python
# Basic function
def greet():
    print("Hello, World!")

# Function with parameters
def greet(name):
    print(f"Hello, {name}!")

# Function with default parameters
def greet(name="Guest"):
    print(f"Hello, {name}!")

# Function with return value
def add(a, b):
    return a + b

# Function with multiple return values
def get_name_age():
    return "John", 30

name, age = get_name_age()

# Function with *args
def sum_all(*args):
    return sum(args)

sum_all(1, 2, 3, 4)    # 10

# Function with **kwargs
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="John", age=30)
```

**Lambda Functions:**
```python
# Lambda (anonymous function)
square = lambda x: x**2
square(5)              # 25

# Use with map, filter
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

---

### 7. How do you handle files in Python?

**Answer:**
**File Operations:**
```python
# Read file
with open('file.txt', 'r') as f:
    content = f.read()
    # or
    lines = f.readlines()
    # or
    for line in f:
        print(line.strip())

# Write file
with open('file.txt', 'w') as f:
    f.write("Hello, World!\n")
    f.writelines(["Line 1\n", "Line 2\n"])

# Append to file
with open('file.txt', 'a') as f:
    f.write("New line\n")

# Binary files
with open('image.jpg', 'rb') as f:
    data = f.read()

# JSON files
import json
with open('data.json', 'r') as f:
    data = json.load(f)

with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)
```

**File Modes:**
- `'r'`: Read (default)
- `'w'`: Write (overwrites)
- `'a'`: Append
- `'x'`: Exclusive creation
- `'b'`: Binary mode
- `'t'`: Text mode (default)
- `'+'`: Read and write

---

### 8. How do you handle exceptions in Python?

**Answer:**
**Exception Handling:**
```python
# Basic try/except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

# Multiple exceptions
try:
    value = int(input("Enter number: "))
    result = 10 / value
except ValueError:
    print("Invalid input")
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"Error: {e}")

# else and finally
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Error")
else:
    print("No error occurred")
finally:
    print("This always executes")

# Raise exception
if value < 0:
    raise ValueError("Value must be positive")

# Custom exception
class CustomError(Exception):
    pass

raise CustomError("Custom error message")
```

---

### 9. How do you work with modules and packages?

**Answer:**
**Importing Modules:**
```python
# Import module
import os
os.getcwd()

# Import with alias
import os as operating_system

# Import specific function
from os import getcwd
getcwd()

# Import all (not recommended)
from os import *

# Import from package
from mypackage import mymodule
from mypackage.mymodule import myfunction
```

**Creating Modules:**
```python
# mymodule.py
def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

# Using module
import mymodule
mymodule.greet("John")
```

**Package Structure:**
```
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
```

---

### 10. How do you use Python for DevOps automation?

**Answer:**
**File Operations:**
```python
import os
import shutil

# Directory operations
os.makedirs('newdir', exist_ok=True)
os.chdir('newdir')
os.getcwd()
os.listdir('.')

# File operations
shutil.copy('source.txt', 'dest.txt')
shutil.move('old.txt', 'new.txt')
os.remove('file.txt')
```

**Subprocess:**
```python
import subprocess

# Run command
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
print(result.stdout)

# Run shell command
result = subprocess.run('ls -l | grep .py', shell=True, capture_output=True)

# Check return code
if result.returncode == 0:
    print("Success")
else:
    print("Error")
```

**JSON/YAML:**
```python
import json
import yaml

# JSON
with open('config.json') as f:
    config = json.load(f)

# YAML
with open('config.yaml') as f:
    config = yaml.safe_load(f)
```

**Requests (HTTP):**
```python
import requests

# GET request
response = requests.get('https://api.example.com/data')
data = response.json()

# POST request
response = requests.post('https://api.example.com/data', json={'key': 'value'})
```

---

### 11. How do you use Python with AWS/Azure/GCP?

**Answer:**
**AWS (boto3):**
```python
import boto3

# Create client
s3 = boto3.client('s3')
ec2 = boto3.client('ec2')

# S3 operations
s3.create_bucket(Bucket='my-bucket')
s3.upload_file('local.txt', 'my-bucket', 'remote.txt')
s3.download_file('my-bucket', 'remote.txt', 'local.txt')

# EC2 operations
instances = ec2.describe_instances()
ec2.run_instances(ImageId='ami-123', MinCount=1, MaxCount=1)
```

**Azure:**
```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

credential = DefaultAzureCredential()
blob_service = BlobServiceClient(account_url, credential=credential)
```

**GCP:**
```python
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('my-bucket')
blob = bucket.blob('file.txt')
blob.upload_from_filename('local.txt')
```

---

### 12. How do you test Python code?

**Answer:**
**Unit Testing (unittest):**
```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
```

**pytest:**
```python
# test_math.py
def test_add():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, 1) == 0
```

**Running Tests:**
```bash
# unittest
python -m unittest test_math.py

# pytest
pytest test_math.py
pytest -v  # Verbose
```

---

## 📝 **Best Practices**

1. **PEP 8**: Follow Python style guide
2. **Documentation**: Use docstrings
3. **Error handling**: Use try/except appropriately
4. **Virtual environments**: Use venv or virtualenv
5. **Dependencies**: Use requirements.txt
6. **Testing**: Write unit tests
7. **Code organization**: Use modules and packages
8. **Type hints**: Use type annotations (Python 3.5+)
9. **Logging**: Use logging module instead of print
10. **Security**: Validate input, avoid eval()

---

**Good luck with your Python Scripting interview preparation!**
