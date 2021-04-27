# discordbot_testing
just messing with making a discord bot with the end goal of being able to use the radio-browser.info api to play any radio station in a discord call...


this is also just something i can say i did on my own while just reading docs and some basic tutorials on the web...


this code needs a ".env" file in the same location as the pyw file. it will contain the discord bot token and other stuff that is specific to your system. i will update this when i get a mostly finalised .env file with all the prerequisite entries or ill make a setup script to make the file for users. 


# most likely updates after testing is done. 
i will likely make a setup.py so i can also set the computer to setup the required python modules using subprossess to run the pip comands needed so the user does not need to do anyting they dont know about and i likely include the custom files that may need to be packaged in a base64 encoded string and dump them to a known directory. (i know it can be a bad idea for security but that is why it all will be in the user space (pip install <Module name> --user) and only i may even make an md5 checksum funtion to be sure the files were not tampered with.  


i like the idea of a self containing package that the user doens't need to do any major leg work. because of this i may even use the setup script to include an update funtion pull the new updated from my github directly. it will take a while before i am ready to release this into the as a usable package. we will see
