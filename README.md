# discordBot_TranferLink

----------- COMMANDS -----------
- "httpsREST_OF_YOUR_LINK" open directly the link on firefox
- ".c YOUR TEXT" sends your text to the clipboard of your computer
- "test" to know who you are and the trusted users



----------- GOAL -----------

With your phone or another device you send to the bot a link. The bot which is running on your computer, will instantly open the web link on your navigator.

----------- How -----------

send JUST the link on the message (by default it opens only https link)

for debug : you can send 'test' to know you tag and trusted users

----------- SETUP -----------

Bot to be used on Linux (tested only on ubuntu) with Firefox

In bot.py modify the first two variables, it should look like something like :
'''
TOKEN_API_DISCORD = 'xxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx.xxxxxxx'
trusted_users = ["poutin93","Kimxx"]
'''


here is the command you have to execute on your terminal to setup the automatic lauching of the program at the start of your OS :


you have to create a service :
'''mkdir -p ~/.config/systemd/user'''
'''sudo nano ~/.config/systemd/user/discordBot_TransferLink.service'''
#you change the name 'discordBot_TransferLink'

in the file you can copy paste this by changing the adresses :

'''
[Unit]
Description=Bot discord to transfer link
After=graphical.target

[Service]
ExecStart=ADRESS_OF_YOUR_PYTHON_INTERPRETER ADRESS_OF_THE_PYTHON_PROGRAM_bot.py
WorkingDirectory=ADRESS_OF_THE_FOLDER_WHERE_THE_PYTHON_PROGRAM_bot.py_IS
StandardOutput=inherit
StandardError=inherit
Environment=DISPLAY=:0
Restart=always

[Install]
WantedBy=default.target

[Service]
ExecStartPre=/bin/sleep 10
'''

#'ExecStartPre=/bin/sleep 10' add a delay of 10sec for stating the service. it is to let the time to start the graphical session and to connect to internet , maybe to increase if you have very very slow computer


Then, ~~authorize your session to have access to xhost
'''xhost +SI:localuser:NAME_OF_YOUR_SESSION'''

Next, as you modified a service
'''sudo systemctl daemon-reload'''

Next , you can enable for starting automatically when the OS launches:
'''systemctl --user enable discordBot_TransferLink.service'''

Or to test it you can start the service with this command : 
'''systemctl --user start discordBot_TransferLink.service'''
(and to stop is '''systemctl --user stop discordBot_TransferLink.service''')

TIPS : to help you to debug potential bugs you can see some logs and if the service is running with 
'''systemctl --user status discordBot_TransferLink.service'''



----------- Installation of xsel -----------

Why is it useful --> xsel manages the clipboard

How to install ?
'''sudo apt update'''
'''sudo apt install xsel'''