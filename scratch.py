#
# import pyradios
# import pprint
# import ffmpeg
#
#
# rb = pyradios.radios.RadioBrowser()
#
# search_rb = rb.search(countrycode='jp',)
#
# pprint.pprint(search_rb)
#
# import os,subprocess, time
# pid = os.getpid()
# shell_program=[ '/home/marty/PycharmProjects/venv/bin/python /home/marty/PycharmProjects/DiscordBot/main.pyw']
# file_path=os.path.realpath(__file__)
# print("".join(shell_program))
# subprocess.Popen(shell_program)
# exit()
#
# print('test')
#

import aiohttp,asyncio


url="http://musicbird.leanstream.co/JCB086-MP3"
async def main():
        sesh_ = aiohttp.ClientSession()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())