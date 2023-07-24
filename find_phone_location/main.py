import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from tkinter import *
from timezonefinder import timezonefinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
from PIL import Image, ImageTk

root = Tk()
root.title("Phone Number Tracker")
root.geometry('365x584+300+200')
root.resizable(False, False)

def Track():
    enter_number = entry.get();
    number = phonenumbers.parse(enter_number)

    locate=geocoder.description_for_number(number, "en")
    country.config(text=locate)

    operator=carrier.name_for_number(number, 'en')
    sim.config(text=operator)

    tzName = timezone.time_zones_for_number(number)
    tz.config(text=tzName)

    geoLocator=Nominatim(user_agent="geoapiExercises")
    location = geoLocator.geocode(locate)

    latitude=location.latitude
    longitude=location.longitude

    # print(latitude, longitude, location)

    lat.config(text=latitude)
    long.config(text=longitude)


    obj = timezonefinder.TimezoneFinder()
    result = obj.timezone_at(lng=longitude, lat=latitude)

    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)

    # +8801912251070





#icon
# icon = PhotoImage(file="logo.jpg")
# root.iconphoto(False, icon)

#logo
# logo = PhotoImage(file='logo.jpg')
# Label(root, image=logo).place(x=240, y=70)

# label = Label(root, image=logo)
# label.pack()

# image = Image.open("logo.jpg")
# photo = ImageTk.PhotoImage(image)
# label=Label(root, image=photo)
# label.place(x=240, y=70)
# label.pack()
#

# Eback = PhotoImage(file='logo.jpg')
# Label(root, image=Eback).place(x=20, y=190)

#Heading
heading=Label(root, text="Track Number", font=('arial',15,'bold'))
heading.place(x=20, y=190)

#entry
entry=StringVar()
enter_number=Entry(root, textvariable=entry, width=17, justify='center', bd=0, font=('arial', 20))
enter_number.place(x=20, y=220)

#Search Button
search=Button(root, text="Search", borderwidth=0, cursor='hand2', bd=0, font=('arial', 20), command=Track)
search.place(x=20, y=260)

#country
country=Label(root, text="Country:", bg="#57adff", fg="black", font=('arial',10,'bold'))
country.place(x=50, y=400)
#sim
sim=Label(root, text="SIM:", bg="#57adff", fg="black", font=('arial',10,'bold'))
sim.place(x=200, y=400)

#Zone
tz=Label(root, text="TimeZone:", bg="#57adff", fg="black", font=('arial',10,'bold'))
tz.place(x=50, y=450)

#Phone time:
clock=Label(root, text="Clock:", bg="#57adff", fg="black", font=('arial',10,'bold'))
clock.place(x=200, y=450)

#lat long
lat=Label(root, text="Lat:", bg="#57adff", fg="black", font=('arial',10,'bold'))
lat.place(x=50, y=500)

long=Label(root, text="Lng:", bg="#57adff", fg="black", font=('arial',10,'bold'))
long.place(x=200, y=500)

root.mainloop()
