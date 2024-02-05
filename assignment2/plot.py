import tkinter as tk
import csv
import math


data = [] # Create an empty list to store the data
min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')

offset_x, offset_y = 0, 0
selectedPoint = -1          # The index of the selected point
default_data_types = [''] # Define your data types

# Create a Tkinter window
window = tk.Tk()
window.title("Scatter Plot Visualization")

# Create a canvas to draw the plot
canvas = tk.Canvas(window, width=700, height=700)
canvas.pack()

def load_data():
    filename = 'data2.csv'

    global default_data_types
    # Set the data types based on the file
    if filename == 'data1.csv':
        default_data_types = ['A', 'B', 'C']
    elif filename == 'data2.csv':
        default_data_types = ['foo', 'bar', 'baz']

    with open(filename, 'r') as file:
        # Create a CSV reader object
        csvreader = csv.reader(file)

        # Load and process the data using csvreader
        entry_index = 0;
        global min_x, max_x, min_y, max_y
        for line in csvreader:
            # Extract the x and y coordinates from the dataset
            x = float(line[0])
            y = float(line[1])
            # Update the minimum and maximum values for x and y axes
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            min_x = min(min_x, x)
            min_y = min(min_y, y)

            data.append((x, y, line[2], entry_index, 0))     # Append the data to the list
            entry_index += 1                                 # Add index to the data

            # Render the points on the canvas
            render_visualization(data)
    return data

# Define a function to render the visualization on the canvas
def render_visualization(data):
    canvas.delete("all") # Clear the canvas

    for i, entry in enumerate(data):
        x = ((entry[0] + max_x) / (2*max_x)) * 600 + 50
        y = ((-entry[1] + max_y) / (2*max_y)) * 600 + 50

        color = ''
        # Check if offset is used
        if offset_x != 0 or offset_y != 0:
           color = check_quadrant(entry)

        # Render the points based on the entry type and focus
        if entry[4] == 0: # The point is not selected, render it in normal size and color
            render_normal_point(entry[2], x, y, color)
                    
        elif entry[4] == 1: # The point is selected, render it in a larger size and color
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='green')
            data[i] = (entry[0], entry[1], entry[2], entry[3], 0) # Set the point to not selected

        elif entry[4] == 2: # The point is near, render it in a larger size and color
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill='gray')
            data[i] = (entry[0], entry[1], entry[2], entry[3], 0) # Set the point to not selected
            
    # Draw the axes and the legend
    draw_axes(canvas)
    create_legend(canvas)

def check_quadrant(entry):
     # Set the color of the point based on which quadrant it is in
    if entry[0] > 0 and entry[1] > 0:
        color = 'brown'     # Quadrant 1 (Q1)
    elif entry[0] < 0 and entry[1] > 0:
        color = 'orange'    # Quadrant 2 (Q2)
    elif entry[0] < 0 and entry[1] < 0:
        color = 'purple'    # Quadrant 3 (Q3)
    elif entry[0] > 0 and entry[1] < 0:
        color = 'yellow'    # Quadrant 4 (Q4)
    else:
        color = 'black'  # If the point is on the axis, set the color to black

    return color

def render_normal_point(entry_type, x, y, color):
    match entry_type:
                # If color is not defined, set it to default for every case
        case 'a':
            if color=='': color='pink'
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline='black')
        case 'b':
            if color=='': color='blue'
            canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3, fill=color, outline='black')
        case 'c':
            if color=='': color='red'
            canvas.create_polygon(x, y - 4, x - 4, y, x, y + 4, x + 4, y, fill=color, outline='black')
        case 'foo':
            if color=='': color='pink'
            canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill=color, outline='black')
        case 'bar':
            if color=='': color='blue'
            canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3, fill=color, outline='black')
        case 'baz':
            if color=='': color='red'
            canvas.create_polygon(x, y - 4, x - 4, y, x, y + 4, x + 4, y, fill=color, outline='black')

# Create a function to draw the x and y axes
def draw_axes(canvas):
    # Draw the x and y axes
    canvas.create_line(50, 350, 650, 350)  # x-axis line
    canvas.create_line(350, 50, 350, 650)  # y-axis line

    # Draw x-axis ticks and labels
    for i in range(0, 11):
        x_tick_position = 650 - i * 60
        canvas.create_line(x_tick_position, 350, x_tick_position, 345, width=2)
        canvas.create_text(x_tick_position, 360, text=f'{max_x - i * ((max_x - min_x) / 10):.1f}', font=("Purisa", 10))

    # Draw y-axis ticks and labels
    for i in range(0, 11):
        y_tick_position = 650 - i * 60
        canvas.create_line(350, y_tick_position, 345, y_tick_position, width=2)
        canvas.create_text(370, y_tick_position, text=f'{min_y - i * ((min_y - max_y) / 10):.1f}', font=("Purisa", 10))

# Draw the legend
def create_legend(canvas):
    # Check if offset is used
    if offset_x == 0 or offset_y == 0:
        # Define your data types and corresponding colors for the default case
        data_types = default_data_types
        colors = ['pink', 'blue', 'red']
        # Add the selected and near data types to the legend
        if selectedPoint != -1:
            data_types.extend(['Selected', 'Near'])
            colors.extend(['green', 'gray'])
    else:
        # Define your data types and corresponding colors for the offset case
        data_types = ['Q1', 'Q2', 'Q3', 'Q4', 'Selected']
        colors = ['orange', 'brown', 'purple', 'yellow', 'green']
        # Add the near data types to the legend
        if selectedPoint != -1:
            data_types.append('Near')
            colors.append('gray')


    # Set the starting coordinates for the legend
    x_start, y_start = 50, 50

    # Iterate through data types to create legend items
    for i, data_type in enumerate(data_types):
        # Draw colored rectangle
        canvas.create_rectangle(x_start, y_start + i * 30, x_start + 20, y_start + i * 30 + 20, fill=colors[i])

        # Display data type label next to the rectangle
        canvas.create_text(x_start + 30, y_start + i * 30 + 10, text=data_type, anchor=tk.W)


def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def right_click(event):
    global data, selectedPoint
    x, y = event.x, event.y

    # Reverse the scaling done when rendering the points
    x  = ((x - 50) * 2 * max_x) / 600 - max_x;
    y  = ((y - 50) * 2 * max_y) / 600 - max_y;
    y = -y; # Invert y axis because it has to apparently?

    p = get_point(x, y)     # Get the point around the mouse click
    print("Clicked:", p);

    # Check if clicked point is already selected
    if p[3] == selectedPoint:
        selectedPoint = -1
        render_visualization(data)
        return

    # Calculate distances to all points
    distances = [(calculate_distance(p, point), point) for point in data]

    # Find the five nearest points (set the point itself, which has a distance of 0, to "selected") and change their render properties
    for near_point in sorted(distances)[0:6]:
        for i, point in enumerate(data):
            if point == near_point[1]:
                if near_point[0] == 0:
                    data[i] = (point[0], point[1], point[2], point[3], 1) # Set the point to selected
                    selectedPoint = point[3]
                else:
                    print("Near:", point);
                    data[i] = (point[0], point[1], point[2], point[3], 2) # Set the point to near   

    render_visualization(data) # Render the points again  

# Create a function to offset the focus of the plot to a specific point
def offset_point(point, sent_x, sent_y):
    return (point[0] - sent_x, point[1] - sent_y, point[2], point[3], 0) 


def left_click(event):
    x, y = event.x, event.y

    # Reset the selected point
    global selectedPoint
    selectedPoint = -1

    # Reverse the scaling done when rendering the points
    x  = ((x - 50) * 2 * max_x) / 600 - max_x;
    y  = ((y - 50) * 2 * max_y) / 600 - max_y;
    y = -y; # Invert y axis because it has to apparently?

    # Get the point around the mouse click, if it exists
    if (p := get_point(x, y)) == False:
        return  # If no point is found, return
    
    global offset_x, offset_y

    # Reset the offset
    for i, point in enumerate(data):
        print("STARTING offset:", point, offset_x, offset_y);
        data[i] = offset_point(point, -offset_x, -offset_y)

    print("Clicked:", p);
    # If the point is the origo, reset the offset and render the points
    if abs(p[0]) < 1e-6 and abs(p[1]) < 1e-6:   # If the point is the origo (float-proof)
        offset_x, offset_y = 0, 0
        render_visualization(data)
        return

    # Add the offset to the existing offset. This is done to keep the offset consistent to the starting position
    offset_x += p[0] 
    offset_y += p[1]

    # Offset the focus so that the point is rendered in origo
    for i, point in enumerate(data):
        print("Offset:", point, offset_x, offset_y);
        data[i] = offset_point(point, offset_x, offset_y)
        if point[3] == p[3]:
            data[i] = (data[i][0], data[i][1], data[i][2], data[i][3], 1) # Set the point to selected
        print("Result:", data[i]);
            

    render_visualization(data) # Render the points again

    
# create a function that checks through the data and finds if there is a point around the mouse click
def get_point(x, y):
    MARGIN = 1;
    for point in data:
        if point[0] > x - MARGIN and point[0] < x + MARGIN and point[1] > y - MARGIN and point[1] < y + MARGIN:
            return point # Return the point if it is found
    return False


# Load the data
data = load_data()

# Render the points on the canvas
render_visualization(data)

# Bind click events to the canvas
canvas.bind("<Button-3>", right_click)
canvas.bind("<Button-1>", left_click)

# Start the Tkinter event loop
window.mainloop()
