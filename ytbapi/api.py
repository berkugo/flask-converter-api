from flask import Flask, request, send_file
from pytube import YouTube
import validators
import os, subprocess

class Converter:

    timeOut = 4*60
    dir_path = os.path.dirname(os.path.realpath(__file__))


    def __init__(self):
        self.app = Flask(__name__)
        self.configRoutes()
        self.testContext()
        self.app.run(debug=True)
    
    def configRoutes(self):
        self.app.add_url_rule("/", "convertTo", self.convertTo, methods=['GET'])

    def convertTo(self):
        if 'url' in request.args:
            url = request.args.get('url')
            result = self.convert(url)
            return result
        else:
            return {'result': "Error"}

    def convert(self, url):
        
        if('url' and 'pid' not in request.args):
            return {'result': False}
        if(validators.url(url)):
            yt = YouTube(request.args.get("url"))
            stream = yt.streams.filter(only_audio=True).first()
            stream.download(output_path=Converter.dir_path + "/files", filename = "{pid}".format(pid = request.args.get('pid')))
            command = "ffmpeg -i files/{pid}.mp4 -map 0:a:0 -b:a 96k {pid}.mp3".format(pid = request.args.get('pid'))
            subprocess.call(command, shell=True)
            result = send_file(Converter.dir_path + "/{pid}.mp3".format(pid=request.args.get('pid')))    
            os.remove(Converter.dir_path+"/files/{pid}.mp4".format(pid=request.args.get('pid')))        
            os.remove(Converter.dir_path+"/{pid}.mp3".format(pid=request.args.get('pid')))        
            return result
        else: 
            return {'result': "Error, URL is invalid."}

    def testContext(self):
        with self.app.test_request_context("/"):
             assert request.path == "/"


if __name__ == "__main__":
    Converter()
