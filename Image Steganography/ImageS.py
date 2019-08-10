from tkinter import *
from tkinter import ttk
import tkinter.filedialog
from PIL import ImageTk
from PIL import Image
from tkinter import messagebox
from io import BytesIO
import  os

class Stegno:
    o_image_size = 0
    '''self.d_image_h = 0
    self.d_image_w  = 0'''
    def main(self,root):

        root.title('StegnoGros')
        root.geometry('900x600')
        root.resizable(width =False, height=False)
        f = Frame(root)
        title = Label(f,text='StegnoGros',pady='12')
        title.config(width=33)
        title.config(font=('courier',33))
        title.grid(pady=50)
        b_encode = Button(f,text="Encode",command= lambda :self.page2(f), padx=14)
        e_logo = PhotoImage(file='encode.png')
        e_logo = e_logo.subsample(2,2)
        b_encode.config(image=e_logo, compound=RIGHT)
        b_encode.image = e_logo
        b_decode = Button(f, text="Decode",padx=12,command=lambda :self.d_page1(f))
        d_logo = PhotoImage(file='decode.png')
        d_logo = d_logo.subsample(2, 2)
        b_decode.config(image=d_logo, compound=LEFT)
        b_decode.image = d_logo
        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        f.grid(row =1)
        b_encode.grid()
        b_decode.grid()

    def d_page1(self,f):
        f.destroy()
        d_f2 = Frame(root)
        l1 = Label(d_f2, text='Give the path of Encoded image your image:')
        l1.grid()
        bws_button = Button(d_f2, text='path', command=lambda :self.d_give_path(d_f2))
        bws_button.grid()
        d_f2.grid()

    def d_give_path(self,d_f2):
        myfile = tkinter.filedialog.askopenfilename(parent=root,
                                                    initialdir="/home/harpreet/PycharmProjects/test")
        myimg = Image.open(myfile, 'r')
        myimage = myimg.resize((350, 250))
        img = ImageTk.PhotoImage(myimage)
        panel = Label(d_f2, image=img)
        panel.image = img
        panel.grid()
        hidden_data = self.decode(myimg)
        l2 = Label(d_f2, text='Hidden data is :')
        l2.grid(pady=10)
        text_area = Text(d_f2, width=50, height=10)
        text_area.insert(INSERT, hidden_data)
        text_area.grid()
        back_button = Button(d_f2, text='<--', command= lambda :self.page3(d_f2))
        back_button.grid()

        #print('height:',self.o_image_h, 'width:',self.o_image_w)'
        show_info = Button(d_f2,text='moreinfo',command=self.info)
        show_info.grid()



    def decode(self, image):
        data = ''
        imgdata = iter(image.getdata())

        while (True):
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            # string of binary data
            binstr = ''

            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            data += chr(int(binstr, 2))
            if pixels[-1] % 2 != 0:
                return data

    def page2(self,f):
        f.destroy()
        f2 = Frame(root)
        l1= Label(f2,text='Give the path of your image:')
        l1.grid()
        bws_button = Button(f2,text='path',command=lambda : self.give_path(f2))
        bws_button.grid()
        f2.grid()


    def give_path(self,f2):
        myfile = tkinter.filedialog.askopenfilename(parent=root,
                                                       initialdir="/home/harpreet/PycharmProjects/test")
        myimg = Image.open(myfile)
        myimage = myimg.resize((350,250))
        img = ImageTk.PhotoImage(myimage)
        panel = Label(f2, image=img)
        panel.image = img
        self.o_image_size = os.stat(myfile)
        self.o_image_w, self.o_image_h = myimg.size
        panel.grid()
        l2 = Label(f2, text='Enter the data in the below text field:')
        l2.grid()
        text_area = Text(f2, width=50, height=10)
        text_area.grid()

        encode_button = Button(f2, text='Encode', command=lambda :self.enc_fun(text_area,myimg))
        back_button = Button(f2, text='<--', command=lambda : self.page3(f2))
        back_button.grid(row=18, column=8)
        encode_button.grid(row=15,column=8)

    def info(self):

        try:
            str = 'original image:-\nsize of original image:{}mb\nwidth: {}\nheight: {}\n\n' \
                  'decoded image:-\nsize of decoded image: {}mb\nwidth: {}' \
                '\nheight: {}'.format(self.o_image_size.st_size/1000000,
                                    self.o_image_w,self.o_image_h,
                                    self.d_image_size/1000000,
                                    self.d_image_w,self.d_image_h)
            messagebox.showinfo('info',str)
        except:
            messagebox.showinfo('info','unable to get the information')
    def genData(self,data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

    def modPix(self,pix, data):

        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):

            # Extracting 3 pixels at a time
            pix = [value for value in imdata.__next__()[:3] +
                   imdata.__next__()[:3] +
                   imdata.__next__()[:3]]

            # Pixel value should be made
            # odd for 1 and even for 0
            for j in range(0, 8):
                if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            # Eigh^th pixel of every set tells
            # whether to stop or read further.
            # 0 means keep reading; 1 means the
            # message is over.
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self,newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):

            # Putting modified pixels in the new image
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self,text_area,myimg):
        # img = input("Enter image name(with extension): ")
        # image = Image.open(img, 'r')
        # data = input("Enter data to be encoded : ")
        data = text_area.get("1.0", "end-1c")
        if (len(data) == 0):
            raise ValueError('Data is empty')

        newimg = myimg.copy()
        self.encode_enc(newimg, data)

        my_file = BytesIO()
        newimg.save('o.png')
        newimg.save(my_file,'png')
        self.d_image_size = my_file.tell()
        self.d_image_w,self.d_image_h = newimg.size
        messagebox.showinfo("Success","Encoding Successful")

    def page3(self,frame):
        frame.destroy()
        self.main(root)

root = Tk()

o = Stegno()
o.main(root)

root.mainloop()
