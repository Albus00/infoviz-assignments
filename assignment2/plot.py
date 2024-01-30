import tkinter as tk
import csv

# Create a Tkinter window
window = tk.Tk()
window.title("Scatter Plot Visualization")

# Create a canvas to draw the plot
canvas = tk.Canvas(window, width=700, height=700)
canvas.pack()


# Load and process the data using csvreader
with open('data1.csv', 'r') as file:
  # Create a CSV reader object
  csvreader = csv.reader(file)

  # Read the header row
  header = next(csvreader)

  # Load and process the data using csvreader
  data = []  # List to store the data

  # Initiate the minimum and maximum values for x and y axes
  min_x = float('inf')
  max_x = float('-inf')
  min_y = float('inf')
  max_y = float('-inf')

  for line in csvreader:
    x = float(line[0])
    y = float(line[1])
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    data.append((x, y, line[2]))
  print(min_x, max_x, min_y, max_y)

    # Update maximum x and y values if needed
  for entry in data:
    x = ((entry[0] + max_x) / (2*max_x)) * 650
    y = ((entry[1] + max_y) / (2*max_y)) * 650
    letterSet = entry[2]
    style_mapping = {'a': 'pink', 'b': 'blue', 'c': 'red'}
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=style_mapping.get(letterSet, 'blue'))


canvas.create_line(50, 350, 650, 350)  # x-axis line
canvas.create_line(350, 50, 350, 650)  # y-axis line

# draw x axis and create text through iteration
# draw x axis and create text through iteration
for i in range(1, 9):
    x_tick_position = (i / 8) * 650
    canvas.create_line(x_tick_position, 350, x_tick_position, 345, width=2)
    canvas.create_text(x_tick_position, 360, text=f'{min_x-i*((min_x-max_x)/ 8):.1f}', font=("Purisa", 10))

# draw y axis and create text through iteration
for i in range(1, 9):
    y_tick_position = 700 - (i / 8) * 650
    canvas.create_line(350, y_tick_position, 345, y_tick_position, width=2)
    canvas.create_text(360, y_tick_position, text=f'{i * max_y / 8:.1f}', font=("Purisa", 10))

  # i = 0;
  # while i < len(xSet):
  #   print(xSet[i], ySet[i], letterSet[i])
  #   i += 1

  #   # Draw the data points based on column 1 and column 2
  #   # Calculate the x and y coordinates for the data point
  #   x = 50 + (column1 - min_x) * (600 / (max_x - min_x))
  #   y = 650 - (column2 - min_y) * (600 / (max_y - min_y))
  #    # Draw the data point
  #   canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")
  #  # ...


# Draw the legend

# Start the Tkinter event loop
window.mainloop()
