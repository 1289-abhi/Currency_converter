#Required Python Modules for the inbuilt functions of python are listed below.
import json
import requests
from pandas import *
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from currency_converter import CurrencyConverter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from datetime import datetime as date

# 'graph' function consists of inbuilt functions from matplotlib, pandas, requests to form a graph for historical exchange rates of the currency chosen by the user.
def graph(from_currency,to_currency):
    rates_by_date = dict()
    for i in range(1,10):
        rates_by_date[date(2019,3,i).strftime("%Y-%m-%d")] = CurrencyConverter(fallback_on_missing_rate=True).convert(1,from_currency,to_currency,date=date(2019, 3, i))

    data = []

    for key, value in rates_by_date.items():#loop to arrange the data gathered from url in date/exchange_rate sequence.
        hist_dict = {'date': key, 'exchange_rate': value}
        data.append(hist_dict)
    data.sort(key = lambda x:x['date'])#sorting the data according to the dates.
    dataframe = DataFrame(data)#using pandas to arrange it in data and columns
    x_axis = dataframe['date']
    y_axis = dataframe['exchange_rate']
    #plotting the graph using matplotlib.
    rate_graph = plt.figure(figsize = (7,5), dpi = 89)
    rate_graph.patch.set_facecolor('#FFFAFA')
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel('Exchange Rates')
    plt.plot(x_axis,y_axis,marker='o',label='Currency Rates',color='#5CEAC3')
    plt.legend()
    plt.grid()
    #drawing the graph into the canvas in tkinter window.
    canvas = FigureCanvasTkAgg(rate_graph, master = graph_frame)
    canvas.draw()
    get_widz = canvas.get_tk_widget()
    get_widz.pack()

# 'convert' function is used to convert the amount from one currency to another and it also calls graph function.
def convert():
    for widget in graph_frame.winfo_children():#destroying previous graphs.
        widget.destroy()
    from_currency=from_country_name.get()
    to_currency=to_country_name.get()
    currency_conversion = CurrencyConverter(fallback_on_missing_rate=True)#currency_converter module.
    try:#to identify if there is any input type error.
        amount_to_convert=float(amount.get())
        converted=currency_conversion.convert(amount_to_convert,from_currency,to_currency)
        converted_amount.configure(text=str(round(converted,3)))
        graph(from_currency,to_currency)#calls graph function with 2 arguments.
    except:#displaying error message in case of invalid input.
        converted_amount.configure(text='Error!')
        error_title=Label(graph_frame,text='Error!',bg='#FFFAFA',fg='#838383',font=('corbel',30),anchor=N)
        Error_message='Seems like our system has encountered an error. Reason can be one of listed below-\n1. Value of amount to convert is not given.\n2. Value does not pass valid criteria(integer or float value).\n3. Not stable internet connection.'
        error_message=Message(graph_frame,text=Error_message,fg='#838383',bg='#FFFAFA',font=('corbel',15),padx=18,anchor=W,width=620)
        error_title.pack()
        error_message.pack()
#'create_numpad' function is used to create the numpad used in tkinter window.
def create_numpad(numpad_frame,amount):
    r=3
    c=0
    button_list=['7','8','9','4','5','6','1','2','3','.','0']
    for button in button_list:#creates the button and assigns the value from the button_list.
        cmd=lambda button=button:amount.insert(END,str(button))
        button=Button(numpad_frame,text=button,width=16,command=cmd,bd=0,height=6,bg='#838383',fg='#FFFAFA',activebackground='#5CEAC3',activeforeground='#FFFAFA').grid(row=r,column=c)
        c+=1
        if c>2:
            c=0
            r+=1
#Main part. All the global declaration is done below this.
window=Tk()#main window
window.title('Currency Converter')
window.configure(bg='#FFFAFA')
main_frame=Frame(window)#main frame which consists all the child frames.
main_frame.pack(side=LEFT)
main_frame.configure(bg='#fffafa')
#from_frame part which consists a combobox with the list of 33 countries from which we want to convert and the amount which we want to convert.
from_frame=Frame(main_frame)
from_frame.configure(bg='#FFFAFA')
from_frame.pack()
from_country_name=StringVar()#holds the value of selected country.
from_countries=ttk.Combobox(from_frame,width=8,state='readonly',font=('corbel',20,'bold'),textvariable=from_country_name)
from_countries['values']=sorted(('EUR','CAD', 'HKD', 'ISK', 'PHP', 'DKK', 'HUF', 'CZK', 'AUD', 'RON', 'SEK', 'IDR', 'INR', 'BRL', 'RUB', 'HRK', 'JPY', 'THB', 'CHF', 'SGD', 'PLN', 'BGN', 'TRY', 'CNY', 'NOK', 'NZD', 'ZAR', 'USD', 'MXN', 'ILS', 'GBP', 'KRW', 'MYR'))
from_countries.current(0)#sets the default value.
from_countries.pack(anchor=W,side=LEFT)

#amount which we want to convert.
amount=Entry(from_frame,width=15,bg='#FFFAFA',font=('candara',20,'bold'),justify=RIGHT,bd=0)
amount.pack(side=LEFT)
#end of from_frame.
#to_frame part which consists a combobox with the list of 33 countries to which we want our amount to be converted and the value of converted amount.
to_frame=Frame(main_frame)
to_frame.configure(bg='#FFFAFA')
to_frame.pack()
to_country_name=StringVar()
to_countries=ttk.Combobox(to_frame,width=8,state='readonly',font=('corbel',20,'bold'),textvariable=to_country_name)
to_countries['values']=sorted(('EUR','CAD', 'HKD', 'ISK', 'PHP', 'DKK', 'HUF', 'CZK', 'AUD', 'RON', 'SEK', 'IDR', 'INR', 'BRL', 'RUB', 'HRK', 'JPY', 'THB', 'CHF', 'SGD', 'PLN', 'BGN', 'TRY', 'CNY', 'NOK', 'NZD', 'ZAR', 'USD', 'MXN', 'ILS', 'GBP', 'KRW', 'MYR'))
to_countries.current(1)
to_countries.pack(side=LEFT,anchor=W) 

converted_amount=Label(to_frame,text='',anchor=E,bg='#F5F5F5',width=14,font=('candara',20,'bold'),bd=0)
converted_amount.pack()
#end of to_frame

#convert button which invoked the convert function in order to convert the amount from chosen country to desired country.
convert_button=Button(main_frame,width=48,bd=0,fg='white',bg='#5CEAC3',padx=7,pady=10,text='Convert',command=convert)
convert_button.pack()

#numpad_frame is to create the numpad with which we can type into the box.
numpad_frame=Frame(main_frame)
numpad_frame.configure(background='#838383')
numpad_frame.pack()
create_numpad(numpad_frame,amount)

#graph_frame consists the graphs for the historical rates of the selected countries.
graph_frame=Frame(window)
graph_frame.pack(side=RIGHT)
graph_frame.configure(bg='#FFFAFA')
Title_label=Label(graph_frame,text='Currency Converter',width=19,anchor=N,padx=100,bg='#FFFAFA',fg='#838383',font=('gabriola',40))
Title_label.pack()

window.resizable(0,0)#to restrict the user to change the size of the main tkinter window.
window.mainloop()
#end of the program.
