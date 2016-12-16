# -*- coding: utf-8 -*-

'''
Created on 2016-12-16

@author: Sawatari
'''

import csv
import os
import string
import sys
import ttk
import webbrowser
from Tkinter import *

def refreshTree():
    # 清空
    items = tree.get_children()
    for item in items:
        tree.delete(item)
    # 读取csv
    if os.path.exists('goods.csv'):
        csvfile = file('goods.csv', 'rb')
        if csvfile:
            lines = []
            reader = csv.reader(csvfile)
            i = 0
            # 转存至数组
            for line in reader:
                # 不输出第一行
                if i > 0:
                    lines.append(line)
                i = i + 1

            # 冒泡排序
            for j in range(len(lines) - 1, 0, -1):
                for k in range(j):
                    if string.atof(lines[k][4]) < string.atof(lines[k + 1][4]):
                        lines[k], lines[k + 1] = lines[k + 1], lines[k]
            i = 0
            for line in lines:
                tree.insert('', i, values=(
                    line[0].decode(sys.getfilesystemencoding()), line[1].decode(sys.getfilesystemencoding()),
                    line[2].decode(sys.getfilesystemencoding()), line[3].decode(sys.getfilesystemencoding()),
                    line[4].decode(sys.getfilesystemencoding()), line[5].decode(sys.getfilesystemencoding()),
                    line[6].decode(sys.getfilesystemencoding())))
                i = i + 1

def startSpider():
    # 获取文本框内容
    good = var.get()
    # 关键字保存至临时文件
    temp = open('tempgoods.temp', 'w')
    temp.write(good.encode(sys.getfilesystemencoding()))
    temp.close()

    # 清空goods.csv
    if os.path.exists('goods.csv'):
        csvfile = open('goods.csv', 'w')
        csvfile.truncate()

    # 开始爬虫程序
    os.system("runscrapy.py")

def onDBClick(event):
    # 点击跳转天猫
    item = tree.selection()[0]
    info = tree.item(item, "values")
    url = info[2]
    webbrowser.open_new(url)

reload(sys)
sys.setdefaultencoding('utf8')

root = Tk()
root.title("FindGoods")
# 高宽均不可变
root.resizable(width=False, height=False)

Label(root, text='  ').grid(row=0)
# Label
Label(root, text='输入商品关键字：').grid(row=1)
# 关键字输入框
var = StringVar()
e = Entry(root, textvariable=var).grid(row=2)
# 确认按钮
Button(root, text="开始查询", command=startSpider).grid(row=3)
Button(root, text="刷新表格", command=refreshTree).grid(row=4)

Label(root, text='  ').grid(row=5, column=0)

# 结果csv表格
tree = ttk.Treeview(root, show="headings", columns=('店名', '商品名', '购买链接', '价格', '评分', '月交易量', '评论数'))
# 表格滚动条
ysb = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
xsb = ttk.Scrollbar(root, orient='horizontal', command=tree.xview)
tree.configure(yscroll=ysb.set, xscroll=xsb.set)

tree.column('店名', width=100, anchor='center')
tree.column('商品名', width=250, anchor='center')
tree.column('购买链接', width=125, anchor='center')
tree.column('价格', width=50, anchor='center')
tree.column('评分', width=65, anchor='center')
tree.column('月交易量', width=55, anchor='center')
tree.column('评论数', width=55, anchor='center')
tree.heading('店名', text='店名')
tree.heading('商品名', text='商品名')
tree.heading('购买链接', text='购买链接')
tree.heading('价格', text='价格')
tree.heading('评分', text='评分')
tree.heading('月交易量', text='月交易量')
tree.heading('评论数', text='评论数')
vbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=vbar.set)

# 初始化表格数据
refreshTree()

# 监听Click
tree.bind("<Double-1>", onDBClick)

# tree.pack()
tree.grid(row=6, column=0)
ysb.grid(row=6, column=1, sticky='ns')
xsb.grid(row=7, column=0, sticky='ew')

# 说明
Label(root, text='结果输出表格文件位于项目根目录“goods.csv”').grid(row=8)

# 进入消息循环
root.mainloop()