import tkinter as tk
from tkinter import ttk, messagebox
import os

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口左上角坐标
x = int((screen_width - root.winfo_reqwidth()) / 2.5)
y = int((screen_height - root.winfo_reqheight()) / 2.5)

# 设置窗口位置
root.geometry("+{}+{}".format(x, y))

root.title("版本1.0.0--fang523")


frame1 = ttk.Frame(root)
frame1.pack(padx=10, pady=10)

# 添加三个单选按钮，并将第一个按钮设置为默认选中状态
var = tk.StringVar(value=os.path.join(os.getenv("APPDATA"), "Factorio", "mods"))
choices = [("steam版默认路径： %appdata%\\Factorio\\mods", os.path.join(os.getenv("APPDATA"), "Factorio", "mods")),
           ("游戏安装目录： D:\\Steam\\steamapps\\common\\Factorio\\mods", "D:\\Steam\\steamapps\\common\\Factorio\\mods"),
           ("自定义路径", "")]

tip_label = ttk.Label(frame1, text="①本软件可以清理Factorio的旧版MOD文件。 \n②仅检测zip文件，跳过文件夹形式的MOD。 \n③软件读取文件名进行版本号对比，无需联网。\n④懒得写报错，如果文件夹不存在：不会有报\n错提示，也不会有清理成功的提示\n\n  请在下面选择你的MOD文件夹路径")
tip_label.grid(row=0, column=0, pady=5)

for i, (choice, path) in enumerate(choices):
    ttk.Radiobutton(frame1, text=choice, variable=var, value=path).grid(row=i+1, column=0, sticky="w", pady=5)

# 添加输入框和确认按钮
frame2 = ttk.Frame(root)
frame2.pack(padx=10, pady=(0, 10))
path_entry = ttk.Entry(frame2, width=40)
path_entry.grid(row=0, column=0, padx=5)
ttk.Button(frame2, text="确定", command=lambda: get_folder_path(path_entry, var)).grid(row=0, column=1, padx=5)

# 做一个布尔类型的标记，表示用户是否选择了自定义路径
is_custom_path = tk.BooleanVar()

# 当单选按钮被点击时，更新输入框状态
def update_path_entry():
    if var.get() == "":
        path_entry.config(state="normal")
        is_custom_path.set(True)
    else:
        path_entry.config(state="disabled")
        is_custom_path.set(False)

var.trace_add("write", lambda *_: update_path_entry())
update_path_entry()


def get_folder_path(entry, var):
    """
    获取用户选择的文件夹路径，并清理 MOD 文件
    """
    if is_custom_path.get():
        folder_path = entry.get()
    else:
        folder_path = var.get()

    # 如果用户没有选择任何文件夹，则退出程序
    if not folder_path:
        messagebox.showinfo("未输入", "请输入或选择你的MOD文件存放位置")
        return

    # 遍历文件夹内所有格式为 zip 的文件
    mod_files = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".zip"):
            # 解析 MOD 名称和版本号
            mod_name, version = file_name[:-4].split("_")[0], file_name[:-4].split("_")[1]

            # 如果该 MOD 已经出现过，则比较版本号并更新字典
            if mod_name in mod_files:
                if version > mod_files[mod_name][0]:
                    # 删除旧版 MOD 文件
                    os.remove(os.path.join(folder_path, mod_files[mod_name][1]))
                    mod_files[mod_name] = (version, file_name)
                else:
                    # 删除当前文件
                    os.remove(os.path.join(folder_path, file_name))
            else:
                mod_files[mod_name] = (version, file_name)

    # 显示清理完成提示信息并退出程序
    messagebox.showinfo("完成", "清理完成")


root.mainloop()
