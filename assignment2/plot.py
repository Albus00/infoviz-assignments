import tkinter as tk
import csv

# Create a Tkinter window
window = tk.Tk()
window.title("Scatter Plot Visualization")

# Create a canvas to draw the plot
canvas = tk.Canvas(window, width=700, height=700)
canvas.pack()

# Calculate the minimum and maximum values for x and y axes
min_x = float('50')
max_x = float('650')
min_y = float('50')
max_y = float('650')

# Draw the x-axis
canvas.create_line(50, 350, 650, 350)  # x-axis line
# Draw the ticks and tick values for x-axis
# ...

# Draw the y-axis
canvas.create_line(350, 50, 350, 650)  # y-axis line

# Draw the ticks and tick values for y-axis
# ...

# Load and process the data using csvreader
with open('data1.csv', 'r') as file:
  # Create a CSV reader object
  csvreader = csv.reader(file)

  # Read the header row
  header = next(csvreader)

  # Process each row of data
  for line in csvreader:
    # Access the data in each column
    xSet = float(line[0])
    ySet = float(line[1])
    letterSet = line[2]
    print(xSet, ySet, letterSet)
    x = 50 + (xSet - min_x) * (600 / (max_x - min_x))
    y = 650 - (ySet - min_y) * (600 / (max_y - min_y))
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")


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
