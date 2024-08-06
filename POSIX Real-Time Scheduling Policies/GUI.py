from tkinter import *
from tkinter import messagebox
from tkintertable import TableCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from FCFO import TaskScheduler as FCFO_T
from FCFO import Scheduler as FCFO_S
from RR import TaskScheduler as RR_T
from RR import Scheduler as RR_S
from MLF import TaskScheduler as MLF_T
from MLF import Scheduler as MLF_S
from EDF import TaskScheduler as EDF_T
from EDF import Scheduler as EDF_S
from DMA import TaskScheduler as DMA_T
from DMA import Scheduler as DMA_S
from RMA import TaskScheduler as RMA_T
from RMA import Scheduler as RMA_S

class Application:
    def __init__(self):
        self.root = Tk()
        self.root.title("POSIX Real-Time Scheduling Policies")
        self.root.geometry("630x600+400+100")

        self.input_frame = Frame(self.root)
        self.input_frame.pack(side=LEFT, fill=Y)

        self.rt_entries = []
        self.pt_entries = []
        self.et_entries = []
        self.dt_entries = []
        self.tasks = []

        Label(self.input_frame, text="No.Tasks ").grid(row=1, column=1, pady=5)
        Label(self.input_frame, text="Scheduling type ").grid(row=3,column=1,pady=5)

        self.use_algorithm = 0

        def hide_indicate():
            FCFO_indicate.config(bg='#C0ffC0') 
            RR_indicate.config(bg='#C0ffC0')  
            MLF_indicate.config(bg='#C0ffC0')  
            EDF_indicate.config(bg='#C0ffC0')  
            DMA_indicate.config(bg='#C0ffC0')  
            RMA_indicate.config(bg='#C0ffC0')  

        def indicate(label, page):
            hide_indicate()
            label.config(bg='#158AFF')  
            page()

        Button(self.input_frame, text="FCFO", fg='#158AFF',bd=0,bg='#C0C0C0',command=lambda:indicate(FCFO_indicate, self.FCFO)).place(x=10, y=120 ,width=90, height=30)
        FCFO_indicate = Label(self.input_frame,text='',bg='#C0C0C0')
        FCFO_indicate.place(x=3, y=120, width=7, height=30)

        Button(self.input_frame, text="RR", fg='#158AFF',bd=0,bg='#C0C0C0',command=lambda:indicate(RR_indicate, self.RR)).place(x=10, y=170 ,width=90, height=30)
        RR_indicate = Label(self.input_frame,text='',bg='#C0C0C0')
        RR_indicate.place(x=3, y=170, width=7, height=30)

        Button(self.input_frame, text="MLF", fg='#158AFF',bd=0,bg='#C0C0C0',command=lambda:indicate(MLF_indicate, self.MLF)).place(x=10, y=220 ,width=90, height=30)
        MLF_indicate = Label(self.input_frame,text='',bg='#C0C0C0')
        MLF_indicate.place(x=3, y=220, width=7, height=30)

        Button(self.input_frame, text="EDF", fg='#158AFF',bd=0,bg='#C0C0C0',command=lambda:indicate(EDF_indicate, self.EDF)).place(x=10, y=270 ,width=90, height=30)
        EDF_indicate = Label(self.input_frame,text='',bg='#C0C0C0')
        EDF_indicate.place(x=3, y=270, width=7, height=30)

        Button(self.input_frame, text="DMA", fg='#158AFF',bd=0,bg='#C0C0C0',command=lambda:indicate(DMA_indicate, self.DMA)).place(x=10, y=320 ,width=90, height=30)
        DMA_indicate = Label(self.input_frame,text='',bg='#C0C0C0')
        DMA_indicate.place(x=3, y=320, width=7, height=30)

        Button(self.input_frame, text="RMA", fg='#158AFF',bd=0,bg='#C0C0C0',command=lambda:indicate(RMA_indicate, self.RMA)).place(x=10, y=370 ,width=90, height=30)
        RMA_indicate = Label(self.input_frame,text='',bg='#C0C0C0')
        RMA_indicate.place(x=3, y=370, width=7, height=30)

        self.no_tasks = IntVar()
        self.no_tasks.set(0)
        self.no_tasks.trace("w", self.refresh)
        option_menu = OptionMenu(self.input_frame, self.no_tasks, *[0, 1, 2, 3, 4, 5])
        option_menu.grid(row=2, column=1, pady=10)
        option_menu.config(fg='#158AFF',bd=0,bg='#C0C0C0')

        self.tasks_frame()

        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.mainloop()

    def exit(self):
        self.root.quit()
        self.root.destroy()

    def FCFO(self):
        self.algorithm_used.config(text="Algorithm: First Come First Out")
        self.use_algorithm = 1
        
    def RR(self):
        self.algorithm_used.config(text="Algorithm: Round-Robin")
        self.use_algorithm = 2

    def MLF(self):
        self.algorithm_used.config(text="Algorithm: Minimum Laxity First")
        self.use_algorithm = 3

    def EDF(self):
        self.algorithm_used.config(text="Algorithm: Earliest Deadline First")
        self.use_algorithm = 4

    def DMA(self):
        self.algorithm_used.config(text="Algorithm: Deadline Monotonic Assignment")
        self.use_algorithm = 5

    def RMA(self):
        self.algorithm_used.config(text="Algorithm: Rate Monotonic Assignment")
        self.use_algorithm = 6

    def tasks_frame(self):
        my_canvas = Canvas(self.root, bg="#F5F5F5")
        my_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        my_scrollbar = Scrollbar(self.root, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.itemconfig('frame', width=my_canvas.winfo_width()))

        self.second_frame = Frame(my_canvas, bg="#F5F5F5")
        self.second_frame.columnconfigure(2, weight=2)

        self.algorithm_used = Label(self.second_frame, text="Algorithm: ", font=("bold"), bg="#F5F5F5", fg="#009900")
        self.algorithm_used.pack()

        self.run_frame = Frame(self.second_frame, bg="#F5F5F5")
        Button(self.run_frame, text="RUN", font=("bold"), bg="#009900", fg="white", bd=0, command=self.Run).pack(side=RIGHT, padx=5, pady=5)

        Label(self.run_frame, text="Max Time:", bg="#F5F5F5", fg="black").pack(side=LEFT, padx=5, pady=5)

        self.max_time_entry = Entry(self.run_frame, justify=CENTER)
        self.max_time_entry.pack(side=LEFT, padx=5, pady=5)

        Label(self.run_frame, text="slots Time:", bg="#F5F5F5", fg="black").pack(side=LEFT, padx=5, pady=5)

        self.slots_time_entry = Entry(self.run_frame, justify=CENTER)
        self.slots_time_entry.pack(side=LEFT, padx=5, pady=5)
        
        my_canvas.create_window((0, 0), window=self.second_frame, anchor="nw", tags='frame')

        self.second_frame.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

       
    def task(self, num):
        self.run_frame.pack_forget()
        f = Frame(self.second_frame, bg="#F5F5F5")
        f.pack(fill=X, expand=True,pady=5)
        self.tasks.append(f)
        Label(f, text=f"Task no.{num}", font=("bold"), bg="#F5F5F5", fg="black").grid(row=0, column=0)
        Label(f, text="_____________________________________________________________________________________________________", bg="#F5F5F5", fg="black").grid(row=1, column=0)

        f2 = Frame(f, bg="#F5F5F5")
        f2.grid(row=2, column=0)
        f2.columnconfigure(0, weight=2)

        Label(f2, text="Release time: ", bg="#F5F5F5", fg="black").grid(row=0, column=1)
        rt_entry = Entry(f2, justify=CENTER)
        rt_entry.grid(row=0, column=2)
        self.rt_entries.append(rt_entry)

        Label(f2, text="Execution time: ", bg="#F5F5F5", fg="black").grid(row=1, column=1)
        et_entry = Entry(f2, justify=CENTER)
        et_entry.grid(row=1, column=2)
        self.et_entries.append(et_entry)

        Label(f2, text="Period: ", bg="#F5F5F5", fg="black").grid(row=0, column=3)
        pt_entry = Entry(f2, justify=CENTER)
        pt_entry.grid(row=0, column=4)
        self.pt_entries.append(pt_entry)

        Label(f2, text="Deadline: ", bg="#F5F5F5", fg="black").grid(row=1, column=3)
        dt_entry = Entry(f2, justify=CENTER)
        dt_entry.grid(row=1, column=4)
        self.dt_entries.append(dt_entry)
        Label(f, text="_____________________________________________________________________________________________________", bg="#F5F5F5", fg="black").grid(row=3, column=0)
        self.run_frame.pack()

    def refresh(self, *args):
        tasks_num = self.no_tasks.get()
        if tasks_num == len(self.tasks):
            pass
        if tasks_num > len(self.tasks):
            for i in range(len(self.tasks)+1, tasks_num+1):
                self.task(i)
        else:
            for i in range(len(self.tasks)-tasks_num):
                self.tasks.pop(-1).destroy()
                self.rt_entries.pop(-1)
                self.et_entries.pop(-1)
                self.pt_entries.pop(-1)
                self.dt_entries.pop(-1)

        if tasks_num == 0:
            self.run_frame.pack_forget()

    def Run(self):
        tasks = []
        results = None
        try:
           max_time = int(self.max_time_entry.get())
           if self.use_algorithm == 2:  
                slot_time = float(self.slots_time_entry.get())
           else:
                slot_time = None  

        except ValueError:
            self.error_message("Please ensure that the maxtime is an integer number and slot is a floating number")
            return  

        if self.check_entries():
            results = []
            if self.use_algorithm == 1:
                for arg in range(len(self.rt_entries)):
                    tasks.append(FCFO_T(f"T{arg+1}", float(self.rt_entries[arg].get()), float(self.pt_entries[arg].get()), float(self.et_entries[arg].get()), float(self.dt_entries[arg].get()), max_time))
                results = FCFO_S(tasks, max_time).get_results()
            elif self.use_algorithm == 2:
                for arg in range(len(self.rt_entries)):
                    tasks.append(RR_T(f"T{arg+1}", float(self.rt_entries[arg].get()), float(self.pt_entries[arg].get()), float(self.et_entries[arg].get()), float(self.dt_entries[arg].get()), max_time))
                results = RR_S(tasks, max_time,slot_time).schedule()
                results = RR_S(tasks, max_time,slot_time).get_results()
            elif self.use_algorithm == 3:
                for arg in range(len(self.rt_entries)):
                    tasks.append(MLF_T(f"T{arg+1}", float(self.rt_entries[arg].get()), float(self.pt_entries[arg].get()), float(self.et_entries[arg].get()), float(self.dt_entries[arg].get()), max_time))
                results = MLF_S(tasks, max_time).get_results()
            elif self.use_algorithm == 4:
                for arg in range(len(self.rt_entries)):
                    tasks.append(EDF_T(f"T{arg + 1}", float(self.rt_entries[arg].get()), float(self.pt_entries[arg].get()), float(self.et_entries[arg].get()), float(self.dt_entries[arg].get()), max_time))
                results = EDF_S(tasks, max_time).get_results()
            elif self.use_algorithm == 5:
                for arg in range(len(self.rt_entries)):
                    tasks.append(DMA_T(f"T{arg + 1}", float(self.rt_entries[arg].get()), float(self.pt_entries[arg].get()),float(self.et_entries[arg].get()), float(self.dt_entries[arg].get()), max_time))
                results = DMA_S(tasks, max_time).get_results()
            elif self.use_algorithm == 6:
                for arg in range(len(self.rt_entries)):
                    tasks.append(RMA_T(f"T{arg + 1}", float(self.rt_entries[arg].get()), float(self.pt_entries[arg].get()), float(self.et_entries[arg].get()), float(self.dt_entries[arg].get()), max_time))
                results = RMA_S(tasks, max_time).get_results()
            else:
                self.error_message("please choose an algorithm to use.")
            if results:
                self.results_window(results)

    def error_message(self, msg):
        messagebox.showerror("Error", msg)

    def check_entries(self):
        for entry in range(len(self.rt_entries)):
            try:
                float(self.rt_entries[entry].get())
                float(self.pt_entries[entry].get())
                float(self.et_entries[entry].get())
                float(self.dt_entries[entry].get())
            except:
                self.error_message("Please ensure that all entries are filled either with integer or float numbers")
                return False
        return True

    def results_window(self, results):
        rw = Toplevel(self.root)
        rw.geometry("1000x600+0+0")
        rw.title("Results")

        my_canvas = Canvas(rw, bg="#2069e0")
        my_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        my_scrollbar = Scrollbar(rw, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.itemconfig('frame', width=my_canvas.winfo_width()))

        second_frame = Frame(my_canvas, bg="#444444")

        execution_frame = Frame(second_frame, bg="#444444")
        execution_frame.pack(fill=X, expand=True, pady=10)
        Label(execution_frame, text="Execution Result: ", font=("bold"), bg="#444444", fg="white").pack(side=TOP)
        exec_dict = results[0]
        fig = self.get_exe_figure(exec_dict)
        execution_fig = FigureCanvasTkAgg(fig, execution_frame)
        execution_fig.get_tk_widget().pack(side=BOTTOM)

        if self.use_algorithm == 3:
            slack_table = results[1]
            table_frame = Frame(second_frame, bg="#444444")
            table_frame.pack(fill=X, expand=True, pady=10)
            Label(table_frame, text="Slack Table: ", font=("bold"), bg="#444444",
                  fg="white").pack(side=TOP)
            data = {}
            for row in slack_table:
                data[row[1]] = {"time": row[1]}
                for index, slack_time in enumerate(row[0]):
                    slack_time = "-" if slack_time == None else slack_time
                    data[row[1]][f"T{index+1}"] = slack_time

            my_frame = Frame(table_frame, bg="#444444")
            my_frame.pack(side=BOTTOM)
            table = TableCanvas(my_frame, data=data,
                                cellwidth=60, cellbackgr='#e3f698',
                                thefont=('times new roman', 20), rowheight=23, rowheaderwidth=50,
                                rowselectedcolor='yellow', read_only=True)
            table.show()
        elif self.use_algorithm == 4:
            deadline_table = results[1]
            table_frame = Frame(second_frame, bg="#444444")
            table_frame.pack(fill=X, expand=True)
            Label(table_frame, text="Deadline Table: ", font=("bold"), bg="#444444",
                  fg="white").pack(side=TOP)
            data = {}
            for row in deadline_table:
                data[row[1]] = {"time": row[1]}
                for index, deadline_time in enumerate(row[0]):
                    deadline_time = "-" if deadline_time == None else deadline_time
                    data[row[1]][f"T{index + 1}"] = deadline_time

            my_frame = Frame(table_frame, bg="#444444")
            my_frame.pack(side=BOTTOM)
            table = TableCanvas(my_frame, data=data,cellwidth=60, cellbackgr='#e3f698', rowheight=23, rowheaderwidth=50, rowselectedcolor='yellow', read_only=True)
            table.show()
        else:
            task_priorities = results[1]
            priorities_frame = Frame(second_frame, bg="#444444")
            priorities_frame.pack(fill=X, expand=True, pady=10)
            Label(priorities_frame, text="Tasks Priorities:", font=("bold"), bg="#444444", fg="white").pack(side=TOP)
            priorities = ""
            for task in task_priorities.keys():
                priorities += f"{task}: {task_priorities[task]} \t"
            Label(priorities_frame, text= priorities, bg="#444444", fg="white").pack(side=BOTTOM)

        broken_deadlines = results[2]
        broken_deadline_frame = Frame(second_frame, bg="#444444")
        broken_deadline_frame.pack(fill=X, expand=True, pady=10)
        Label(broken_deadline_frame, text="Broken Deadlines: ", font=("bold"), bg="#444444", fg="white").pack(side=TOP)
        broken_deadlines_text = ""
        for task in broken_deadlines.keys():
            broken_deadlines_text += f"{task}: {broken_deadlines[task]} \t"
        Label(broken_deadline_frame, text= broken_deadlines_text, bg="#444444", fg="white").pack(side=BOTTOM)

        my_canvas.create_window((0, 0), window=second_frame, anchor="nw", tags='frame')

        second_frame.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    def get_exe_figure(self, exec_dict):
        colors = ['#FFCC00', '#ADD8E6', 'gray', 'red', 'purple']

        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size as needed

        i = 1
        for task in exec_dict.keys():
            for execution in exec_dict[task]:
                execution[1] -= execution[0]

            ax.broken_barh(exec_dict[task], (10 * i, 10), facecolors=f'{colors[i - 1]}')
            i += 1

        max_time = int(self.max_time_entry.get())  
        ax.set_xlim(0, max_time * 1.1)  
        ax.set_ylim(5, 15 + 10 * (len(self.tasks)))
        ax.set_xlabel('Time')
        if max_time <= 40:
            ax.set_xticks(range(max_time + 1))
        
        ax.set_yticks([15 + 10 * tick for tick in range(len(self.tasks))], labels=[f'T{tnum + 1}' for tnum in range(len(self.tasks))])
        ax.grid(True)

        return fig



