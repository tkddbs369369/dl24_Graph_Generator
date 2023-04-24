import csv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from matplotlib import font_manager, rc
from tkinter import *
from tkinter import filedialog
import os
import chardet

# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)
# pyinstaller용


def draw_graph(path, save_path, y_number=33, x_number=13, x_size=12, y_size=10):
    font_path = "C:/Windows/Fonts/gulim.ttc"
    font = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font)
    plt.rc('ytick', labelsize=15)
    plt.rc('axes', labelsize=24)

    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader) # 첫째줄 무시
        DT = []
        TestTime = []
        TestOn = []
        Voltage = []
        Current = []
        W = []
        WH = []
        AH = []
        Temperature = []

        for row in reader:
            if int(row[2]) == 1:
                DT.append(row[0])
                TestTime.append(row[1])
                TestOn.append(int(row[2]))
                Voltage.append(float(row[3]))
                Current.append(float(row[4]))
                W.append(float(row[5]))
                WH.append(float(row[6]))
                AH.append(float(row[7]))
                Temperature.append(int(row[8]))

    TestTime = [datetime.strptime(t, "%p %I:%M:%S") for t in TestTime]
    elapsed_time = [(t - TestTime[0]).total_seconds() / 3600 for t in TestTime]
    elapsed_time = [t - elapsed_time[0] for t in elapsed_time]
    y = np.linspace(round(min(Voltage), 2), round(max(Voltage), 2), y_number)
    y = [round(i, 2) for i in y]
    y.insert(0, round(min(Voltage), 2))
    y.append(round(max(Voltage), 2))
    start_time = TestTime[0].replace(hour=0, minute=0, second=0,microsecond=0)
    x_ticks=np.linspace(0 ,elapsed_time[-1],x_number)
    x_ticklabels=[start_time+timedelta(hours=x) for x in x_ticks]
    x_ticklabels=[dt.strftime('%H:%M:%S') for dt in x_ticklabels]
    fig, ax = plt.subplots(figsize=(x_size,y_size))
    plt.plot(elapsed_time, Voltage)
    plt.ylim([min(Voltage), max(Voltage)])
    plt.xticks(x_ticks,x_ticklabels)
    plt.yticks(y)
    plt.xlabel('작동시간')
    plt.ylabel('전압')
    plt.savefig(save_path)



def browse_file():
    filename = filedialog.askopenfilename()
    path_entry.delete(0, END)
    path_entry.insert(0, filename)

def browse_save_file():
    filename = filedialog.asksaveasfilename(defaultextension=".png")
    save_path_entry.delete(0, END)
    save_path_entry.insert(0, filename)

def set_current_path():
    current_path = os.getcwd()
    i = 0
    while True:
        if i == 0:
            save_filename = "graph.png"
        else:
            save_filename = f"graph{i}.png"
        save_path = os.path.join(current_path, save_filename)
        if not os.path.exists(save_path):
            break
        i += 1
    save_path_entry.delete(0, END)
    save_path_entry.insert(0, save_path)

def draw():
    path = path_entry.get()
    save_path = save_path_entry.get()
    y_number = int(y_number_entry.get())
    x_number = int(x_number_entry.get())
    x_size = int(x_size_entry.get())
    y_size = int(y_size_entry.get())

    with open(path, 'rb') as f:
        rawdata = f.read()
        encoding = chardet.detect(rawdata)['encoding']

    with open(path, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        rows = [row for row in reader]

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            new_row = [cell.replace('오전', 'AM').replace('오후', 'PM') for cell in row]
            writer.writerow(new_row)

    draw_graph(path, save_path, y_number=y_number,
               x_number=x_number, x_size=x_size, y_size=y_size)
root = Tk()
root.title("dl24 그래프 생성기v1")
root.geometry("400x400")
root.iconbitmap('dl24.ico')
# root.iconbitmap(resource_path('dl24.ico')) pyinstaller 용

path_label = Label(root,text="파일 경로")
path_label.pack()

path_entry = Entry(root)
path_entry.pack()

browse_button = Button(root,text="찾아보기", command=browse_file)
browse_button.pack()

save_path_label=Label(root,text="저장 경로")
save_path_label.pack()

save_path_entry=Entry(root)
save_path_entry.pack()

browse_save_button=Button(root,text="찾아보기",command=browse_save_file)
browse_save_button.pack()

current_path_button = Button(root, text="현재 경로", command=set_current_path)
current_path_button.pack()

y_number_label=Label(root,text="y축 간격")
y_number_label.pack()

y_number_entry = Entry(root)
y_number_entry.insert(0, "33")
y_number_entry.pack()

x_number_label = Label(root, text="x축 간격")
x_number_label.pack()

x_number_entry = Entry(root)
x_number_entry.insert(0, "13")
x_number_entry.pack()

x_size_label = Label(root, text="그래프 가로 크기")
x_size_label.pack()

x_size_entry = Entry(root)
x_size_entry.insert(0, "12")
x_size_entry.pack()

y_size_label = Label(root, text="그래프 세로 크기")
y_size_label.pack()
y_size_entry = Entry(root)
y_size_entry.insert(0, "10")
y_size_entry.pack()

draw_button = Button(root, text="변환", command=draw)
draw_button.pack()

root.mainloop()