from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector


def dbFun():
    """Establish a connection to the database."""
    global con, cur
    con = mysql.connector.connect(host="localhost", user="root", passwd="Mohith@1315", database="rec")
    cur = con.cursor()


def clr(r, g, b):
    """Generate hex color codes."""
    return f"#{r:02x}{g:02x}{b:02x}"


def insertFun():
    book_name = name.get().strip()
    edition = options.get().strip()
    book_price = price.get().strip()
    quantity = quant.get().strip()

    # Debug: Check the value of edition
    

    if book_name and edition in ("First", "Second", "Third") and book_price.isdigit() and quantity.isdigit():
        try:
            price_val = int(book_price)
            quantity_val = int(quantity)

            dbFun()
            cur.execute("INSERT INTO books (name, edition, price, quant) VALUES (%s, %s, %s, %s)",
                        (book_name, edition, price_val, quantity_val))
            con.commit()

            messagebox.showinfo("Success", f"Book '{book_name}' of {edition} Edition has been added successfully!")
            name.delete(0, END)
            options.set("Select Edition")  # Reset combobox
            price.delete(0, END)
            quant.delete(0, END)
            showAllFun()
        except mysql.connector.Error as db_error:
            messagebox.showerror("Error", f"Database error: {db_error}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            if con.is_connected():
                con.close()
    else:
        if not book_name:
            messagebox.showwarning("Warning", "Please enter the book name!")
        elif edition == "Select Edition" or edition not in ("First", "Second", "Third"):
            messagebox.showwarning("Warning", "Please select a valid edition!")
        elif not book_price.isdigit():
            messagebox.showwarning("Warning", "Price should be a numeric value!")
        elif not quantity.isdigit():
            messagebox.showwarning("Warning", "Quantity should be a numeric value!")
        else:
            messagebox.showwarning("Warning", "Please fill in all the fields!")
def srchFun():
    """Search for a book in the database."""
    book_name = name2.get().strip()
    edition = options2.get().strip()

    try:
        dbFun()
        cur.execute("SELECT * FROM books WHERE name=%s AND edition=%s", (book_name, edition))
        row = cur.fetchone()
        if row:
            table.delete(*table.get_children())
            table.insert('', END, values=row)
        else:
            messagebox.showerror("Error", f"Book '{book_name}' or edition '{edition}' not found!")
        con.close()

    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")


def showAllFun():
    """Display all books in the database."""
    try:
        dbFun()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        table.delete(*table.get_children())
        for row in rows:
            table.insert('', END, values=row)
        con.close()

    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")


def purFun():
    """Purchase a book and update its quantity."""
    book_name = name2.get().strip()
    edition = options2.get().strip()

    try:
        dbFun()
        cur.execute("SELECT price, quant FROM books WHERE name=%s AND edition=%s", (book_name, edition))
        row = cur.fetchone()

        if row and row[1] > 0:
            new_quantity = row[1] - 1
            cur.execute("UPDATE books SET quant=%s WHERE name=%s AND edition=%s", (new_quantity, book_name, edition))
            con.commit()
            messagebox.showinfo("Success", f"Book '{book_name}' purchased for ${row[0]}!")
        else:
            messagebox.showwarning("Warning", f"Book '{book_name}' of edition '{edition}' is out of stock!")

        con.close()

    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")


def delFun():
    try:
        dbFun()
        indexing = table.focus()

        content = table.item(indexing)
        book_name = content['values'][0]
        edition = content['values'][1]
        query = 'DELETE FROM books WHERE name=%s AND edition=%s'
        cur.execute(query, (book_name, edition))
        con.commit()
        messagebox.showinfo("Success", f"Book '{book_name}' of edition '{edition}' has been deleted!")

        showAllFun()  # Refresh the table

    except Exception as e:
        messagebox.showerror("Error", f"Database error: {e}")


# Main Window
root = Tk()
root.title("Book Store Management")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f"{width}x{height}+0+0")

title = Label(root, text="Book Store Management", bd=4, relief="groove",
              bg="gray", fg="cyan", font=("Elephant", 45, "italic"))
title.pack(side="top", fill="x")

# Add Frame
addFrame = Frame(root, bd=5, relief="ridge", bg=clr(100, 150, 255))
addFrame.place(width=width / 3, height=height - 180, x=70, y=100)

nameLbl = Label(addFrame, text="Book Name:", bg=clr(100, 150, 255), font=("Arial", 15, "bold"))
nameLbl.grid(row=0, column=0, padx=20, pady=30)
name = Entry(addFrame, bd=2, width=18, font=("Arial", 15))
name.grid(row=0, column=1, padx=10, pady=30)

ediLbl = Label(addFrame, text="Edition:", bg=clr(100, 150, 255), font=("Arial", 15, "bold"))
ediLbl.grid(row=1, column=0, padx=20, pady=30)
options = ttk.Combobox(addFrame, width=16, font=("Arial", 15))
options['values'] = ("First", "Second", "Third")
options.set("Select Edition")
options.grid(row=1, column=1, padx=10, pady=30)

priceLbl = Label(addFrame, text="Price:", bg=clr(100, 150, 255), font=("Arial", 15, "bold"))
priceLbl.grid(row=2, column=0, padx=20, pady=30)
price = Entry(addFrame, bd=2, width=18, font=("Arial", 15))
price.grid(row=2, column=1, padx=10, pady=30)

quantLbl = Label(addFrame, text="Quantity:", bg=clr(100, 150, 255), font=("Arial", 15, "bold"))
quantLbl.grid(row=3, column=0, padx=20, pady=30)
quant = Entry(addFrame, bd=2, width=18, font=("Arial", 15))
quant.grid(row=3, column=1, padx=10, pady=30)

addBtn = Button(addFrame, text="Add Book", command=insertFun, width=20, bd=3, relief="raised", font=("Arial", 20, "bold"))
addBtn.grid(row=4, column=0, padx=20, pady=40, columnspan=2)

# Detail Frame
detFrame = Frame(root, bd=5, relief="ridge", bg=clr(150, 200, 100))
detFrame.place(width=width / 2, height=height - 180, x=width / 3 + 140, y=100)

nameLbl2 = Label(detFrame, text="Book Name:", bg=clr(150, 200, 100), font=("Arial", 15, "bold"))
nameLbl2.grid(row=0, column=0, padx=10, pady=20)
name2 = Entry(detFrame, bd=2, width=16, font=("Arial", 15))
name2.grid(row=0, column=1, padx=5, pady=20)

ediLbl2 = Label(detFrame, text="Edition:", bg=clr(150, 200, 100), font=("Arial", 15, "bold"))
ediLbl2.grid(row=0, column=2, padx=20, pady=30)
options2 = ttk.Combobox(detFrame, width=16, font=("Arial", 15))
options2['values'] = ("First", "Second", "Third")
options2.set("Select Edition")
options2.grid(row=0, column=3, padx=10, pady=30)

btnFrame = Frame(detFrame, bd=3, relief="ridge", bg=clr(140, 210, 120))
btnFrame.place(width=width / 2 - 20, height=70, x=8, y=60)

srchBtn = Button(btnFrame, text="Search", command=srchFun, width=10, bd=3, relief="raised", font=("Arial", 15, "bold"))
srchBtn.grid(row=0, column=0, padx=10, pady=10)

allBtn = Button(btnFrame, text="Show All", command=showAllFun, width=10, bd=3, relief="raised", font=("Arial", 15, "bold"))
allBtn.grid(row=0, column=1, padx=10, pady=10)

purBtn = Button(btnFrame, text="Purchase", command=purFun, width=10, bd=3, relief="raised", font=("Arial", 15, "bold"))
purBtn.grid(row=0, column=2, padx=10, pady=10)

delBtn = Button(btnFrame, text="Remove", command=delFun, width=10, bd=3, relief="raised", font=("Arial", 15, "bold"))
delBtn.grid(row=0, column=3, padx=10, pady=10)

# Table Frame
tabFrame = Frame(detFrame, bd=4, relief="sunken", bg="cyan")
tabFrame.place(width=width / 2 - 40, height=height - 350, x=17, y=150)

x_scroll = Scrollbar(tabFrame, orient="horizontal")
x_scroll.pack(side="bottom", fill="x")

y_scroll = Scrollbar(tabFrame, orient="vertical")
y_scroll.pack(side="right", fill="y")

table = ttk.Treeview(tabFrame, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set,
                     columns=("name", "edi", "price", "quant"))

x_scroll.config(command=table.xview)
y_scroll.config(command=table.yview)

table.heading("name", text="Book")
table.heading("edi", text="Edition")
table.heading("price", text="Price")
table.heading("quant", text="Quantity")
table["show"] = "headings"
table.pack(fill="both", expand=1)

root.mainloop()
