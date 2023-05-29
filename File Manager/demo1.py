import tkinter as tk
from tkinter import filedialog
import os
import shutil
import mysql.connector
import tkinter.messagebox as messagebox
import datetime
from tkinter import ttk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# Configure the MySQL connection details
host = 'localhost'
user = 'root'
password = 'managerjd'
database = 'file_manager_db'

def get_connection():
    return mysql.connector.connect( host=host, user=user, password=password, database=database)

def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    create_table_query = """ CREATE TABLE IF NOT EXISTS files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        filename VARCHAR(255) NOT NULL,
        path VARCHAR(255) NOT NULL,
        CreateDateTime DATETIME 
    )
    """
    cursor.execute(create_table_query)
    connection.commit()

    cursor.close()
    connection.close()

def insert_file(filename, path, CreateDateTime):
    connection = get_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO files (filename, path, CreateDateTime) VALUES (%s, %s, %s)"
    values = (filename, path, CreateDateTime)
    cursor.execute(insert_query, values)
    connection.commit()

    cursor.close()
    connection.close()


def delete_files(filename):
    connection = get_connection()
    cursor = connection.cursor()

    delete_query = "DELETE FROM files WHERE filename = %s"
    values = (filename,)
    cursor.execute(delete_query, values)
    connection.commit()

    cursor.close()
    connection.close()

def display_message(title,message):
    messagebox.showinfo(title,message)

"""def create_directory():
    dir_path = filedialog.askdirectory()
    directory_name = directory_entry.get()
    
    if dir_path:
        directory_path = os.path.join(dir_path,directory_name)
        try:
            os.mkdir(directory_path)
            display_message("Success","Directory successfully created")
            #os.makedirs(directory_name,exist_ok=True)
            #directory_path = os.path.abspath(directory_name)
        except OSError:
            display_message("Failed","Failed to create directory")
        createDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_file(directory_name, directory_path, createDateTime)  # Insert directory into the database
        
    else:
        display_message("Creation cancelled","Cancelled")
        

def create_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    file_name = os.path.basename(file_path)
    if file_path:
        try:
            with open(file_path, 'w') as file:
                pass  # Create an empty file
            display_message("Success","File created successfully.")
            createDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_file(file_name, file_path, createDateTime)
        except IOError:
            display_message("Error occurred while creating the file.")
    else:
        display_message("No file path specified.")"""
        
import stat

# ...

# Create Directory
def create_directory():
    dir_path = filedialog.askdirectory()
    directory_name = directory_entry.get()
    permissions = permission_var.get()  # Get selected permissions
    
    if dir_path:
        directory_path = os.path.join(dir_path, directory_name)
        try:
            os.mkdir(directory_path)
            os.chmod(directory_path, permissions)  # Set permissions
            display_message("Success", "Directory successfully created")
            
            createDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_file(directory_name, directory_path, createDateTime)  # Insert directory into the database
        except OSError:
            display_message("Failed", "Failed to create directory")
    else:
        display_message("Creation cancelled", "Cancelled")

# Create File
def create_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    file_name = os.path.basename(file_path)
    permissions = permission_var.get()  # Get selected permissions
    
    if file_path:
        try:
            with open(file_path, 'w') as file:
                pass  # Create an empty file
            os.chmod(file_path, permissions)  # Set permissions
            display_message("Success", "File created successfully.")
            
            createDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_file(file_name, file_path, createDateTime)
        except IOError:
            display_message("Error occurred while creating the file.")
    else:
        display_message("No file path specified.")

# ...



def move_file():
    source_path = source_entry.get()
    destination_path = destination_entry.get()
    shutil.move(source_path, destination_path)
    display_message("Success","File moved successfully!")
    
def delete_file():
    file_path = file_entry.get()
    
    confirm = messagebox.askyesno("Confirmation",f"Are you sure you want to delete the file: {file_path}?")
    
    if confirm:
        os.remove(file_path)
        file_name = os.path.basename(file_path)
        delete_files(file_name)  # Delete file from the database
        display_message("Success","File Deleted Successfully")
    else:
        display_message("Cancelled","File Deletion Cancelled")
        


#FileDialog for selecting Source and Destination to move the file
def browse_source():
    source_path = filedialog.askopenfilename()
    source_entry.delete(0, tk.END)
    source_entry.insert(tk.END, source_path)

def browse_destination():
    destination_path = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(tk.END, destination_path)

#FileDialog for deleting a file
def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(tk.END, file_path)
    


    
#Accessing current Directory details
def open_directory_window():
    connection = get_connection()
    cursor = connection.cursor()

    select_query = "SELECT * FROM files"
    cursor.execute(select_query)
    directories = cursor.fetchall()

    cursor.close()
    connection.close()

    directory_window = tk.Toplevel(root)   #Create window on top of the current one
    directory_window.title("Present Directories")

    tree = ttk.Treeview(directory_window, columns=("ID", "Name", "Path", "Creation Date"))
    tree.heading("ID",text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Path", text="Path")
    tree.heading("Creation Date", text="Creation Date")

    for directory in directories:
        tree.insert("",tk.END, values=directory[0:])

    tree.pack()
    
#Accessing any Directory details
def display_directory_details():
    # Prompt user to select a directory
    directory_path = filedialog.askdirectory()

    if directory_path:
        # Create a new window
        details_window = tk.Toplevel(root)
        details_window.title("File Details")

        # Create a Treeview widget to display the file details in a table format
        treeview = ttk.Treeview(details_window)
        treeview['columns'] = ('Name', 'Size')
        treeview.heading('#0', text='File Path')
        treeview.heading('Name', text='File Name')
        treeview.heading('Size', text='File Size (bytes)')
        treeview.pack(fill='both', expand=True)

        # Get a list of all files in the directory
        file_list = os.listdir(directory_path)

        # Display the details of each file in the Treeview widget
        for file_name in file_list:
            file_path = os.path.join(directory_path, file_name)
            file_size = os.path.getsize(file_path)
            treeview.insert('', 'end', text=file_path, values=(file_name, file_size))

    else:
        display_message("No Directory Selected", "Please select a directory.")

root = tk.Tk()
root.title("File Manager")
root.configure(bg="#f8f8f8")
# Selecting Shadow Color for the buttons
btn_shadow = "#005cbf"

#Header
header_label = tk.Label(root,text="File Manager",bg="blue", fg="white", font=("Helvetica", 16, "bold"))
header_label.pack(fill = tk.X)


# Directory Creation
directory_label = tk.Label(root, text="Create Directory:",bg="#f8f8f8",fg="#000000")
directory_label.pack()

directory_frame = tk.Frame(root,bg="#f8f8f8")
directory_frame.pack()

directory_entry = tk.Entry(directory_frame)
directory_entry.pack(side=tk.LEFT)

directory_button = tk.Button(directory_frame, text="Create", command=create_directory,bg="#007bff",fg="#ffffff")
directory_button.pack(side=tk.LEFT)
directory_button.configure(highlightbackground=btn_shadow, highlightcolor=btn_shadow)

# File Permissions
permission_frame = tk.Frame(root, bg="#f8f8f8")
permission_frame.pack(pady=10)

permission_label = tk.Label(permission_frame, text="Permissions:", bg="#f8f8f8")
permission_label.pack(side=tk.LEFT)

permission_var = tk.IntVar()
permission_checkbuttons = []

# Permission Checkbuttons
read_checkbutton = tk.Checkbutton(permission_frame, text="Read", variable=permission_var, onvalue=stat.S_IREAD, offvalue=0)
read_checkbutton.pack(side=tk.LEFT)
permission_checkbuttons.append(read_checkbutton)

write_checkbutton = tk.Checkbutton(permission_frame, text="Write", variable=permission_var, onvalue=stat.S_IWRITE, offvalue=0)
write_checkbutton.pack(side=tk.LEFT)
permission_checkbuttons.append(write_checkbutton)

execute_checkbutton = tk.Checkbutton(permission_frame, text="Execute", variable=permission_var, onvalue=stat.S_IEXEC, offvalue=0)
execute_checkbutton.pack(side=tk.LEFT)
permission_checkbuttons.append(execute_checkbutton)

#Creating an empty file
file_label = tk.Label(root, text="Create a File:",bg="#f8f8f8",fg="#000000")
file_label.pack(pady=20)
             
create_file_button = tk.Button(root, text="Create File", command=create_file,bg="#007bff",fg="#ffffff")
create_file_button.pack()

from cryptography.fernet import Fernet

# ...

# Encryption and Decryption
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(file_path, 'wb') as file:
        file.write(encrypted_data)



# ...

# Encrypt File
def encrypt_selected_file():
    file_path = filedialog.askopenfilename()

    if file_path:
        key = Fernet.generate_key()
        encrypt_file(file_path, key)
        display_message("Success", "File encrypted successfully.")
    else:
        display_message("No file selected.", "Please select a file to encrypt.")


# ...

# Encrypt Button
encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_selected_file, bg="#007bff", fg="#ffffff")
encrypt_button.pack()




# File Movement
move_label = tk.Label(root, text="Move File:",bg="#f8f8f8")
move_label.pack(pady=25)

source_frame = tk.Frame(root,bg="#f8f8f8")
source_frame.pack()

source_entry = tk.Entry(source_frame)
source_entry.pack(pady=10,side=tk.LEFT)

source_button = tk.Button(source_frame, text="Browse Source", command=browse_source,bg="#007bff",fg="#ffffff")
source_button.pack(padx=25,side=tk.LEFT)
source_button.configure(highlightbackground=btn_shadow, highlightcolor=btn_shadow)

destination_frame = tk.Frame(root,bg="#f8f8f8")
destination_frame.pack()

destination_entry = tk.Entry(destination_frame)
destination_entry.pack(side=tk.LEFT)

destination_button = tk.Button(destination_frame, text="Browse Destination", command=browse_destination,bg="#007bff",fg="#ffffff")
destination_button.pack(padx=13,side=tk.LEFT)
destination_button.configure(highlightbackground=btn_shadow, highlightcolor=btn_shadow)

move_button = tk.Button(root, text="Move", command=move_file,bg="#007bff",fg="#ffffff")
move_button.pack(pady=25)
move_button.configure(highlightbackground=btn_shadow, highlightcolor=btn_shadow)

# File Deletion
delete_label = tk.Label(root, text="Delete File:",bg="#f8f8f8")
delete_label.pack(pady=10)

file_frame = tk.Frame(root,bg="#f8f8f8")
file_frame.pack()

file_entry = tk.Entry(file_frame)
file_entry.pack(side=tk.LEFT)

file_button = tk.Button(file_frame, text="Browse", command=browse_file,bg="#007bff",fg="#ffffff")
file_button.pack(side=tk.LEFT)
file_button.configure(highlightbackground=btn_shadow, highlightcolor=btn_shadow)

delete_button = tk.Button(root, text="Delete", command=delete_file,bg="#007bff",fg="#ffffff")
delete_button.pack(pady=20)
delete_button.configure(highlightbackground=btn_shadow, highlightcolor=btn_shadow)



# Create the button for opening the directory window
directory_button = tk.Button(root, text="Directory and File History", command=open_directory_window,bg="#007bff",fg="#ffffff")
directory_button.pack(padx=200, side=tk.LEFT)
directory_button.configure(highlightbackground=btn_shadow, highlightcolor=btn_shadow)

# Button to access directory and display details
details_button = tk.Button(root, text="Access Directory", command=display_directory_details,bg="#007bff",fg="#ffffff")
details_button.pack(padx=200,side=tk.RIGHT)
details_button.configure(highlightbackground=btn_shadow, highlightcolor=btn_shadow)

# Create the database table
create_table()

root.mainloop()