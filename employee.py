import sqlite3
from tkinter import messagebox, ttk
from tkinter import *

class basicWindow():
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+230+140")
        self.root.title("Shop Management System Project")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.iconbitmap("img/icon.ico")

        #===variables===
        self.varEmpId=StringVar()
        self.varName=StringVar()
        self.varEmail=StringVar()
        self.varGender=StringVar()
        self.varDOB=StringVar()
        self.varPass=StringVar()
        self.varContact=StringVar()
        self.varUType=StringVar()
        self.varSalary=StringVar()


        self.varSearchBy=StringVar()
        self.varSearchTxt=StringVar()
        

class EC(basicWindow):
    def __init__(self,root):
        super().__init__(root)
        self.row = False
  
        #===search frame===
        searchFrame=LabelFrame(self.root,text="Search Employee",bd=2,relief=RIDGE,font=("goudy old style",12,"bold"),bg="white")
        searchFrame.place(x=50,y=20,width=800,height=70)

        #===otions===
        cmbSearch=ttk.Combobox(searchFrame,textvariable=self.varSearchBy,values=("Name","Email","Contact"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbSearch.pack(side=LEFT,padx=10)
        # cmbSearch.place(x=10,y=10,width=180)
        cmbSearch.current(0)

        txtSearch=Entry(searchFrame,textvariable=self.varSearchTxt,font=("goudy old style",15),bg="lightyellow")
        txtSearch.pack(side=LEFT,padx=10)
        txtSearch.configure(width=42)
        # .place(x=200,y=10)

        
        btnSearch=Button(searchFrame,text="Search",command=self.search,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",20))
        btnSearch.pack(side=RIGHT,padx=10,pady=8)
        # .place(x=410,y=9,width=150,height=30)



        #===title===
        title=Label(self.root,text="Employee Details",bg="#0f4d7d",fg="white",font=("goudy old style",20)).place(x=20,y=100,width=1060)



        #===buttons===
        btnAdd=Button(self.root,text="Add",command=self.add,bg="#2196f3",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=870,y=25,width=100,height=27)
        
        btnUpdate=Button(self.root,text="Update",command=self.update,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=870,y=62,width=100,height=27)
        
        btnDelete=Button(self.root,text="Delete",command=self.delete,bg="#f44336",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=980,y=62,width=100,height=27)
        
        btnClearFilter=Button(self.root,text="Clear Filter",command=self.show,bg="#607d86",fg="white",cursor="hand2",font=("goudy old style",16)).place(x=980,y=25,width=100,height=27)
        
        #====Employee Details===
        empFrame=Frame(self.root,bd=3,relief=RIDGE)
        empFrame.place(x=0,y=150,relwidth=1,height=350)

        scrolly=Scrollbar(empFrame,orient=VERTICAL)
        scrollx=Scrollbar(empFrame,orient=HORIZONTAL)

        self.employeeTable=ttk.Treeview(empFrame,columns=("eid","name","email","gender","contact","dob","pass","utype","address","salary"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.employeeTable.xview)
        scrolly.config(command=self.employeeTable.yview)
        self.employeeTable.heading("eid",text="EMP ID")
        self.employeeTable.heading("name",text="Name")
        self.employeeTable.heading("email",text="E-mail")
        self.employeeTable.heading("gender",text="Gender")
        self.employeeTable.heading("contact",text="Contact")
        self.employeeTable.heading("dob",text="D.O.B")
        self.employeeTable.heading("pass",text="Password")
        self.employeeTable.heading("utype",text="User Type")
        self.employeeTable.heading("address",text="Address")
        self.employeeTable.heading("salary",text="Salary")
        self.employeeTable["show"]="headings"

        self.employeeTable.column("eid",width=50,anchor=CENTER)
        self.employeeTable.column("name",width=120,anchor=CENTER)
        self.employeeTable.column("email",width=200,anchor=CENTER)
        self.employeeTable.column("gender",width=60,anchor=CENTER)
        self.employeeTable.column("contact",width=70,anchor=CENTER)
        self.employeeTable.column("dob",width=90,anchor=CENTER)
        self.employeeTable.column("pass",width=90,anchor=CENTER)
        self.employeeTable.column("utype",width=90,anchor=CENTER)
        self.employeeTable.column("address",width=90,anchor=CENTER)
        self.employeeTable.column("salary",width=90,anchor=CENTER)
        self.employeeTable.bind("<ButtonRelease-1>",self.getData)

        self.employeeTable.pack(fill=BOTH,expand=1)

        self.show()

#========================================================================================
    #===show records in table===
    def show(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from employee")
            rows=cur.fetchall()
            self.employeeTable.delete(*self.employeeTable.get_children())
            for row in rows:
                self.employeeTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

    def getData(self,ev):
        f=self.employeeTable.focus()
        content=(self.employeeTable.item(f))
        self.row=content['values']


    def add(self):
        adddetails = Toplevel(self.root)
        self.empdetail = empDetails(adddetails,"Add")
        self.empdetail.btnCheck.configure(background="#2196f3")

    def update(self):
        if self.row:
            updatedetails = Toplevel(self.root)
            self.empdetail = empDetails(updatedetails,"Update")
            empDetails.setData(self.empdetail)
            self.empdetail.btnCheck.configure(bg="#4caf50")
        else:
            messagebox.showerror("Error",f"Select a employee first",parent=self.root)

    def delete(self):
        if self.row:
            deletedetails = Toplevel(self.root)
            self.empdetail = empDetails(deletedetails,"Delete")
            empDetails.setData(self.empdetail)
            self.empdetail.btnCheck.configure(bg="#f44336")
        else:
            messagebox.showerror("Error",f"Select a employee first",parent=self.root)

    #===search function===
    def search(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSearchTxt.get()=="":
                messagebox.showinfo("Error",f"Enter {self.varSearchBy.get()} to search",parent=self.root)
            else:
                cur.execute(f"Select * from employee where {self.varSearchBy.get()} LIKE '%{self.varSearchTxt.get()}%'")
                rows=cur.fetchall()
                if rows==0:
                    messagebox.showerror("Error","No Record Found",parent=self.root)
                else:
                    self.employeeTable.delete(*self.employeeTable.get_children())
                    for row in rows:
                        self.employeeTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

#=============================================================================================================================================================
class empDetails(basicWindow):
    def __init__(self,root,func):
        super().__init__(root)
        self.root.geometry("800x400+380+140")
        self.func = func

        self.deatilsFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")

        #===content===
        lblEmpId=Label(self.deatilsFrame,text="EmpId",bg="white",font=("goudy old style",15)).place(x=50,y=20)
        txtEmpId=Entry(self.deatilsFrame,textvariable=self.varEmpId,bg="lightyellow",font=("goudy old style",15)).place(x=150,y=20,width=180)

        lblEmail=Label(self.deatilsFrame,text="Email",bg="white",font=("goudy old style",15)).place(x=50,y=60)
        txtEmail=Entry(self.deatilsFrame,textvariable=self.varEmail,bg="lightyellow",font=("goudy old style",15)).place(x=150,y=60,width=180)
        
        lblPass=Label(self.deatilsFrame,text="Password",bg="white",font=("goudy old style",15)).place(x=50,y=100)
        txtPass=Entry(self.deatilsFrame,textvariable=self.varPass,bg="lightyellow",font=("goudy old style",15)).place(x=150,y=100,width=180)

        lblName=Label(self.deatilsFrame,text="Name",bg="white",font=("goudy old style",15)).place(x=50,y=140)
        txtName=Entry(self.deatilsFrame,textvariable=self.varName,bg="lightyellow",font=("goudy old style",15)).place(x=150,y=140,width=180)

        lblContact=Label(self.deatilsFrame,text="Contact",bg="white",font=("goudy old style",15)).place(x=50,y=180)
        txtContact=Entry(self.deatilsFrame,textvariable=self.varContact,bg="lightyellow",font=("goudy old style",15)).place(x=150,y=180,width=180)    

        lblUType=Label(self.deatilsFrame,text="UType",bg="white",font=("goudy old style",15)).place(x=50,y=220)
        cmbUType=ttk.Combobox(self.deatilsFrame,textvariable=self.varUType,values=("Employee","Admin"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbUType.place(x=150,y=220,width=180)
        cmbUType.current(0)

        lblAddress=Label(self.deatilsFrame,text="Address",bg="white",font=("goudy old style",15)).place(x=50,y=270)
        self.txtAddress=Text(self.deatilsFrame,bg="lightyellow",font=("goudy old style",15))
        self.txtAddress.place(x=150,y=270,width=330,height=70)
        
        lblGender=Label(self.deatilsFrame,text="Gender",bg="white",font=("goudy old style",15)).place(x=400,y=20)
        cmbGender=ttk.Combobox(self.deatilsFrame,textvariable=self.varGender,values=("Male","Female","Others"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbGender.place(x=500,y=20,width=180)
        cmbGender.current(0)

        lblDOB=Label(self.deatilsFrame,text="DOB",bg="white",font=("goudy old style",15)).place(x=400,y=60)
        txtDOB=Entry(self.deatilsFrame,textvariable=self.varDOB,bg="lightyellow",font=("goudy old style",15)).place(x=500,y=60,width=180)
        
        lblSalary=Label(self.deatilsFrame,text="Salary",bg="white",font=("goudy old style",15)).place(x=400,y=100)        
        txtSalary=Entry(self.deatilsFrame,textvariable=self.varSalary,bg="lightyellow",font=("goudy old style",15)).place(x=500,y=100,width=180)

        
        self.btnCheck=Button(self.root,text=self.func,command=self.check,fg="white",cursor="hand2",font=("goudy old style",20))
        self.btnCheck.place(x=530,y=300,width=150,height=27)
        

        self.deatilsFrame.place(x=0,y=0,height=500,width=1100)

    #===insert selected row data in text feilds===
    def setData(self):
        self.varEmpId.set(obj.row[0])
        self.varName.set(obj.row[1])
        self.varEmail.set(obj.row[2])
        self.varGender.set(obj.row[3])
        self.varContact.set(obj.row[4])
        self.varDOB.set(obj.row[5])
        self.varPass.set(obj.row[6])
        self.varUType.set(obj.row[7])
        self.txtAddress.delete('1.0',END)
        self.txtAddress.insert(END,obj.row[8])
        self.varSalary.set(obj.row[9])

    def check(self):
        if self.func == "Add":
            self.add()
        elif self.func == "Update":
            self.update()
        elif self.func == "Delete":
            self.delete()
        EC.show(obj)

    #===add function===
    def add(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varEmpId.get()=="" or self.varPass.get()=="" or self.varEmail.get()=="":
                messagebox.showerror("Error","Employee ID , email and Password must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from employee where eid={self.varEmpId.get()}")
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID already assigned, try different",parent=self.root)
                else:
                    values=f'"{self.varEmpId.get()}","{self.varName.get()}","{self.varEmail.get()}","{self.varGender.get()}","{self.varContact.get()}","{self.varDOB.get()}","{self.varPass.get()}","{self.varUType.get()}","{self.txtAddress.get(1.0,END)}","{self.varSalary.get()}"'
                    # print(values)
                    cur.execute(f"Insert into employee(eid,name,email,gender,contact,dob,pass,utype,address,salary) values({values})")
                    con.commit()
                    messagebox.showinfo("Success","Employee Added Successfull",parent=self.root)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

    #===update function===
    def update(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varEmpId.get()=="" or self.varPass.get()=="" or self.varEmail.get()=="":
                messagebox.showerror("Error","Employee ID , email and Password must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from employee where eid={self.varEmpId.get()}")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    cur.execute(f"Update employee set name='{self.varName.get()}',email='{self.varEmail.get()}',gender='{self.varGender.get()}',contact='{self.varContact.get()}',dob='{self.varDOB.get()}',pass='{self.varPass.get()}',utype='{self.varUType.get()}',address='{self.txtAddress.get(1.0,END)}',salary='{self.varSalary.get()}' where eid='{self.varEmpId.get()}'")
                    con.commit()
                    messagebox.showinfo("Success","Employee updated Successfull",parent=self.root)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        
    #===delete function===
    def delete(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varEmpId.get()=="":
                messagebox.showerror("Error","Employee ID must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from employee where eid='{self.varEmpId.get()}'")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Employee ID",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op:
                        cur.execute(f"Delete from employee where eid={self.varEmpId.get()}")
                        con.commit()
                        messagebox.showinfo("Success","Employee deleted Successfull",parent=self.root)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        



if __name__=="__main__":
    root=Tk()
    obj=EC(root)
    root.mainloop()