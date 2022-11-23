from os import startfile
from subprocess import call
import sqlite3
import tempfile
import time
from tkinter import *
from functions import openImage
from tkinter import ttk,messagebox
class billClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+10+10")
        self.root.title("Shop Management System Project")
        self.root.config(bg="white")
        self.root.iconbitmap("img/icon.ico")

        #===variables====
        self.varSearch=StringVar()
        self.varCName=StringVar()
        self.varCContact=StringVar()
        self.varPName=StringVar()
        self.varPId=StringVar()
        self.varPQuantity=StringVar()
        self.varPPrice=StringVar()
        self.varPStatus=StringVar()
        self.varPStock=StringVar()
        self.varCalculatorInput=StringVar()
        self.cartItems=0
        self.billAmount=0
        self.netPay=0
        self.discount=0
        self.billPresent=0
  

        #====Header=====
        self.headerIcon=openImage("img/cart.png",50,50)
        header=Label(self.root,text="Shop Management System",image=self.headerIcon,compound=LEFT,font="None 30 bold",bg="blue",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #===logout btn===
        btnLogout=Button(self.root,text="Logout",command=self.logout,bg="yellow",cursor="hand2",font="None 20 bold").place(x=1150,y=15,width=150,height=40)

        #===clock===
        self.lblClock=Label(self.root,text="Welcome to Shop Management System\t\tDate: mmm:dd,yy\t\tTime: hh:mm:ss",font="None 15",bg="grey",fg="white")
        self.lblClock.place(x=0,y=70,relwidth=1,height=30)

        #===Product Frame===
        productFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        productFrame.place(x=10,y=110,width=410,height=550)

        pTitle=Label(productFrame,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        
        #===search Frame===
        searchFrame=Frame(productFrame,bd=4,relief=RIDGE,bg="white")
        searchFrame.place(x=2,y=40,width=398,height=90)

        lblSearch=Label(searchFrame,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lblName=Label(searchFrame,text="Product Name ",font=("times new roman",13,"bold"),bg="white",fg="green").place(x=2,y=45)

        txtSearch=Entry(searchFrame,textvariable=self.varSearch,bg="lightyellow",font=("goudy old style",15)).place(x=125,y=47,width=150,height=22)

        btnSearch=Button(searchFrame,text="Search",command=self.search,bd=3,bg="#2196f3",fg="white",cursor="hand2",font=("goudy old style",15,"bold")).place(x=280,y=45,width=100,height=25)

        btnShowAll=Button(searchFrame,text="Show All",command=self.show,bd=3,bg="#184a45",fg="white",cursor="hand2",font=("goudy old style",15,"bold")).place(x=280,y=10,width=100,height=25)


        #====Product Details===
        productDetailFrame=Frame(productFrame,bd=3,relief=RIDGE)
        productDetailFrame.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(productDetailFrame,orient=VERTICAL)
        scrollx=Scrollbar(productDetailFrame,orient=HORIZONTAL)

        self.productTable=ttk.Treeview(productDetailFrame,columns=("pid","name","price","quantity","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("pid",text="PID")
        self.productTable.heading("name",text="Name")
        self.productTable.heading("price",text="Price")
        self.productTable.heading("quantity",text="Qty")
        self.productTable.heading("status",text="Status")

        self.productTable["show"]="headings"

        self.productTable.column("pid",width=40)
        self.productTable.column("name",width=90)
        self.productTable.column("price",width=70)
        self.productTable.column("quantity",width=40)
        self.productTable.column("status",width=90)
        self.productTable.bind("<ButtonRelease-1>",self.getData)

        self.productTable.pack(fill=BOTH,expand=1)

        lblNote=Label(productFrame,text="Note: 'Enter 0 Quantity to remove product from cart'",font=("goudy old style",13,"bold"),bg="white",fg="red").pack(side=BOTTOM,fill=X)

        #===Customer Frame===
        customerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        customerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(customerFrame,text="Customer Details",font=("goudy old style",15),bg="lightgrey").pack(side=TOP,fill=X)
        
        lblName=Label(customerFrame,text="Name ",font=("times new roman",13),bg="white").place(x=5,y=35)
        txtName=Entry(customerFrame,textvariable=self.varCName,bg="lightyellow",font=("goudy old style",13)).place(x=60,y=35,width=170)
        
        lblContact=Label(customerFrame,text="Contact no. ",font=("times new roman",13),bg="white").place(x=250,y=35)
        txtContact=Entry(customerFrame,textvariable=self.varCContact,bg="lightyellow",font=("goudy old style",13)).place(x=340,y=35,width=170)

        #===Calculator and cart Frame===
        calculatorCartFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        calculatorCartFrame.place(x=420,y=190,width=530,height=360)

        #===Calculator Frame===
        calculatorFrame=Frame(calculatorCartFrame,bd=8,relief=RIDGE,bg="white")
        calculatorFrame.place(x=5,y=10,width=268,height=340)
        
        txtCalculatorInput=Entry(calculatorFrame,textvariable=self.varCalculatorInput,font=("arial",15,"bold"),bd=10,relief=GROOVE,state="readonly",justify="right").grid(row=0,columnspan=4)
        #==r1==
        btn7=Button(calculatorFrame,command=lambda:self.getInput("7"),text="7",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=1,column=0)
        btn8=Button(calculatorFrame,command=lambda:self.getInput("8"),text="8",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=1,column=1)
        btn9=Button(calculatorFrame,command=lambda:self.getInput("9"),text="9",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=1,column=2)
        btnSum=Button(calculatorFrame,command=lambda:self.getInput("+"),text="+",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=1,column=3)
        #==r2==
        btn4=Button(calculatorFrame,command=lambda:self.getInput("4"),text="4",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=2,column=0)
        btn5=Button(calculatorFrame,command=lambda:self.getInput("5"),text="5",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=2,column=1)
        btn6=Button(calculatorFrame,command=lambda:self.getInput("6"),text="6",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=2,column=2)
        btnSub=Button(calculatorFrame,command=lambda:self.getInput("-"),text="-",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=2,column=3)
        #==r3==
        btn1=Button(calculatorFrame,command=lambda:self.getInput("1"),text="1",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=3,column=0)
        btn2=Button(calculatorFrame,command=lambda:self.getInput("2"),text="2",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=3,column=1)
        btn3=Button(calculatorFrame,command=lambda:self.getInput("3"),text="3",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=3,column=2)
        btnMul=Button(calculatorFrame,command=lambda:self.getInput("*"),text="*",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=3,column=3)
        #==r4==
        btn0=Button(calculatorFrame,command=lambda:self.getInput("0"),text="0",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        btnC=Button(calculatorFrame,command=self.clearCalculator,text="C",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        btnEqual=Button(calculatorFrame,command=self.performCalculation,text="=",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        btnDiv=Button(calculatorFrame,command=lambda:self.getInput("/"),text="/",font=("arial",15,"bold"),width=4,pady=15,cursor="hand2").grid(row=4,column=3)


        #====cart Details===
        cartFrame=Frame(calculatorCartFrame,bd=4,relief=RIDGE,bg="white")
        cartFrame.place(x=280,y=10,width=240,height=342)

        self.cartTitle=Label(cartFrame,text="Cart \t Total Product: [0]",font=("goudy old style",15),bg="lightgrey")
        self.cartTitle.pack(side=TOP,fill=X)
        

        scrolly=Scrollbar(cartFrame,orient=VERTICAL)
        scrollx=Scrollbar(cartFrame,orient=HORIZONTAL)

        self.cartTable=ttk.Treeview(cartFrame,columns=("pid","name","price","quantity"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)

        self.cartTable.heading("pid",text="PID")
        self.cartTable.heading("name",text="Name")
        self.cartTable.heading("price",text="Price")
        self.cartTable.heading("quantity",text="Qty")
        # self.cartTable.heading("priceperitem",text="Price per item")

        self.cartTable["show"]="headings"

        self.cartTable.column("pid",width=35)
        self.cartTable.column("name",width=95)
        self.cartTable.column("price",width=45)
        self.cartTable.column("quantity",width=35)
        # self.cartTable.column("priceperitem",width=85)
        self.cartTable.bind("<ButtonRelease-1>",self.getCartData)

        self.cartTable.pack(fill=BOTH,expand=1)


        #===cart button===
        cartButtonFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        cartButtonFrame.place(x=420,y=550,width=530,height=110)

        lblPName=Label(cartButtonFrame,text="Product Name",font=("goudy old style",15),bg="white").place(x=5,y=5)
        txtPName=Entry(cartButtonFrame,textvariable=self.varPName,font=("goudy old style",15),bg="lightyellow",state="readonly").place(x=5,y=35,width=190,height=22)

        lblPPrice=Label(cartButtonFrame,text="Price per Qty",font=("goudy old style",15),bg="white").place(x=230,y=5)
        txtPPrice=Entry(cartButtonFrame,textvariable=self.varPPrice,font=("goudy old style",15),bg="lightyellow",state="readonly").place(x=230,y=35,width=150,height=22)

        lblPQuantity=Label(cartButtonFrame,text="Quantity",font=("goudy old style",15),bg="white").place(x=400,y=5)
        txtPQuanity=Entry(cartButtonFrame,textvariable=self.varPQuantity,font=("goudy old style",15),bg="lightyellow").place(x=400,y=35,width=110,height=22)

        self.lblPStock=Label(cartButtonFrame,text=f"In Stock [0]",font=("goudy old style",15),bg="white")
        self.lblPStock.place(x=5,y=70)
        
        btnClearCart=Button(cartButtonFrame,command=self.clear,text="Clear",bg="lightgrey",cursor="hand2",font=("times new roman",15, "bold")).place(x=180,y=70,width=150,height=30)
        
        btnAddCart=Button(cartButtonFrame,text="Add | Update",command=self.addUpdateCart,bg="orange",cursor="hand2",font=("times new roman",15, "bold")).place(x=340,y=70,width=160,height=30)


        #===billing area===
        billingAreaFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billingAreaFrame.place(x=952,y=110,width=390,height=410)

        bTitle=Label(billingAreaFrame,text="Customer Bill",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)

        scrolly=Scrollbar(billingAreaFrame,orient=VERTICAL)
        scrolly.pack(side="right",fill=Y)
        self.txtBillArea=Text(billingAreaFrame,yscrollcommand=scrolly.set,font=("goudy old style",10,"bold"))
        self.txtBillArea.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txtBillArea.yview)

        #===billing button===
        billingMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billingMenuFrame.place(x=952,y=520,width=390,height=140)

        self.lblAmount=Label(billingMenuFrame,text="Bill Amount(Rs.)\n[0]",font=("goudy old style",12,"bold"),bg="#3f51b5",fg="white")
        self.lblAmount.place(x=2,y=5,width=120,height=70)
        self.lblDiscount=Label(billingMenuFrame,text="Discount\n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lblDiscount.place(x=124,y=5,width=120,height=70)
        self.lblNetPay=Label(billingMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lblNetPay.place(x=246,y=5,width=130,height=70)


        btnPrint=Button(billingMenuFrame,cursor="hand2",command=self.printBill,text="Print",font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btnPrint.place(x=2,y=80,width=120,height=50)
        btnClearAll=Button(billingMenuFrame,command=self.clearAll,cursor="hand2",text="Clear All",font=("goudy old style",15,"bold"),bg="grey",fg="white")
        btnClearAll.place(x=124,y=80,width=120,height=50)
        btnGenerate=Button(billingMenuFrame,command=self.generateBill,cursor="hand2",text="Generate/Save Bill",font=("goudy old style",12,"bold"),bg="#009688",fg="white")
        btnGenerate.place(x=246,y=80,width=130,height=50)


        
        #===footer===
        lblFooter=Label(self.root,text="SMS-Shop Management System\n",font=("times new roman",11),bg="grey",fg="white",bd=0)
        lblFooter.pack(side=BOTTOM,fill=X)
        
        self.show()

#======Functions==============================================================================================================

    #===input in calculator screen====
    def getInput(self,num):
        xnum=self.varCalculatorInput.get()+str(num)
        self.varCalculatorInput.set(xnum)

    #===function to clear calculator screen===
    def clearCalculator(self):
        self.varCalculatorInput.set("")

    #===perform calculations===
    def performCalculation(self):
        self.varCalculatorInput.set(eval(self.varCalculatorInput.get()))

    #===show records in table===
    def show(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select pid,name,price,quantity,status from product where status='Active'")
            rows=cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert("",END,values=row)
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        finally:
            self.showCart()
            self.billUpdates()
            self.updateDateTime()


    #===search function===
    def search(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varSearch.get()=="":
                messagebox.showerror("Error",f"Search input should be required",parent=self.root)
            else:
                cur.execute(f"Select pid,name,price,quantity,status from product where name LIKE '%{self.varSearch.get()}%' and status='Active'")
                rows=cur.fetchall()
                if rows==0:
                    messagebox.showerror("Error","No Record Found",parent=self.root)
                else:
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
        self.varPName.set(row[1])
        self.varPPrice.set(row[2])
        self.varPStock.set(row[3])
        self.lblPStock.config(text=f"In Stock [{self.varPStock.get()}]")
        self.varPQuantity.set("1")

    def getCartData(self,ev):
        f=self.cartTable.focus()
        content=(self.cartTable.item(f))
        row=content['values']

        self.varPId.set(row[0])
        self.varPName.set(row[1])
        self.varPQuantity.set(row[3])

        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        cur.execute(f"Select price from product where pid='{self.varPId.get()}'")
        ppi=cur.fetchone()[0]
        self.varPPrice.set(ppi)
        cur.execute(f"Select quantity from product where pid='{self.varPId.get()}'")
        qty=cur.fetchone()[0]
        self.lblPStock.config(text=f"In Stock [{qty}]")

    #===add or update data function===
    def addUpdateCart(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            if self.varPId.get()=="":
                messagebox.showerror("Error","Select product from list",parent=self.root)
            elif self.varPQuantity.get()=="":
                messagebox.showerror("Error","Quantity is required",parent=self.root)
            elif self.varPQuantity.get()=="0":
                op=messagebox.askyesno("Confirm","Do you really want to remove this product from Cart?")
                if op:
                    cur.execute(f"Delete from cartList where pid={self.varPId.get()}")
                    con.commit()
                    messagebox.showinfo("Success","Product Removed Successfull",parent=self.root)
            elif int(self.varPQuantity.get())>int(self.varPStock.get()):
                messagebox.showerror("Error","Quantity is greater than stock",parent=self.root)
            else:
                priceCal=int(self.varPQuantity.get())*float(self.varPPrice.get())
                cur.execute(f"Select * from cartList where pid='{self.varPId.get()}'")
                row=cur.fetchone()
                if row!=None:
                    op=messagebox.askyesno("Confirm","Do you really want to Update?")
                    if op:
                        cur.execute(f"Update cartList set price='{priceCal}',quantity='{self.varPQuantity.get()}' where pid='{self.varPId.get()}'")
                        con.commit()
                        messagebox.showinfo("Success","Product Updated Successfull",parent=self.root)
                else:
                    values=f'"{self.varPId.get()}","{self.varPName.get()}","{priceCal}","{self.varPQuantity.get()}","{self.varPPrice.get()}"'
                    cur.execute(f"Insert into cartList(pid,name,price,quantity,priceperitem) values({values})")
                    con.commit()
                    messagebox.showinfo("Success","Product Added Successfull",parent=self.root)    
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        finally:
            self.showCart()
            self.billUpdates()
        
        
    def showCart(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select pid,name,price,quantity from cartList")
            rows=cur.fetchall()
            self.cartTable.delete(*self.cartTable.get_children())
            for row in rows:
                self.cartTable.insert("",END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def billUpdates(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            #==total items==
            #==bill amount==
            cur.execute("Select price,quantity from cartList")
            prices=cur.fetchall()
            for price in prices:
                self.cartItems+=int(price[1])
                self.billAmount+=float(price[0])

            #==net pay==
            self.discount=self.billAmount*5/100
            self.netPay=(self.billAmount-self.discount)

            #==update labels==
            self.lblAmount.config(text=f"Bill Amount(Rs.)\n[{str(self.billAmount)}]")
            self.lblNetPay.config(text=f"Net Pay(Rs.)\n[{str(self.netPay)}]")
            self.cartTitle.config(text=f"Cart \t Total Product: [{self.cartItems}]")


        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def generateBill(self):
        if self.varCName.get()=="" or self.varCContact.get()=="":
            messagebox.showerror("Error",f"Customer Details are required",parent=self.root)
        elif self.cartItems==0:
            messagebox.showerror("Error",f"Add products to the Cart first!!!",parent=self.root)
        else:
            #==Bill top==
            self.billTop()
            #==Bill middle==
            self.billMiddleTemplate()
            #==Bill bottom==
            self.billBottom()
            
            with open(f"bill/{str(self.invoice)}.txt","w") as fp:
                fp.write(self.txtBillArea.get("1.0",END))
            messagebox.showinfo("Saved","Bill has been generated")
            self.billPresent=1
            self.clearCart()
            self.showCart()
    
    #===Bill top===
    def billTop(self):
        self.invoice=int(time.strftime("%y%m%d"))+int(time.strftime("%H%M%S"))
        date_=time.strftime("%b %d,%Y")
        billTopTemplate=f"SMS-Shop Management System".center(45)+"\n"+f" Phone No. 808*****74".ljust(30)+f"Kharar - 140301".rjust(15)+"\n"+"="*45+"\n"+f" Customer Name: {self.varCName.get()}".ljust(45)+"\n"+f" Phone no.: {self.varCContact.get()}".ljust(45)+"\n"+f" Bill No. {self.invoice}".ljust(22)+f"Date:{date_}".rjust(23)+"\n"+"="*45+"\n Product Name".ljust(15)+"QTY".center(15)+" Price".ljust(15)+"\n"
    
        self.txtBillArea.delete("1.0",END)
        self.txtBillArea.insert("1.0",billTopTemplate)
    
    #===Bill middle===
    def billMiddleTemplate(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select name,quantity,price from cartList")
            rows=cur.fetchall()
            for row in rows:
                name=row[0]
                qty=row[1]
                price=row[2]
                self.txtBillArea.insert(END,f" {name}".ljust(15)+f"{qty}".center(15)+f"Rs.{price}".ljust(15)+"\n")
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    #===Bill bottom===
    def billBottom(self):
        billBottomTemplate="="*45+"\n Bill Amount".ljust(30)+f" Rs.{self.billAmount}".ljust(15)+"\n"+" Discount".ljust(30)+f"Rs.{self.discount}".ljust(15)+"\n"+" Net Pay".ljust(30)+f"Rs.{self.netPay}".ljust(15)+"\n"+"="*45
        self.txtBillArea.insert(END,billBottomTemplate)
        self.txtBillArea.config(state=DISABLED)
        #==update stock==
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("Select pid,quantity from cartList")
            items=cur.fetchall()
            cur.execute("Select pid,Quantity from product")
            stocks=cur.fetchall()
            for item in items:
                self.varPId.set(item[0])
                self.varPQuantity.set(item[1])
                for stock in stocks:
                    if int(self.varPId.get())==stock[0]:
                        self.varPStock.set(stock[1])
                        break
                if self.varPStock.get()==self.varPQuantity.get():
                    status="Inactive"
                else:
                    status="Active"
                cur.execute(f"Update product set Quantity='{int(self.varPStock.get())-int(self.varPQuantity.get())}',Status='{status}' where pid='{self.varPId.get()}'")
                con.commit()
        except Exception as e:
            messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
        self.show()
        

    def clear(self):
        self.varPId.set("")
        self.varPName.set("")
        self.varPPrice.set("")
        self.varPStock.set("")
        self.lblPStock.config(text=f"In Stock [0]")
        self.varPQuantity.set("")

    def clearCart(self):
        con=sqlite3.connect(database=r"sms.db")
        cur=con.cursor()
        try:
            cur.execute("DELETE FROM cartList;")
            con.commit()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
        


    def clearAll(self):
        self.clearCart()
        self.varCName.set("")
        self.varCContact.set("")
        self.txtBillArea.delete("1.0",END)
        self.varSearch.set("")
        self.billPresent=0
        self.clear()
        self.show()
        self.showCart()

    def updateDateTime(self):
        date_=time.strftime("%b %d, %Y")
        time_=time.strftime("%H:%M:%S")
        self.lblClock.config(text=f"Welcome to Shop Management Systemf\tDate: {date_}\t\tTime: {time_}")
        self.lblClock.after(1000,self.updateDateTime)

    def printBill(self):
        if self.billPresent:
            messagebox.showinfo("Print Bill","Wait while printing")
            newFile=tempfile.mktemp(".txt")
            with open(newFile,"w")as f:
                f.write(self.txtBillArea.get("1.0",END))
            startfile(newFile,"print")
        else:
            messagebox.showerror("Print Bill","Generate Bill to print receipt")

    def logout(self):
        self.root.destroy()
        call(["python", "SMS.py"])
        


if __name__=="__main__":
    root=Tk()
    obj=billClass(root)
    root.mainloop()