import tkinter as tk
from tkPDFViewer import tkPDFViewer as pdf
import results_to_pdf as rtp

def handle_click(event):
    company = entry.get()
    entry.delete(0, tk.END)
    
    if len(company) > 0:
        rtp.generate_reports(company)
    
    busted_display = tk.Label(window, text="\nIf the company name supplied was correct, two pdf files will be created in the summarize_scripts folder.")
    busted_display.pack()
    window.after(3000, busted_display.destroy)
    window.update_idletasks()

window = tk.Tk()
window.geometry("800x400")
title = tk.Label(text="\nStock Analyzer\n")
title.config(font=('Helvetica bold', 16))
title.pack()

label = tk.Label(text="To get started, type in a company's symbol and enter it into the text field.\n\nThe calculator will return two files, either in PDF or CSV format, showing the percent gains and loss\n\nduring different periods between local minimum and maximum points in the company's stock market history.")
label.place(relx = 0.5,rely = 0.5, anchor = 'center')
entry = tk.Entry()

label.pack()
entry.pack(padx=50, pady=20)

button = tk.Button(
    text="Submit",
    width=15,
    height=2,
    bg="white",
    fg="black",
)

button.bind("<Button-1>", handle_click)

button.pack()

window.mainloop()