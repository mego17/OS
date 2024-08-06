from FCFS_Algorithm import FCFS_Algorithm
from SSTF_Algorithm import SSTF_Algorithm
from SCAN_Algorithm import SCAN_Algorithm
from LOOK_Algorithm import LOOK_Algorithm
from CSCAN_Algorithm import CSCAN_Algorithm
from CLOOK_Algorithm import CLOOK_Algorithm
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# GUI class for application
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Disk Scheduling Algorithms")
        self.geometry("500x500")
        
        self.configure(bg="black")  # Set background color
        
      
        
        # Labels for entries
        tk.Label(self, text="Enter requests (separated by spaces)  >>>", bg="yellow").place(x=50, y=50)
        self.requests_entry = tk.Entry(self)
        self.requests_entry.place(x=285, y=50)

        tk.Label(self, text="Enter head position  >>>", bg="yellow").place(x=50, y=100)
        self.head_position_entry = tk.Entry(self)
        self.head_position_entry.place(x=200, y=100)

        # Radio buttons for algorithm selection
        tk.Label(self, text="<<< Select Algorithm >>>", bg="yellow").place(x=160, y=150)
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("FCFS")
        tk.Radiobutton(self, text="FCFS", variable=self.algorithm_var, value="FCFS", fg="black",
                       command=self.on_algorithm_change).place(x=40, y=200)
        tk.Radiobutton(self, text="SSTF", variable=self.algorithm_var, value="SSTF", fg="green",
                       command=self.on_algorithm_change).place(x=110, y=200)
        tk.Radiobutton(self, text="SCAN", variable=self.algorithm_var, value="SCAN", fg="blue",
                       command=self.on_algorithm_change).place(x=180, y=200)
        tk.Radiobutton(self, text="LOOK", variable=self.algorithm_var, value="LOOK", fg="orange",
                       command=self.on_algorithm_change).place(x=250, y=200)
        tk.Radiobutton(self, text="C-SCAN", variable=self.algorithm_var, value="CSCAN", fg="brown",
                       command=self.on_algorithm_change).place(x=320, y=200)
        tk.Radiobutton(self, text="C-LOOK", variable=self.algorithm_var, value="CLOOK", fg="red",
                       command=self.on_algorithm_change).place(x=400, y=200)

        # Button to run the selected algorithm
        tk.Button(self, text="Run", command=self.run_algorithm, bg="red", fg="white", width=10).place(x=210, y=250)

        self.total_tracks_label = tk.Label(self, text="<< Enter total number of tracks >>", bg="yellow")
        self.total_tracks_entry = tk.Entry(self)
        self.direction_label = tk.Label(self, text="<<< Select direction >>>", bg="yellow")
        self.direction_var = tk.StringVar()
        self.direction_var.set("Right")
        self.direction_left = tk.Radiobutton(self, text="Left (Toward Outer)", variable=self.direction_var, value="Left")
        self.direction_right = tk.Radiobutton(self, text="Right (Toward Inner)", variable=self.direction_var, value="Right")

        # Create a frame to hold the result label and apply a border
        self.result_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        self.result_frame.place(x=50, y=400, width=400, height=80)
        self.result_label = tk.Label(self.result_frame, text="The Results Will Be Display Here", wraplength=500)
        self.result_label.pack(fill=tk.BOTH, expand=1)

    def on_algorithm_change(self):
        algorithm = self.algorithm_var.get()
        if algorithm in ("FCFS", "SSTF"):
            self.total_tracks_label.place_forget()
            self.total_tracks_entry.place_forget()
            self.direction_label.place_forget()
            self.direction_left.place_forget()
            self.direction_right.place_forget()
        else:
            self.total_tracks_label.place(x=10, y=300)
            self.total_tracks_entry.place(x=50, y=335)
            self.direction_label.place(x=300, y=300)
            self.direction_left.place(x=302, y=330)
            self.direction_right.place(x=302, y=360)

    # Function to run the selected algorithm
    def run_algorithm(self):
        algorithm = self.algorithm_var.get()
        algorithm_name = ""  # Initialize algorithm name

        if algorithm == "FCFS":
            algorithm_class = FCFS_Algorithm
            algorithm_name = "First Come First Serve"
        elif algorithm == "SSTF":
            algorithm_class = SSTF_Algorithm
            algorithm_name = "Shortest Seek Time First"
        elif algorithm == "SCAN":
            algorithm_class = SCAN_Algorithm
            algorithm_name = "SCAN"
        elif algorithm == "LOOK":
            algorithm_class = LOOK_Algorithm
            algorithm_name = "LOOK"
        elif algorithm == "CSCAN":
            algorithm_class = CSCAN_Algorithm
            algorithm_name = "Circular SCAN"
        elif algorithm == "CLOOK":
            algorithm_class = CLOOK_Algorithm
            algorithm_name = "Circular LOOK"

        requests = list(map(int, self.requests_entry.get().split()))
        head_position = int(self.head_position_entry.get())

        if algorithm == "FCFS" or algorithm == "SSTF":
            algorithm = algorithm_class(requests, head_position)
            order, seek_time = algorithm.algorithm()
            # Display result
            self.result_label.config(text=f"Order of requests: {order}\nTotal seek time: {seek_time}")
            # Draw request graph
            self.draw_request_graph1(algorithm_name, requests, order,
                                     head_position)  # 0 for total_tracks for FCFS and SSTF
        else:
            total_tracks = int(self.total_tracks_entry.get())
            direction = self.direction_var.get()
            algorithm = algorithm_class(requests, head_position, direction, total_tracks)
            order, seek_time = algorithm.algorithm()
            # Display result
            self.result_label.config(text=f"Order of requests: {order}\nTotal seek time: {seek_time}")
            # Draw request graph
            self.draw_request_graph(algorithm_name, requests, order, head_position, total_tracks)

    def draw_request_graph1(self, algorithm_name, requests, order, head_position):
        fig, ax = plt.subplots()
        ax.plot([head_position] + order, range(len(order) + 1), 'ro-')  # Plot the order of requests
        ax.set_yticks(range(len(order) + 1))
        ax.set_yticklabels([f'Head = {head_position}'] + list(map(str, order)))  # Set y-axis labels to request values
        if head_position >= max(order) :
            ax.set_xlim(0, head_position)  # Limit x-axis from 0 to head
        else:
            ax.set_xlim(0, max(order))  # Limit x-axis from 0 to largest request
        ax.set_ylim(-1, len(order) + 1)  # Limit y-axis from -1 to number of requests
        ax.set_xlabel('Track Number')
        ax.set_ylabel('Request Order')
        ax.set_title(f'Disk Request Order - {algorithm_name}')  # Include algorithm name in the title
        ax.grid(True)

        # Embed the plot in tkinter window
        self.embed_graph_in_tk(fig)

    # Function to draw request graph
    def draw_request_graph(self, algorithm_name, requests, order, head_position, total_tracks):
        fig, ax = plt.subplots()
        ax.plot([head_position] + order, range(len(order) + 1), 'ro-')  # Plot the order of requests
        ax.set_yticks(range(len(order) + 1))
        ax.set_yticklabels([f'Head = {head_position}'] + list(map(str, order)))  # Set y-axis labels to request values
        ax.set_xlim(0, total_tracks - 1)  # Limit x-axis from 0 to total_tracks - 1
        ax.set_ylim(-1, len(order) + 1)  # Limit y-axis from -1 to number of requests
        ax.set_xlabel('Track Number')
        ax.set_ylabel('Request Order')
        ax.set_title(f'Disk Request Order - {algorithm_name}')  # Include algorithm name in the title
        ax.grid(True)

        # Embed the plot in tkinter window
        self.embed_graph_in_tk(fig)

    # Function to embed graph in tkinter window
    def embed_graph_in_tk(self, fig):
        # Create a new window to embed the plot
        graph_window = tk.Toplevel(self)
        graph_window.title("Disk Request Order Graph")
        graph_window.geometry("900x900")

        # Create a canvas to draw the plot
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add a toolbar for the plot
        toolbar = ttk.Toolbar(graph_window, orient='horizontal')
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.update()

