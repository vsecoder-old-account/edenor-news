"""
    MIT License

    Copyright (c) 2022 Edenor-News

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

# ************** Standart module *********************
from datetime import datetime
import configparser
import psutil
import uvicorn
# ************** Standart module end *****************

# ************** External module *********************
from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
#from fastapi import WebSocket
from starlette.templating import Jinja2Templates
from starlette.responses import Response
# ************** External module end *****************

# ************** Logging beginning *******************
from loguru import logger
from mod.logging import add_logging
# ************** Unicorn logger off ******************
import logging
#logging.disable()
# ************** Logging end *************************

# ************** Read "config.ini" ********************
config = configparser.ConfigParser()
config.read('config.ini')
database = config["DATABASE"]
directory = config["TEMPLATES"]
logging = config["LOGGING"]
admin = config["ADMIN"]
# ************** END **********************************

# ************ DB connect and import ******************
from mod.db import global_init
#global_init(database["name"])
global_init("database.db")
# import classes
from mod.post import Posts
# ************** END **********************************

# loguru logger on
add_logging(logging.getint("level"))

# Server instance creation
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
logger.info("Start server")
templates = Jinja2Templates(directory["folder"])

# Record server start time (UTC)
server_started = datetime.now()

# Server home page
@app.get('/')
def home_page(request: Request):
    posts = Posts._get_last_posts()
    return templates.TemplateResponse('index.html', {'request': request, 'posts': posts})

# Server page with working statistics
@app.get('/status')
def status_page(request: Request):
    ram = psutil.virtual_memory()
    stats = {
        "Server time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Server uptime": str(datetime.now()-server_started),
        "CPU": f"{psutil.cpu_count()} cores ({psutil.cpu_freq().max}MHz) with {psutil.cpu_percent()} current usage",
        "RAM": f"{ram.used >> 20} mb / {ram.total >> 20} mb"
    }
    return templates.TemplateResponse('status.html',
                                      {'request': request,
                                       'stats': stats})

# ************** Start post page handlers **************
# /post/<id>
@app.get('/post/{id}')
def methods_page(request: Request, id):
    post = Posts._get_post(id)
    return templates.TemplateResponse('post.html',
                                      {'request': request,
                                       'post': post})

# /editor/
@app.get('/editor')
def methods_page(request: Request, password):
    print(admin["password"])
    if password != "admin":
        return "Unvalid password"
    else:
        return templates.TemplateResponse('editor.html',
                                        {'request': request})
# *********************** END *************************

# ******************* start server ********************
if __name__ == "__main__":
    # ******* dev *******
    uvicorn.run('app:app',
        host="0.0.0.0", 
        port=8000,
        log_level="debug",
        http="h11",
        reload=True, 
        use_colors=True,
        workers=3
    )
    # **** production ****
    """
    uvicorn.run('app:app',
        host="0.0.0.0", 
        port=80,
        http="h11"
    )
    """
    logger.info("Stop server")
