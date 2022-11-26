from os import getcwd
from subprocess import call
import sqlite3
import time
from tkinter import messagebox
from createDB import createDB
from tkinter import *

from functions import resource_path


class loginSystem:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+10+10")
        self.root.title("Shop Management System Project")
        self.root.config(bg="white")
        self.realPath=getcwd()
        try:
            self.root.iconbitmap("img/icon.ico")
        except:
            pass

        #====variables====
        self.varEmployeeID=StringVar()
        self.varPassword=StringVar()
        self.varNewPassword=StringVar()
        self.varConfirmPassword=StringVar()
        self.varOTP=StringVar()
        self.OTP=int(time.strftime("%H%S%M"))+int(time.strftime("%S%M%H"))


    
        #===Welcome frame===
        welcomeFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        welcomeFrame.place(x=650,y=90,width=350,height=60)

        lblTxt=Label(welcomeFrame,text="Welcome to SMS-Shop Management System",font=("times new roman",13),bg="white",bd=0).place(x=0,y=20,relwidth=1)

        #===Login frame===
        loginFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        loginFrame.place(x=650,y=170,width=350,height=460)

        lblTitle=Label(loginFrame,text="Login",font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lblUser=Label(loginFrame,text="Employee ID",font=("Andalus",15,"bold"),bg="white",fg="#767171").place(x=50,y=100)
        txtUser=Entry(loginFrame,textvariable=self.varEmployeeID,font=("times new roman",15,"bold"),bg="lightyellow",fg="#767171").place(x=50,y=140)

        lblPassword=Label(loginFrame,text="Password",font=("Andalus",15,"bold"),bg="white",fg="#767171").place(x=50,y=200)
        txtUser=Entry(loginFrame,textvariable=self.varPassword,font=("times new roman",15,"bold"),bg="lightyellow",fg="#767171").place(x=50,y=240)

        btnLogin=Button(loginFrame,text="Log In",command=self.login,font=("Arial Rounded MT Bold",15,"bold"),cursor="hand2",bg="#00B0F0",activebackground="#00B0F0",activeforeground="white").place(x=50,y=300,width=250,height=35)

        createDB()

    #============All Functions===============
    # ====login funtion====
    def login(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varEmployeeID.get()=="" or self.varPassword.get()=="":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute(f"select utype from employee where eid='{self.varEmployeeID.get()}' and pass='{self.varPassword.get()}'")
                user=cur.fetchone()
                if user==None:
                    messagebox.showerror("Error","Invalid USERNAME/PASSWORD",parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        dashboard=resource_path("dashboard.py")
                        print(dashboard)
                        call(["python", dashboard])
                    else:
                        self.root.destroy()
                        call(["python", resource_path("billing.py")])

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

root=Tk()
obj=loginSystem(root)
root.mainloop()