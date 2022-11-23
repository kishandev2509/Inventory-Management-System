import sqlite3
from tkinter import messagebox, ttk
from tkinter import *
class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+230+140")
        self.root.title("Shop Management System Project")
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.iconbitmap("img/icon.ico")

        #===variables===
        self.varCategory=StringVar()
        self.varCategoryList=["Select"]
        self.varName=StringVar()
        self.varSupplier=StringVar()
        self.varSupplierList=["Select"]
        self.varPrice=StringVar()
        self.varQuantity=StringVar()
        self.varStatus=StringVar()
        self.varPId=StringVar()


        self.varSearchBy=StringVar()
        self.varSearchTxt=StringVar()
        
        self.fetchCategorySupplier()

        #====Manage Product Details===
        manageProductFrame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        manageProductFrame.place(x=10,y=10,width=450,height=480)

        
        #===title===
        title=Label(manageProductFrame,text="Manage Product Details",bg="#0f4d7d",fg="white",font=("goudy old style",20)).pack(side=TOP,fill=X)

        #===column 1====
        lblCategory=Label(manageProductFrame,text="Category",bg="white",font=("goudy old style",20)).place(x=30,y=60)
        lblSupplier=Label(manageProductFrame,text="Supplier",bg="white",font=("goudy old style",20)).place(x=30,y=110)
        lblProductName=Label(manageProductFrame,text="Name",bg="white",font=("goudy old style",20)).place(x=30,y=160)
        lblPrice=Label(manageProductFrame,text="Price",bg="white",font=("goudy old style",20)).place(x=30,y=210)
        lblQuantity=Label(manageProductFrame,text="Quantity",bg="white",font=("goudy old style",20)).place(x=30,y=260)
        lblStatus=Label(manageProductFrame,text="Status",bg="white",font=("goudy old style",20)).place(x=30,y=310)


        #===column 1====
        cmbCat=ttk.Combobox(manageProductFrame,textvariable=self.varCategory,values=(self.varCategoryList),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbCat.place(x=150,y=60,width=200)
        cmbCat.current(0)
        
        cmbSupplier=ttk.Combobox(manageProductFrame,textvariable=self.varSupplier,values=(self.varSupplierList),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbSupplier.place(x=150,y=110,width=200)
        cmbSupplier.current(0)

        txtName=Entry(manageProductFrame,textvariable=self.varName,bg="lightyellow",font=("goudy old style",15)).place(x=150,y=160,width=200)

        txtPrice=Entry(manageProductFrame,textvariable=self.varPrice,bg="lightyellow",font=("goudy old style",15)).place(x=150,y=210,width=200)

        txtQuantity=Entry(manageProductFrame,textvariable=self.varQuantity,bg="lightyellow",font=("goudy old style",15)).place(x=150,y=260,width=200)

        cmbStatus=ttk.Combobox(manageProductFrame,textvariable=self.varStatus,values=("Active","Inactive"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbStatus.place(x=150,y=310,width=200)
        cmbStatus.current(0)


        #===buttons===
        btnAdd=Button(manageProductFrame,text="Add",command=self.add,bg="#2196f3",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=10,y=400,width=100,height=40)

        btnUpdate=Button(manageProductFrame,text="Update",command=self.update,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=120,y=400,width=100,height=40)
        
        btnDelete=Button(manageProductFrame,text="Delete",command=self.delete,bg="#f44336",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=230,y=400,width=100,height=40)
        
        btnClear=Button(manageProductFrame,text="Clear",command=self.clear,bg="#607d8b",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=340,y=400,width=100,height=40)
  
        #===search frame===
        searchFrame=LabelFrame(self.root,text="Search Product",bd=2,relief=RIDGE,font=("goudy old style",12,"bold"),bg="white")
        searchFrame.place(x=480,y=10,width=600,height=80)

        #===otions===
        cmbCat=ttk.Combobox(searchFrame,textvariable=self.varSearchBy,values=("Category","Supplier","Name"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbCat.place(x=10,y=10,width=180)
        cmbCat.current(0)

        txtSearch=Entry(searchFrame,textvariable=self.varSearchTxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)

        btnSearch=Button(searchFrame,text="Search",command=self.search,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=410,y=9,width=150,height=30)




        #====Product Details===
        productFrame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        productFrame.place(x=480,y=100,width=600,height=390)
        
        scrolly=Scrollbar(productFrame,orient=VERTICAL)
        scrollx=Scrollbar(productFrame,orient=HORIZONTAL)

        self.productTable=ttk.Treeview(productFrame,columns=("pid","Category","Supplier","Name","Price","Quantity","Status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)
        self.productTable.heading("pid",text="P ID")
        self.productTable.heading("Category",text="Category")
        self.productTable.heading("Supplier",text="Supplier")
        self.productTable.heading("Name",text="Name")
        self.productTable.heading("Price",text="Price")
        self.productTable.heading("Quantity",text="Quantity")
        self.productTable.heading("Status",text="Status")

        self.productTable["show"]="headings"

        self.productTable.column("pid",width=90)
        self.productTable.column("Category",width=90)
        self.productTable.column("Supplier",width=90)
        self.productTable.column("Name",width=90)
        self.productTable.column("Price",width=90)
        self.productTable.column("Quantity",width=90)
        self.productTable.column("Status",width=90)

        self.productTable.bind("<ButtonRelease-1>",self.getData)

        self.productTable.pack(fill=BOTH,expand=1)

        self.show()

#========================================================================================
    #===function to categories and suppleirs===
    def fetchCategorySupplier(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            categories=cur.fetchall()
            for category in categories:
                self.varCategoryList.append(category[0])

            cur.execute("Select name from supplier")
            suppliers=cur.fetchall()
            for supplier in suppliers:
                self.varSupplierList.append(supplier[0])

        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)


    
    
    #===show records in table===
    def show(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select * from product")
            rows=cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)

    #===insert selected row data in text feilds===
    def getData(self,ev):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']

        self.varPId.set(row[0])
        self.varCategory.set(row[1])
        self.varSupplier.set(row[2])
        self.varName.set(row[3])
        self.varPrice.set(row[4])
        self.varQuantity.set(row[5])
        self.varStatus.set(row[6])

    #===add function===
    def add(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varCategory.get()=="Select" or self.varSupplier.get()=="Select":
                messagebox.showerror("Error","All fields are required",parent=self.root)
            else:
                cur.execute(f"Select * from product where Name='{self.varName.get()}'")
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Product already added, try different",parent=self.root)
                else:
                    values=f'"{self.varCategory.get()}","{self.varSupplier.get()}","{self.varName.get()}","{self.varPrice.get()}","{self.varQuantity.get()}","{self.varStatus.get()}"'
                    # print(values)
                    cur.execute(f"Insert into product(Category,Supplier,Name,Price,Quantity,Status) values({values})")
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfull",parent=self.root)
                    self.show()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        

    #===update function===
    def update(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varPId.get()=="":
                messagebox.showerror("Error","Select product from list",parent=self.root)
            else:
                cur.execute(f"Select * from product where pid={self.varPId.get()}")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute(f"Update product set Category='{self.varCategory.get()}',Supplier='{self.varSupplier.get()}',Name='{self.varName.get()}',Price='{self.varPrice.get()}',Quantity='{self.varQuantity.get()}',Status='{self.varStatus.get()}' where pid='{self.varPId.get()}'")
                    con.commit()
                    messagebox.showinfo("Success","Product updated Successfull",parent=self.root)
                    self.show()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        

    #===delete function===
    def delete(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varPId.get()=="":
                messagebox.showerror("Error","Select product from list",parent=self.root)
            else:
                cur.execute(f"Select * from product where pid='{self.varPId.get()}'")
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?")
                    if op:
                        cur.execute(f"Delete from product where pid={self.varPId.get()}")
                        con.commit()
                        messagebox.showinfo("Success","Product deleted Successfull",parent=self.root)
                        self.clear()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        

    #===clear function===
    def clear(self):
        f=self.productTable.focus()
        content=(self.productTable.item(f))
        row=content['values']

        self.varCategory.set("Select")
        self.varSupplier.set("Select")
        self.varName.set("")
        self.varPrice.set("")
        self.varQuantity.set("")
        self.varStatus.set("Active")
        self.varPId.set("")
        self.show()

    #===search function===
    def search(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSearchTxt.get()=="":
                self.clear()
            else:
                self.clear()
                cur.execute(f"Select * from product where {self.varSearchBy.get()} LIKE '%{self.varSearchTxt.get()}%'")
                rows=cur.fetchall()
                if rows==0:
                    messagebox.showerror("Error","No Record Found",parent=self.root)
                else:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)




if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()