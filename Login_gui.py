from tkinter import *
from PIL import ImageTk, Image


class Login(Tk):
    def __init__(self):
        super().__init__()
            
        self.login_info=[]

        # create window
        self.title('Dumbscord')
        self.geometry('500x400')
        self.resizable(False,False)
        self.iconbitmap("pngegg1.ico")

        # create top and bottom main frames
        self.top_frame = Frame(self,bg="#34495e",width=500,height=100)
        self.bottom_frame = Frame(self, bg="#34495e",width=500,height=300)
        self.top_frame.grid_propagate(False)
        self.top_frame.grid(sticky="ew")
        self.bottom_frame.grid_propagate(False)
        self.bottom_frame.grid(sticky="ew")
        
        # create main frame
        self.image_path = Image.open("white_pngegg1.png")
        self.image = ImageTk.PhotoImage(self.image_path)
        self.title_image = Label(self.top_frame, image=self.image,bg="#34495e")
        self.title_text = Label(self.top_frame,text="DUMBSCORD",bg="#34495e",fg="#ffffff", font=("times",25))
        self.title_image.place(x=120,y=25)
        self.title_text.place(x=165,y=25)

        # create input fields
        self.address_label = Label(self.bottom_frame,text="IP Address",bg="#34495e",fg="#ffffff")
        self.address_label.grid(row=0,column=0,padx=(130,10),pady=(20,5))
        self.address_entry = Entry(self.bottom_frame,bg="#5d6d7e",fg="#ffffff")
        self.address_entry.grid(row=0, column=1,padx=(10,150),pady=(20,5))

        self.port_label = Label(self.bottom_frame,text="Port Number",bg="#34495e",fg="#ffffff")
        self.port_label.grid(row=1,column=0,padx=(130,10),pady=(5,5))
        self.port_entry = Entry(self.bottom_frame,bg="#5d6d7e",fg="#ffffff")
        self.port_entry.grid(row=1,column=1,padx=(10,150),pady=(5,5))

        self.user_label = Label(self.bottom_frame,text="Username",bg="#34495e",fg="#ffffff")
        self.user_label.grid(row=2,column=0,padx=(130,10),pady=(5,5))
        self.user_entry = Entry(self.bottom_frame,bg="#5d6d7e",fg="#ffffff")
        self.user_entry.grid(row=2,column=1,padx=(10,150),pady=(5,5))

        # define login button event
        def set_login():
            ip_add = self.address_entry.get()
            self.login_info.append(ip_add)            
            port = self.port_entry.get()
            self.login_info.append(port)
            username = self.user_entry.get()
            self.login_info.append(username)
            Login.destroy(self)

        # create login button
        self.login_button = Button(self.bottom_frame, text="Login", command=set_login,bg="#34495e",fg="#ffffff")
        self.login_button.grid(row=3,column=1,pady=(20,0), sticky="w")

        self.mainloop()

    # define function for fetching login info for server
    def get_login(self):
        return self.login_info
        

if __name__ =="__main__":
    login = Login()
  
    