import tkinter as tk
import csv
import math

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
style_mapping = {'a': 'pink', 'b': 'blue', 'c': 'red','foo': 'green', 'bar': 'yellow', 'baz': 'orange'}
for entry in data:
  x = ((entry[0] + max_x) / (2*max_x)) * 600 + 50
  y = ((-entry[1] + max_y) / (2*max_y)) * 600 + 50

  letterSet = entry[2]
  
  if letterSet == 'a':
     canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=style_mapping.get(letterSet, 'blue'))
  elif letterSet == 'b':
     canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3, fill=style_mapping.get(letterSet, 'blue'))
  elif letterSet == 'c':
     canvas.create_line(x - 3, y - 3, x + 3, y + 3, fill=style_mapping.get(letterSet, 'blue'))

canvas.create_line(50, 350, 650, 350)  # x-axis line #startposx,startposy,endposx,endposy
canvas.create_line(350, 50, 350, 650)  # y-axis line

# draw x axis and create text through iteration
for i in range(0, 11):
    x_tick_position = 650 - i*60
    canvas.create_line(x_tick_position, 350, x_tick_position, 345, width=2)
    canvas.create_text(x_tick_position, 360, text=f'{max_x-i*((max_x-min_x)/ 10):.1f}', font=("Purisa", 10))

# draw y axis and create text through iteration
for i in range(0, 11):
    y_tick_position = 650 - i*60
    canvas.create_line(350, y_tick_position, 345, y_tick_position, width=2)
    canvas.create_text(370, y_tick_position, text=f'{min_y-i*((min_y-max_y)/10):.1f}', font=("Purisa", 10))

# Draw the legend
def create_legend(canvas):
    # Define your data types and corresponding colors
    data_types = ['a', 'b', 'c']
    colors = ['pink', 'blue', 'red']

    # Set the starting coordinates for the legend
    x_start, y_start = 50, 50


    # Iterate through data types to create legend items
    for i, data_type in enumerate(data_types):
        # Draw colored rectangle
        canvas.create_rectangle(x_start, y_start + i * 30, x_start + 20, y_start + i * 30 + 20, fill=colors[i])

        # Display data type label next to the rectangle
        canvas.create_text(x_start + 30, y_start + i * 30 + 10, text=data_type, anchor=tk.W)
create_legend(canvas)



def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def right_click(event):
    x, y = event.x, event.y

    # Reverse the scaling done when rendering the points
    x  = ((x - 50) * 2 * max_x) / 600 - max_x;
    y  = ((y - 50) * 2 * max_y) / 600 - max_y;
    y = -y; # Invert y axis because it has to apparently?

    print(get_point(x, y));

    # Calculate distances to all points
    distances = [(calculate_distance((x, y), (point[0], point[1])), point) for point in data]

    # Sort distances and find the five nearest points
    nearest_points = sorted(distances)[:5]

    # Change the color of the five nearest points
    for _, point in nearest_points:
        canvas.create_rectangle(point[0] - 3, point[1] - 3, point[0] + 3,point[1] + 3, fill=style_mapping.get(letterSet, 'orange'))

canvas.bind("<Button-3>", right_click)

# create a function that checks through the data and finds if there is a point around the mouse click
def get_point(x, y):
    MARGIN = 1;
    for point in data:
        print(point, x, y)
        if point[0] > x - MARGIN and point[0] < x + MARGIN and point[1] > y - MARGIN and point[1] < y + MARGIN:
            return point
    return False


# Start the Tkinter event loop
window.mainloop()
