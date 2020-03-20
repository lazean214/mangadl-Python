import tkinter
from tkinter import BOTH, END, LEFT
import random # For random functions
import requests
import os
from bs4 import BeautifulSoup
import time
import re

window = tkinter.Tk()
window.title("Manga Downloader")
window.geometry("500x200")


def initDl():
    mUrl = MyUrl.get()
    mStart = MyStartEntry.get();
    page = requests.get(mUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    title = soup.find('h1').getText()
    
    dice_thrown.configure(text="Downloading: " + str(title))
    
    content = soup.find(class_="row-content-chapter")
    
    links = content.find_all('a')
    MyMangaTitle = MangaTitle.get()
    count = 0;
    for link in links:
        chapter = link.get_text()
        count = count + 1
        
        if int(count) >= int(mStart): 
           
            urls = link['href']
            print(chapter + str(count))
            
            window.update_idletasks()
            time.sleep(2)

            chap = re.sub(r'^(.{11}).*$', '\g<1>...', chapter)
#            chaptetTitle = re.sub(r'\W+', '-', chap)
            chaptetTitle = urls.rsplit('/', 1)[-1]
            
            
            if not os.path.exists('../../../downloads/' + str(MyMangaTitle) + '/' + chaptetTitle):
                os.makedirs('../../../downloads/' + str(MyMangaTitle) + '/' + chaptetTitle)

            page = requests.get(urls)

            soup = BeautifulSoup(page.content, 'html.parser')   
            container = soup.find(class_="container-chapter-reader")

            images = container.findAll('img')

            counter = 0
            #print images
            for image in images:
                src = image['src']
            #    image_url = 'https://www.nakheel.com' + src
                counter += 1
               
                number = counter
                r = requests.get(src)
                with open('../../../downloads/' + str(MyMangaTitle) + '/' + chaptetTitle + '/' +str(number) +".jpg", "wb") as code:
                    code.write(r.content)
                print ("Downloading: " + src)
       
        else: 
            print('Escaping offset ' + str(count))
        
    dice_thrown.configure(text="Download Completed ")        
            
    
    
    
MyTitle = tkinter.Label(window, text="NCS Manga Downloader",font="Helvetica 12 bold")
MyTitle.pack()

MyManga = tkinter.Label(window, text="Enter Url")
MyManga.pack()

MyUrl = tkinter.Entry(window)
MyUrl.pack()

MangaTitleLabel =tkinter.Label(window, text="Enter Manga Title : No Special Character")
MangaTitleLabel.pack()

MangaTitle = tkinter.Entry(window)
MangaTitle.pack()

MyStartLabel = tkinter.Label(window, text="Offset (Note: Latest > Old)").pack()
MyStartEntry = tkinter.Entry(window)
MyStartEntry.pack()

MyButton = tkinter.Button(window, text="Download", command=initDl)
MyButton.pack()

dice_thrown = tkinter.Label(window, font="Helvetica 11")
dice_thrown.pack()


window.mainloop()