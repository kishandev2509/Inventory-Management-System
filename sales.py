from os import listdir
from posixpath import splitext
from tkinter import messagebox
from tkinter import *

from functions import openImage
class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+230+140")
        self.root.title("Inventory Management System Project")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.iconbitmap("img/icon.ico")

        #===variables===
        self.varInvoice=StringVar()
        self.billList=[]


        #===title===
        lblTitle=Label(self.root,text="View Customer Bills",bg="#0f4d7d",bd=3,relief=RIDGE,fg="white",font=("goudy old style",20)).pack(side=TOP,fill=X,padx=10,pady=20)
        lblInvoice=Label(self.root,text="Bill No.",bg="white",font=("goudy old style",15)).place(x=50,y=100)   
        self.txtInvoce=Entry(self.root,textvariable=self.varInvoice,bg="lightyellow",font=("goudy old style",15))
        self.txtInvoce.place(x=160,y=100,width=280,height=28)

        btnSearch=Button(self.root,text="Search",command=self.search,bd=3,bg="#184a45",fg="white",cursor="hand2",font=("goudy old style",15,"bold")).place(x=490,y=100,width=120,height=28)

        btnClear=Button(self.root,text="\u2716",command=self.clear,bd=3,bg="grey",cursor="hand2",font=("goudy old style",15,"bold")).place(x=440,y=100,width=40,height=28)



        #====Bill list===
        salesFrame=Frame(self.root,bd=3,relief=RIDGE)
        salesFrame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(salesFrame,orient=VERTICAL)
        self.salesList=Listbox(salesFrame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.salesList.yview)
        self.salesList.pack(fill=BOTH,expand=1)
        self.salesList.bind("<ButtonRelease-1>",self.getData)

        #====Bill Area===
        billFrame=Frame(self.root,bd=3,relief=RIDGE)
        billFrame.place(x=280,y=140,width=410,height=330)

        
        lblTitle2=Label(billFrame,text="Customer Bill Area",bg="orange",font=("goudy old style",20)).pack(side=TOP,fill=X)

        scrolly2=Scrollbar(billFrame,orient=VERTICAL)
        self.billArea=Text(billFrame,font=("goudy old style",12),bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.billArea.yview)
        self.billArea.pack(fill=BOTH,expand=1)

        #===image===
        self.billPhoto=openImage("img/sales.png",380,370)

        lblBillPhoto=Label(self.root,image=self.billPhoto,bd=0)
        lblBillPhoto.place(x=700,y=110)

        
        self.show()

#========================================================================================
    #===show records in table===
    def show(self):
        del self.billList[:]
        self.salesList.delete(0,END)
        for i in listdir('bill'):
            if splitext(i)[-1]==".txt":
                self.salesList.insert(END,i)
                self.billList.append(i.split('.')[0])



    def getData(self,ev):
        index_=self.salesList.curselection()
        fileName=self.salesList.get(index_)
        self.billArea.delete(1.0,END)
        with open(f"bill/{fileName}","r") as fp:
            for i in fp:
                self.billArea.insert(END,i)

    def search(self):
        if self.varInvoice.get()=="":
            messagebox.showerror("Error","Invoice no. should be required",parent=self.root)
        else:
            if self.varInvoice.get() in self.billList:
                with open(f"bill/{self.varInvoice.get()}.txt","r") as fp:
                    self.billArea.delete("1.0",END)
                    for i in fp:
                        self.billArea.insert(END,i)
            else:
                messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)

    def clear(self):
        self.show()
        self.txtInvoce.delete(0,END)


if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()