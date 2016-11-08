# smart_watch

This project was done for the EECSE 4764 class at Columbia University. The details of the project are explained in the file Lab6.pdf.
To run the code on a ESP8266 chip you need to:
1. Flash the files accelerometer.py, buttons.py, shared.py twitter.py and main.py in the Huzzah (you can do that in the mpfshell with the command: put <my_file>). The file main.py will be automatically launched when you reset the chip.
2. Load the Android app in an Android smartphone on which USB debugging has been enabled.
3. Create an ngrok tunnel to provide a public IP address for the Huzzah: ngrok http <IP_ADDRESS>:<PORT>
4. Put the new ngrok link in the MainActivity.java file of the Android app.
5. Log into your AWS console and launch an EC2 instance
6. Install MongoDB and create a database "accelerometer" with a collection "measures"
7. 