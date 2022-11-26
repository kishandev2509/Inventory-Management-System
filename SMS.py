from os import getcwd
from subprocess import call
import smtplib
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


        #===images===
        # self.phoneImage=ImageTk.PhotoImage(file="img/phone.png")
        # self.phoneImage=ImageTk.PhotoImage(file="images/phone.png")
        # self.phoneImage=ImageTk.PhotoImage(file="images/phone.png")

        # self.lblPhoneImage=Label(self.root,image=self.phoneImage,bd=0).place(x=200,y=50)

        
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

        # lblHr=Label(loginFrame,bg="lightgrey").place(x=50,y=370,width=250,height=2)
        # lblOr=Label(loginFrame,text="OR",bg="white",fg="lightgrey",font=("times new roman",15,"bold")).place(x=150,y=355)
        
        # btnforget=Button(loginFrame,text="Forget Password?",command=self.forgetWindow,font=("times new roman",13),bg="white",activebackground="white",cursor="hand2",fg="#00759E",activeforeground="#00759E",bd=0).place(x=100,y=390,height=35)

        createDB()
        self.setUsername()

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
        

    
    def forgetWindow(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varEmployeeID.get()=="":
                messagebox.showerror("Error","Employee id must be required",parent=self.root)
            else:
                cur.execute(f"select email from employee where eid='{self.varEmployeeID.get()}'")
                email=cur.fetchone()
                if email[0]==None:
                    messagebox.showerror("Error","Invalid Employee id",parent=self.root)
                else:
                    chk=self.sendEmail(email[0])
                    if chk!="s":
                        messagebox.showerror("Error","Connection Error, try again",parent=self.root)
                    else:
                        self.forgetWindowFrame=Toplevel(self.root)
                        self.forgetWindowFrame.title("RESET PASSWORD")
                        self.forgetWindowFrame.geometry("400x350+500+100")
                        self.forgetWindowFrame.focus_force()
                        self.forgetWindowFrame.iconbitmap("img/icon.ico")

                        lblTitle=Label(self.forgetWindowFrame,text="Reset Password",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white").pack(side=TOP,fill=X)
                        
                        lblSubmit=Label(self.forgetWindowFrame,text="Enter OTP sent on registerd email",font=("times new roman",15),fg="#767171").place(x=20,y=60)
                        txtSubmit=Entry(self.forgetWindowFrame,textvariable=self.varOTP,font=("times new roman",15),bg="lightyellow",fg="#767171").place(x=20,y=100,width=250,height=30)
                        
                        self.btnSubmit=Button(self.forgetWindowFrame,text="Submit",command=self.validateOTP,font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",cursor="hand2",activeforeground="white")
                        self.btnSubmit.place(x=280,y=100,height=30,width=100)


                        lblNewPassword=Label(self.forgetWindowFrame,text="New Password",font=("Andalus",15,"bold"),fg="#767171").place(x=50,y=160)
                        txtNewPassword=Entry(self.forgetWindowFrame,textvariable=self.varNewPassword,font=("times new roman",15,"bold"),bg="lightyellow",fg="#767171").place(x=20,y=190,width=250,height=30)

                        lblConfirmPassword=Label(self.forgetWindowFrame,text="Confirm Password",font=("Andalus",15,"bold"),fg="#767171").place(x=20,y=225)
                        txtConfirmPassword=Entry(self.forgetWindowFrame,textvariable=self.varConfirmPassword,font=("times new roman",15,"bold"),bg="lightyellow",fg="#767171").place(x=20,y=255,width=250,height=30)

                        
                        self.btnUpdate=Button(self.forgetWindowFrame,text="Update",command=self.updatePassword,font=("Arial Rounded MT Bold",15),state=DISABLED,bg="#00B0F0",cursor="hand2",activebackground="#00B0F0",activeforeground="white")
                        self.btnUpdate.place(x=150,y=300,height=30,width=100)


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        

    def sendEmail(self,to_):
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        email_=epfile.email_
        pass_=epfile.pass_
        s.login(email_,pass_)
        # subj="SMS-Reset Password OTP"
        msg=f"Subject: SMS-Reset Password OTP\n\nDear sir/Madam, \n\tYour reset OTP for your SMS-Shop Management System is {self.OTP}\n\n\t\tWith Regards,\n\tSMS-Shop Management System Team"
        s.sendmail(email_,to_,msg)
        chk=s.ehlo()
        if chk[0]==250:
            return "s"
        else:
            return 'f'

    def validateOTP(self):
        if int(self.OTP)==int(self.varOTP.get()):
            self.btnUpdate.config(state=NORMAL)
            self.btnSubmit.config(state=DISABLED)
        else:
            messagebox.showerror("Error",f"Invalid OTP",parent=self.forgetWindowFrame)

    def updatePassword(self):
        if self.varNewPassword.get()=="" or self.varConfirmPassword.get()=="":
            messagebox.showerror("Error",f"Password is required",parent=self.forgetWindowFrame)
        elif self.varNewPassword.get()!=self.varConfirmPassword.get():
            messagebox.showerror("Error",f"Passwords do not match",parent=self.forgetWindowFrame)
        else:
            con=sqlite3.connect(database=r"sms.db")
            cur=con.cursor()
            cur.execute(f"Update employee set pass='{self.varNewPassword.get()}' where eid='{self.varEmployeeID.get()}'")
            con.commit()
            messagebox.showinfo("Success","Employee updated Successfull",parent=self.forgetWindowFrame)
            self.forgetWindowFrame.destroy()


    def setUsername(self):
            con=sqlite3.connect(database=r"sms.db")
            cur=con.cursor()
            cur.execute(f"select eid from employee limit 1")
            empid=cur.fetchone()[0]
            self.varEmployeeID.set(empid)
    

root=Tk()
obj=loginSystem(root)
root.mainloop()