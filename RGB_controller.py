##############################################################################################################
# Author: Nicolas Blanchard
# Date: 3/12/21
# Purpose: Interface with a MySql server in order to retrieve RGB values. These RGB values are then used
#          to control a strip of WS2811 individually addressable pixels.
#          Developed for use with Rasspberry Pi.
##############################################################################################################

# MYSQL CONNECTOR (to access mysql database)
#import mysql.connector as mysql
#from mysql.connector import Error

# Neopixel library and initialization
import board
import neopixel

# Time library
import time

# HTTP request library
import requests

# OS library
import os

# Light strip is hooked up to D18 on the Pi
pixels = neopixel.NeoPixel(board.D12, 50)





def update_color_values(connection):
    ''' CURRENTLY UNUSED
        The input paramter 'connection' is a mysql object obtained by instantiating a class in the mysql.connector library
    '''

    try:
        # Create mysql query
        sql_select_Query = "select * from lights_color"

        # Retrieve data from database using the mysql query
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()

        # Set default values (in case the table is empty)
        red = 255
        green = 255
        blue = 255
        
        # Iterate through results
        for color in records:
            red = color[0]
            green = color[1]
            blue = color[2]

    except Error as error:
        print("Error reading from MYSQL database." + str(error))
    finally:
        # Return our data
        return [red, green, blue]


def http_request():
    ''' Sends HTTP GET request to web server and returns the data in a string '''

    r = requests.get('https://nickyblanch.xyz/lights_control/data_out.php')
    return r.text.split()





def main():

    # Loop infinitely
    while(1):
        # Clear the previous console output
        #os.system('cls')
        #os.system("cls")

        # Get our RGB values
        colors = http_request()
        print(colors) # debug
        if colors:
            red = colors[0]
            green = colors[1]
            blue = colors[2]
        else:
            red = '255'
            green = '255'
            blue = '255'

        # Illuminate the lights!!! Yay!
        pixels.fill((int(green), int(red), int(blue)))
    


# Call main
main()