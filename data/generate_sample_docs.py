"""
Generates a small set of sample "study notes" PDFs so the project has a
real, working document collection out of the box for the demo.

These are short, simple, and text-extractable on purpose -- they are meant
as a STARTER corpus. For your actual submission, feel free to replace the
files in data/raw_docs/ with your own PDFs (lecture notes, course slides
exported as PDF, textbook chapters, etc.) as long as they are text-based
(not scanned images).

Run with:
    python data/generate_sample_docs.py
"""

import os

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "raw_docs")

DOCUMENTS = {
    "python_basics.pdf": {
        "title": "Python Basics: Variables and Data Types",
        "paragraphs": [
            "A variable in Python is a named container used to store a value in memory. "
            "You create a variable simply by assigning a value to a name, for example: "
            "age = 25. Python does not require you to declare the type of a variable "
            "in advance; the type is determined automatically based on the value assigned.",

            "Python has several built-in data types. The most common ones are int for "
            "whole numbers, float for decimal numbers, str for text (strings), and bool "
            "for True/False values. There are also collection types such as list, tuple, "
            "dict, and set, which allow you to store multiple values together.",

            "Variable names in Python must start with a letter or an underscore, and can "
            "contain letters, digits, and underscores. Python is case-sensitive, so 'age' "
            "and 'Age' are treated as two different variables. By convention, variable "
            "names use lowercase letters with underscores between words (snake_case).",

            "You can check the type of any variable using the built-in type() function, "
            "for example type(age) will return <class 'int'>. Python also allows dynamic "
            "typing, meaning the same variable name can be reassigned to a value of a "
            "different type later in the program.",
        ],
    },
    "python_functions.pdf": {
        "title": "Python Basics: Functions",
        "paragraphs": [
            "A function in Python is a reusable block of code that performs a specific "
            "task. Functions are defined using the def keyword, followed by the function "
            "name and parentheses, for example: def greet(name): return f'Hello, {name}'.",

            "Functions can accept input values called parameters (or arguments when you "
            "actually pass values in when calling the function). A function can also "
            "return a value back to the caller using the return statement. If a function "
            "has no return statement, it returns None by default.",

            "Default parameter values let you make some arguments optional. For example, "
            "def greet(name, greeting='Hello'): return f'{greeting}, {name}' lets you call "
            "greet('Sara') and get 'Hello, Sara', or greet('Sara', 'Hi') to get 'Hi, Sara'.",

            "Functions help avoid repeating the same code multiple times, make programs "
            "easier to test and debug, and allow you to break a complex problem down into "
            "smaller, well-named pieces. This is a core idea behind writing clean code.",
        ],
    },
    "data_structures.pdf": {
        "title": "Data Structures: Lists, Dictionaries, and Sets",
        "paragraphs": [
            "A list in Python is an ordered, changeable (mutable) collection of items, "
            "written with square brackets, for example: fruits = ['apple', 'banana', "
            "'cherry']. You can access items by their index, starting at 0, and you can "
            "add, remove, or change items after the list is created.",

            "A dictionary stores data as key-value pairs, written with curly braces, for "
            "example: student = {'name': 'Ali', 'age': 21}. Dictionaries are extremely "
            "useful when you need to look up a value quickly using a unique key, instead "
            "of searching through a list by position.",

            "A set is an unordered collection of unique items -- duplicates are "
            "automatically removed. Sets are useful for membership tests (checking if an "
            "item exists) and for operations like union, intersection, and difference "
            "between two collections.",

            "Choosing the right data structure matters for performance: looking up a value "
            "in a dictionary or set is typically much faster than searching through a "
            "list, especially as the amount of data grows.",
        ],
    },
    "oop_basics.pdf": {
        "title": "Object-Oriented Programming Basics",
        "paragraphs": [
            "Object-Oriented Programming, or OOP, organizes code around 'objects', which "
            "bundle together data (attributes) and behavior (methods). In Python, you "
            "define a blueprint for an object using the class keyword, and then create "
            "individual objects, called instances, from that class.",

            "A class typically has an __init__ method, called the constructor, which runs "
            "automatically when a new object is created and sets up its initial "
            "attributes. For example: class Dog: def __init__(self, name): self.name = name.",

            "Encapsulation means keeping an object's internal data and logic bundled "
            "together and controlling how outside code interacts with it. Inheritance "
            "lets one class (a child class) reuse and extend the behavior of another "
            "class (a parent class), which helps avoid duplicated code.",

            "Polymorphism allows different classes to define methods with the same name "
            "but different behavior, so the same piece of calling code can work with "
            "objects of different types, as long as they share the expected method names.",
        ],
    },
}


def build_pdf(path: str, title: str, paragraphs: list[str]) -> None:
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path, pagesize=LETTER, topMargin=1 * inch, bottomMargin=1 * inch)
    story = [Paragraph(title, styles["Title"]), Spacer(1, 0.3 * inch)]
    for para in paragraphs:
        story.append(Paragraph(para, styles["BodyText"]))
        story.append(Spacer(1, 0.2 * inch))
    doc.build(story)


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename, content in DOCUMENTS.items():
        path = os.path.join(OUTPUT_DIR, filename)
        build_pdf(path, content["title"], content["paragraphs"])
        print(f"Created {path}")


if __name__ == "__main__":
    main()
