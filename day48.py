import tkinter as tk
from tkhtmlview import HTMLLabel

# Create the main window
root = tk.Tk()
root.title("Python Learning Hub")
root.geometry("800x700")

# Define enhanced HTML content
html_content = """
<h1 style='text-align: center; color: #306998;'>Python Learning Hub</h1>
<p>Welcome to the Python Learning Hub! Here, you’ll find an overview of essential Python topics, project ideas, a learning roadmap, and resources to enhance your Python skills.</p>

<!-- Python Roadmap Section -->
<h2>Python Learning Roadmap</h2>
<p>Follow this roadmap to master Python:</p>
<ol>
    <li><strong>Basics:</strong> Data Types, Variables, Control Flow</li>
    <li><strong>Intermediate:</strong> Functions, Modules, File Handling, Error Handling</li>
    <li><strong>Object-Oriented Programming (OOP):</strong> Classes, Objects, Inheritance, Polymorphism</li>
    <li><strong>Data Structures and Algorithms:</strong> Lists, Stacks, Queues, Linked Lists, Trees, Graphs</li>
    <li><strong>Libraries for Development:</strong> Web (Flask, Django), Data Science (Pandas, NumPy), Visualization (Matplotlib)</li>
    <li><strong>Advanced Topics:</strong> Multithreading, Networking, Machine Learning with Scikit-Learn</li>
</ol>

<!-- Project Ideas Section -->
<h2>Python Project Ideas</h2>
<p>Here are some project ideas to help you apply what you've learned:</p>
<ul>
    <li><strong>Beginner:</strong> To-do list app, Calculator, Quiz Game</li>
    <li><strong>Intermediate:</strong> Web Scraper, Personal Budget Manager, Blog Website with Flask</li>
    <li><strong>Advanced:</strong> Machine Learning model for predicting stock prices, Chat Application with Socket Programming</li>
</ul>

<!-- Popular Python Libraries Section -->
<h2>Popular Python Libraries</h2>
<p>Some essential libraries that make Python a versatile and powerful language:</p>
<table border="1" style="width: 100%; border-collapse: collapse;">
   <tr style="background-color: #f2f2f2;">
      <th>Library</th>
      <th>Description</th>
   </tr>
   <tr>
      <td><strong>NumPy</strong></td>
      <td>Provides support for large multidimensional arrays and matrices, along with a collection of mathematical functions.</td>
   </tr>
   <tr>
      <td><strong>Pandas</strong></td>
      <td>Offers data manipulation and analysis tools for structured data operations.</td>
   </tr>
   <tr>
      <td><strong>Matplotlib</strong></td>
      <td>A plotting library for creating static, animated, and interactive visualizations.</td>
   </tr>
   <tr>
      <td><strong>Scikit-Learn</strong></td>
      <td>Provides simple and efficient tools for data mining and machine learning.</td>
   </tr>
   <tr>
      <td><strong>Flask</strong></td>
      <td>A lightweight WSGI web application framework for small to medium-sized applications.</td>
   </tr>
   <tr>
      <td><strong>Django</strong></td>
      <td>A high-level Python web framework that encourages rapid development and clean, pragmatic design.</td>
   </tr>
</table>

<!-- Quiz Section -->
<h2>Interactive Quiz</h2>
<p>Test your Python knowledge with this simple quiz:</p>
<ol>
    <li>What is the output of <code>print(2 ** 3)</code>?</li>
    <li>Which library is used for data manipulation in Python?</li>
    <li>How do you create a virtual environment in Python?</li>
</ol>

<p><em>Answer Key:</em> 1) 8, 2) Pandas, 3) <code>python -m venv myenv</code></p>

<!-- Resources Section -->
<h2>Additional Resources</h2>
<p>Explore more on Python by visiting these links:</p>
<ul>
    <li><a href='https://docs.python.org/3/' target='_blank'>Python Official Documentation</a></li>
    <li><a href='https://www.learnpython.org/' target='_blank'>Learn Python - Free Interactive Python Tutorial</a></li>
    <li><a href='https://realpython.com/' target='_blank'>Real Python - Python Tutorials</a></li>
    <li><a href='https://www.codecademy.com/learn/learn-python-3' target='_blank'>Codecademy - Learn Python</a></li>
</ul>

<p style='text-align: center; color: #555;'>Happy Learning and Coding!</p>
"""

# Display the HTML content in a tkhtmlview HTMLLabel
html_label = HTMLLabel(root, html=html_content)
html_label.pack(fill="both", expand=True, padx=10, pady=10)

# Run the application
root.mainloop()