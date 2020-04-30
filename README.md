I have created an API by using Python Flask to use it inside of my some game module project. It is actually sending requests to YouTube with pytube module and fetching MP4 file and converting it to MP3 by using FFMPEG lib and stores, serves the converted file as a respond to the client.

You may want to config WSGI for the deployment and for your own stuff.

`apt install ffmpeg`

`pip3 install flask`

`pip3 install ffmpeg-python`
