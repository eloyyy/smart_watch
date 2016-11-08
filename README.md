# smart_watch

This project was done for the EECSE 4764 class at Columbia University. The details of the project are explained in the file Lab6.pdf.
To run the code on a ESP8266 chip you need to:

0. In the file esp8266_code/main.py set the ESSID and password of your current WiFi network.
1. Flash the files: accelerometer.py, buttons.py, shared.py twitter.py and main.py in the Huzzah (you can do that in the mpfshell with the command: put <my_file>). The file main.py will be automatically launched when you reset the chip.
2. Load the Android app in an Android smartphone on which USB debugging has been enabled.
3. Create an ngrok tunnel to provide a public IP address for the Huzzah: ngrok http <IP_ADDRESS>:<PORT>
4. Put the new ngrok link in the MainActivity.java file of the Android app.
5. Log into your AWS console and launch an EC2 instance
6. Install MongoDB and create a database "accelerometer" with a collection "measures"
7. Get an API key for the OpenWeather API and put this key in the file flaskapp/flaskapp.py
8. Get an API key to connect to your twitter account with Thingspeak, put this key in the file flaskapp/flaskapp.py
9. SSH into your EC2 instance and launch the flask app

After completing all these steps the smart watch is ready to use ! Here is a diagram that sums up how the global system was built.

#### Architecture of the smart watch environment
![alt tag](https://github.com/eloyyy/smart_watch/blob/master/architecture_smart_watch.JPG)