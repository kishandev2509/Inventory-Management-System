import sqlite3
from tkinter import messagebox, ttk
from tkinter import *

class basicWindow():
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+230+140")
        self.root.title("Inventory Management System Project")
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

class productClass(basicWindow):
    def __init__(self, root):
        super().__init__(root)
        self.row = False

        self.varSearchBy=StringVar()
        self.varSearchTxt=StringVar()
        

        #===buttons===

        frameBtns=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        frameBtns.place(x=630,y=20,width=450)

        btnAdd=Button(frameBtns,text="Add",command=self.add,bg="#2196f3",fg="white",cursor="hand2",font=("goudy old style",20))
        btnAdd.pack(side=LEFT, padx=10,pady=4)
        # .place(x=10,y=400,width=100,height=40)

        btnUpdate=Button(frameBtns,text="Update",command=self.update,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",20))
        btnUpdate.pack(side=LEFT, padx=10,pady=4)
        # .place(x=120,y=400,width=100,height=40)
        
        btnDelete=Button(frameBtns,text="Delete",command=self.delete,bg="#f44336",fg="white",cursor="hand2",font=("goudy old style",20))
        btnDelete.pack(side=LEFT, padx=10,pady=4)
        # .place(x=230,y=400,width=100,height=40)
        
        btnViewAll=Button(frameBtns,text="View All",command=self.show,bg="#607d8b",fg="white",cursor="hand2",font=("goudy old style",20))
        btnViewAll.pack(side=LEFT, padx=10,pady=4)
        # .place(x=340,y=400,width=100,height=40)
  
        #===search frame===
        searchFrame=LabelFrame(self.root,text="Search Product",bd=2,relief=RIDGE,font=("goudy old style",12,"bold"),bg="white")
        searchFrame.place(x=20,y=10,width=600,height=80)

        #===otions===
        cmbCat=ttk.Combobox(searchFrame,textvariable=self.varSearchBy,values=("Category","Supplier","Name"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmbCat.place(x=10,y=10,width=180)
        cmbCat.current(0)

        txtSearch=Entry(searchFrame,textvariable=self.varSearchTxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)

        btnSearch=Button(searchFrame,text="Search",command=self.search,bg="#4caf50",fg="white",cursor="hand2",font=("goudy old style",20)).place(x=410,y=9,width=150,height=30)




        #====Product Details===
        productFrame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        productFrame.place(x=20,y=100,width=1060,height=390)
        
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
        self.row=content['values']

    def add(self):
        adddetails = Toplevel(self.root)
        self.productDetail = productDetails(adddetails,"Add")
        self.productDetail.btnCheck.configure(background="#2196f3")

    def update(self):
        if self.row:
            adddetails = Toplevel(self.root)
            self.productDetail = productDetails(adddetails,"Update")
            productDetails.setData(self.productDetail)
            self.productDetail.btnCheck.configure(bg="#4caf50")
        else:
            messagebox.showerror("Error",f"Select a product first",parent=self.root)

    def delete(self):
        if self.row:
            adddetails = Toplevel(self.root)
            self.productDetail = productDetails(adddetails,"Delete")
            productDetails.setData(self.productDetail)
            self.productDetail.btnCheck.configure(bg="#f44336")
        else:
            messagebox.showerror("Error",f"Select a product first",parent=self.root)

    #===search function===
    def search(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSearchTxt.get()=="":
                messagebox.showinfo("Error",f"Enter {self.varSearchBy.get()} to search",parent=self.root)
            else:
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



class productDetails(basicWindow):
    def __init__(self, root, func):
        super().__init__(root)
        self.root.geometry("480x500+540+140")
        self.func = func

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

        self.btnCheck=Button(manageProductFrame,text=self.func,command=self.check,fg="white",cursor="hand2",font=("goudy old style",20))
        self.btnCheck.place(x=200,y=400,width=150,height=27)

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

    def check(self):
        if self.func == "Add":
            self.add()
        elif self.func == "Update":
            self.update()
        elif self.func == "Delete":
            self.delete()
        productClass.show(self=obj)

    def setData(self):
        self.varPId.set(obj.row[0])
        self.varCategory.set(obj.row[1])
        self.varSupplier.set(obj.row[2])
        self.varName.set(obj.row[3])
        self.varPrice.set(obj.row[4])
        self.varQuantity.set(obj.row[5])
        self.varStatus.set(obj.row[6])

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
            self.root.destroy()
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
            self.root.destroy()
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
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op:
                        cur.execute(f"Delete from product where pid={self.varPId.get()}")
                        con.commit()
                        messagebox.showinfo("Success","Product deleted Successfull",parent=self.root)
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)



if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()