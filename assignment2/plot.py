import tkinter as tk
import csv
import math


data = [] # Create an empty list to store the data
min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')

offset_x, offset_y = 0, 0

# Create a Tkinter window
window = tk.Tk()
window.title("Scatter Plot Visualization")

# Create a canvas to draw the plot
canvas = tk.Canvas(window, width=700, height=700)
canvas.pack()

def load_data():
    with open('data1.csv', 'r') as file:
        # Create a CSV reader object
        csvreader = csv.reader(file)

        # Load and process the data using csvreader
        entryIndex = 0;
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

            data.append((x, y, line[2], entryIndex, 0))     # Append the data to the list
            entryIndex += 1                                 # Add index to the data

            # Render the points on the canvas
            render_points(data)
    return data

# Define a function to render the points on the canvas
def render_points(data):
    canvas.delete("all") # Clear the canvas

    for i, entry in enumerate(data):
        x = ((entry[0] + max_x) / (2*max_x)) * 600 + 50
        y = ((-entry[1] + max_y) / (2*max_y)) * 600 + 50

        # Render the points based on the entry type and focus
        if entry[4] == 0: # The point is not selected, render it in normal size and color
            entry_type = entry[2]    # Get the letter of the entry
            match entry_type:
                case 'a':
                    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='pink')
                case 'b':
                    canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3, fill='blue')
                case 'c':
                    canvas.create_polygon(x, y - 4, x - 4, y, x, y + 4, x + 4, y, fill='red')
                case 'foo':
                    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='pink')
                case 'bar':
                    canvas.create_rectangle(x - 3, y - 3, x + 3, y + 3, fill='blue')
                case 'baz':
                    canvas.create_polygon(x, y - 4, x - 4, y, x, y + 4, x + 4, y, fill='red')

                    
        elif entry[4] == 1: # The point is selected, render it in a larger size and color
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='green')
            data[i] = (entry[0], entry[1], entry[2], entry[3], 0) # Set the point to not selected

        elif entry[4] == 2: # The point is near, render it in a larger size and color
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='yellow')
            data[i] = (entry[0], entry[1], entry[2], entry[3], 0) # Set the point to not selected
            

    # Draw the x and y axes
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

    create_legend(canvas)

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

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def right_click(event):
    global data
    x, y = event.x, event.y

    # Reverse the scaling done when rendering the points
    x  = ((x - 50) * 2 * max_x) / 600 - max_x;
    y  = ((y - 50) * 2 * max_y) / 600 - max_y;
    y = -y; # Invert y axis because it has to apparently?

    p = get_point(x, y)     # Get the point around the mouse click
    print("Clicked:", p);

    # Calculate distances to all points
    distances = [(calculate_distance(p, point), point) for point in data]


    # Find the five nearest points (set the point itself, which has a distance of 0, to "selected") and change their render properties
    for near_point in sorted(distances)[0:6]:
        for i, point in enumerate(data):
            if point == near_point[1]:
                if near_point[0] == 0:
                    data[i] = (point[0], point[1], point[2], point[3], 1) # Set the point to selected
                else:
                    print("Near:", point);
                    data[i] = (point[0], point[1], point[2], point[3], 2) # Set the point to near    

    render_points(data) # Render the points again  

# Create a function to offset the focus of the plot to a specific point
def offset_point(point, offset_x, offset_y):
    return (point[0] - offset_x, point[1] - offset_y, point[2], point[3], 0) 


def left_click(event):
    x, y = event.x, event.y

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
        data[i] = offset_point(point, -offset_x, -offset_y)
    
    offset_x, offset_y = 0, 0
         
    
    print("Clicked:", p);

    offset_x, offset_y = p[0], p[1]

    # Offset the focus so that the point is rendered in origo
    for i, point in enumerate(data):
        data[i] = offset_point(point, offset_x, offset_y)
        if point == p:
            data[i] = (data[i][0], data[i][1], data[i][2], data[i][3], 1) # Set the point to selected

    render_points(data) # Render the points again

    
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
render_points(data)

# Bind click events to the canvas
canvas.bind("<Button-3>", right_click)
canvas.bind("<Button-1>", left_click)

# Start the Tkinter event loop
window.mainloop()
