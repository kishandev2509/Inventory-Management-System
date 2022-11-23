from subprocess import call
from os import listdir,getcwd
import sqlite3
import time
from tkinter import *
from tkinter import messagebox
from functions import *
from employee import EC
from product import productClass
from sales import salesClass
from supplier import supplierClass
from category import categoryClass
class RM:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+10+10")
        self.root.title("Shop Management System Project")
        self.root.config(bg="white")
        self.root.iconbitmap("img/icon.ico")
        self.newObj=None
        self.realPath=getcwd()
  

        #====Header=====
        self.headerIcon=openImage("img/cart.png",50,50)
        header=Label(self.root,text="Shop Management System",image=self.headerIcon,compound=LEFT,font="None 30 bold",bg="#4D4DFF",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #===logout btn===
        btnLogout=Button(self.root,text="Logout",command=self.logout,bg="yellow",cursor="hand2",font="None 20 bold").place(x=1150,y=15,width=150,height=40)

        #===clock===
        self.lblClock=Label(self.root,text="Welcome to Shop Management System\t\tDate: mmm:dd,yy\t\tTime: hh:mm:ss",font="None 15",bg="grey",fg="white")
        self.lblClock.place(x=0,y=70,relwidth=1,height=30)

        #==left Menu===
        self.menuLogo=openImage("img/menu.jpg",200,200)
        leftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        leftMenu.place(x=0,y=102,width=200,height=565)

        lblMenuLogo=Label(leftMenu,image=self.menuLogo).pack(side=TOP,fill=X)

        lblMenu=Label(leftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        
        self.nextIcon=openImage("img/next.png",20,20)

        btnEmployee=Button(leftMenu,text="Employee",image=self.nextIcon,compound=LEFT,bg="white",bd=3,cursor="hand2",font=("times new roman",20),padx=5,anchor="w",command=self.employee).pack(side=TOP,fill=X)

        btnSupplier=Button(leftMenu,text="Supplier",image=self.nextIcon,compound=LEFT,bg="white",bd=3,cursor="hand2",font=("times new roman",20),padx=5,anchor="w",command=self.supplier).pack(side=TOP,fill=X)

        btnCategory=Button(leftMenu,text="Category",image=self.nextIcon,compound=LEFT,bg="white",bd=3,cursor="hand2",font=("times new roman",20),padx=5,anchor="w",command=self.category).pack(side=TOP,fill=X)

        btnProduct=Button(leftMenu,text="Product",image=self.nextIcon,compound=LEFT,bg="white",bd=3,cursor="hand2",font=("times new roman",20),padx=5,anchor="w",command=self.product).pack(side=TOP,fill=X)

        btnSales=Button(leftMenu,text="Sales",image=self.nextIcon,compound=LEFT,bg="white",bd=3,cursor="hand2",font=("times new roman",20),padx=5,anchor="w",command=self.sales).pack(side=TOP,fill=X)

        btnExit=Button(leftMenu,text="Exit",image=self.nextIcon,compound=LEFT,bg="white",bd=3,cursor="hand2",font=("times new roman",20),padx=5,anchor="w",command=self.exit).pack(side=TOP,fill=X)


        #===content===
        
        self.lblEmployee=Label(self.root,text="Total Employee\t[ 0 ]",font="None 25 bold",bg="#33bbf9",fg="white")
        self.lblEmployee.pack(fill=X, pady=(120,10),padx=(300,100),ipady=10)
        # self.lblEmployee.place(x=300,y=120,width=300,height=150)
        
        self.lblSupplier=Label(self.root,text="Total Supplier\t[ 0 ]",font="None 25 bold",bg="#ff5722",fg="white")
        self.lblSupplier.pack(fill=X, pady=10,padx=(300,100),ipady=10)
        # self.lblSupplier.place(x=650,y=120,width=300,height=150)
        
        self.lblCategory=Label(self.root,text="Total Category\t[ 0 ]",font="None 25 bold",bg="#009688",fg="white")
        self.lblCategory.pack(fill=X, pady=10,padx=(300,100),ipady=10)
        # self.lblCategory.place(x=1000,y=120,width=300,height=150)
        
        self.lblProduct=Label(self.root,text="Total Product\t[ 0 ]",font="None 25 bold",bg="#607d86",fg="white")
        self.lblProduct.pack(fill=X, pady=10,padx=(300,100),ipady=10)
        # self.lblProduct.place(x=300,y=300,width=300,height=150)
        
        self.lblSales=Label(self.root,text="Total Sales\t[ 0 ]",font="None 25 bold",bg="#ffc107",fg="white")
        self.lblSales.pack(fill=X, pady=10,padx=(300,100),ipady=10)
        # self.lblSales.place(x=650,y=300,width=300,height=150)
        

        #===footer===
        self.lblFooter=Label(self.root,text="SMS-Shop Management System\n",font="None 12",bg="grey",fg="white")
        self.lblFooter.pack(side=BOTTOM,fill=X)
        
        
        self.updateDateTime()
        self.updateContent()

    #===functions===
    def employee(self):
        if self.newObj!=None:
            self.newObj.root.destroy()
        self.newWin=Toplevel(self.root)
        self.newObj=EC(self.newWin)

    def supplier(self):
        if self.newObj!=None:
            self.newObj.root.destroy()
        self.newWin=Toplevel(self.root)
        self.newObj=supplierClass(self.newWin)

    def category(self):
        if self.newObj!=None:
            self.newObj.root.destroy()
        self.newWin=Toplevel(self.root)
        self.newObj=categoryClass(self.newWin)

    def product(self):
        if self.newObj!=None:
            self.newObj.root.destroy()
        self.newWin=Toplevel(self.root)
        self.newObj=productClass(self.newWin)

    def sales(self):
        if self.newObj!=None:
            self.newObj.root.destroy()
        self.newWin=Toplevel(self.root)
        self.newObj=salesClass(self.newWin)

    def exit(self):
        self.root.destroy()

    def updateDateTime(self):
        date_=time.strftime("%b %d, %Y")
        time_=time.strftime("%H:%M:%S")
        self.lblClock.config(text=f"Welcome to Shop Management System\t\tDate: {date_}\t\tTime: {time_}")
        self.lblClock.after(1000,self.updateContent)

    def updateContent(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("select count(*) from employee")
            data=cur.fetchone()[0]
            self.lblEmployee.config(text=f"Total Employee\t[ {data} ]")

            cur.execute("select count(*) from supplier")
            data=cur.fetchone()[0]
            self.lblSupplier.config(text=f"Total Supplier\t[ {data} ]")

            cur.execute("select count(*) from category")
            data=cur.fetchone()[0]
            self.lblCategory.config(text=f"Total Category\t[ {data} ]")

            cur.execute("select count(*) from product")
            data=cur.fetchone()[0]
            self.lblProduct.config(text=f"Total Product\t[ {data} ]")

            self.lblSales.config(text=f"Total Sales\t[ {len(listdir('bill'))} ]")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

        self.updateDateTime()

    def logout(self):
        self.root.destroy()
        call(["python", resource_path("sms.py")])


if __name__=="__main__":
    root=Tk()
    obj=RM(root)
    root.mainloop()