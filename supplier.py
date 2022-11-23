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
        self.varSupInvoice=StringVar()
        self.varName=StringVar()
        self.varContact=StringVar()



class supplierClass(basicWindow):
    def __init__(self,root):
        super().__init__(root)
        self.row = False

        #===variables===
        self.varSearchBy=StringVar()
        self.varSearchTxt=StringVar()
  
        #===search frame===
        searchFrame=LabelFrame(self.root,text="Search Supplier",bd=2,relief=RIDGE,font=("goudy old style",9,"bold"),bg="white")
        searchFrame.place(x=50,y=55,width=640,height=60)

        #===otions===
        cmbSearch=ttk.Combobox(searchFrame,textvariable=self.varSearchBy,values=("Invoice","Name","Contact"),state="readonly",justify=CENTER,font=("goudy old style",11))
        cmbSearch.pack(side=LEFT,padx=10)
        cmbSearch.current(0)

        txtSearch=Entry(searchFrame,textvariable=self.varSearchTxt,font=("goudy old style",15),bg="lightyellow")
        txtSearch.pack(side=LEFT,padx=10)
        txtSearch.configure(width=34)
        # .place(x=110,y=5,width=210)

        
        btnSearch=Button(searchFrame,text="Search",command=self.search,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",12))
        btnSearch.pack(side=RIGHT,padx=10,pady=6)
        # .place(x=330,y=3,width=70,height=30)



        #===title===
        title=Label(self.root,text="Supplier Details",bg="#0f4d7d",fg="white",font=("goudy old style",20)).place(x=50,y=10,width=1000,height=40)

        #===buttons===
        btnAdd=Button(self.root,text="Add",command=self.add,bg="#2196f3",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=700,y=70,width=110,height=35)
        
        btnUpdate=Button(self.root,text="Update",command=self.update,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=820,y=70,width=110,height=35)
        
        btnDelete=Button(self.root,text="Delete",command=self.delete,bg="#f44336",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=940,y=70,width=110,height=35)


        #====supplier Details===
        supFrame=Frame(self.root,bd=3,relief=RIDGE)
        supFrame.place(x=50,y=120,width=1000,height=350)

        scrolly=Scrollbar(supFrame,orient=VERTICAL)
        scrollx=Scrollbar(supFrame,orient=HORIZONTAL)

        self.supplierTable=ttk.Treeview(supFrame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Invoice")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")

        self.supplierTable["show"]="headings"

        self.supplierTable.column("invoice",width=50)
        self.supplierTable.column("name",width=90)
        self.supplierTable.column("contact",width=60)
        self.supplierTable.bind("<ButtonRelease-1>",self.getData)

        self.supplierTable.pack(fill=BOTH,expand=1)

        self.show()

#========================================================================================
    #===show records in table===
    def show(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows=cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

    #===insert selected row data in text feilds===
    def getData(self,ev):
        f=self.supplierTable.focus()
        content=(self.supplierTable.item(f))
        self.row=content['values']


    def add(self):
        adddetails = Toplevel(self.root)
        self.supplierDetail = supplierDetails(adddetails,"Add")
        self.supplierDetail.btnCheck.configure(background="#2196f3")

    def update(self):
        if self.row:
            adddetails = Toplevel(self.root)
            self.supplierDetail = supplierDetails(adddetails,"Update")
            supplierDetails.setData(self.supplierDetail)
            self.supplierDetail.btnCheck.configure(bg="#4caf50")
        else:
            messagebox.showerror("Error",f"Select a employee first",parent=self.root)

    def delete(self):
        if self.row:
            adddetails = Toplevel(self.root)
            self.supplierDetail = supplierDetails(adddetails,"Delete")
            supplierDetails.setData(self.supplierDetail)
            self.supplierDetail.btnCheck.configure(bg="#f44336")
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
                
                cur.execute(f"Select * from supplier where {self.varSearchBy.get()} LIKE '%{self.varSearchTxt.get()}%'")
                rows=cur.fetchall()
                if rows==0:
                    messagebox.showerror("Error","No Record Found",parent=self.root)
                else:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    for row in rows:
                        self.supplierTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)


#=====================================================================================================================================================================
class supplierDetails(basicWindow):
    def __init__(self, root, func):
        super().__init__(root)
        self.root.geometry("800x400+380+140")
        self.func = func


        #===content===
        lblSupplierInvoice=Label(self.root,text="Invoice No.",bg="white",font=("goudy old style",15)).place(x=50,y=20)
        txtSupplierInvoice=Entry(self.root,textvariable=self.varSupInvoice,bg="lightyellow",font=("goudy old style",15)).place(x=180,y=20,width=180)

        lblName=Label(self.root,text="Name",bg="white",font=("goudy old style",15)).place(x=50,y=60)
        txtName=Entry(self.root,textvariable=self.varName,bg="lightyellow",font=("goudy old style",15)).place(x=180,y=60,width=180)

        lblContact=Label(self.root,text="Contact",bg="white",font=("goudy old style",15)).place(x=50,y=100)
        txtContact=Entry(self.root,textvariable=self.varContact,bg="lightyellow",font=("goudy old style",15)).place(x=180,y=100,width=180)
        
        lblDesc=Label(self.root,text="Description",bg="white",font=("goudy old style",15)).place(x=50,y=140)
        self.txtDesc=Text(self.root,bg="lightyellow",font=("goudy old style",15))
        self.txtDesc.place(x=180,y=140,width=470,height=200)

        
        self.btnCheck=Button(self.root,text=self.func,command=self.check,fg="white",cursor="hand2",font=("goudy old style",20))
        self.btnCheck.place(x=500,y=100,width=150,height=27)
        

    def setData(self):
        self.varSupInvoice.set(obj.row[0])
        self.varName.set(obj.row[1])
        self.varContact.set(obj.row[2])
        self.txtDesc.delete('1.0',END)
        self.txtDesc.insert(END,obj.row[3])

    def check(self):
        if self.func == "Add":
            self.add()
        elif self.func == "Update":
            self.update()
        elif self.func == "Delete":
            self.delete()
        supplierClass.show(obj)

    #===add function===
    def add(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from supplier where invoice={self.varSupInvoice.get()}")
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice no. already assigned, try different",parent=self.root)
                else:
                    values=f'"{self.varSupInvoice.get()}","{self.varName.get()}","{self.varContact.get()}","{self.txtDesc.get("1.0",END)}"'
                    cur.execute(f"Insert into supplier(invoice,name,contact,desc) values({values})")
                    con.commit()
                    messagebox.showinfo("Success","Supplier Added Successfull",parent=self.root)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        

    #===update function===
    def update(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from supplier where Invoice={self.varSupInvoice.get()}")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
                else:
                    cur.execute(f"Update supplier set name='{self.varName.get()}',contact='{self.varContact.get()}',desc='{self.txtDesc.get(1.0,END)}' where invoice='{self.varSupInvoice.get()}'")
                    con.commit()
                    messagebox.showinfo("Success","Supplier updated Successfull",parent=self.root)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        
    #===delete function===
    def delete(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSupInvoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be entered",parent=self.root)
            else:
                cur.execute(f"Select * from supplier where Invoice='{self.varSupInvoice.get()}'")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Invoice no.",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op:
                        cur.execute(f"Delete from supplier where Invoice={self.varSupInvoice.get()}")
                        con.commit()
                        messagebox.showinfo("Success","supplier deleted Successfull",parent=self.root)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        


if __name__=="__main__":
    root=Tk()
    obj=supplierClass(root)
    root.mainloop()