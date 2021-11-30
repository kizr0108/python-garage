import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
LOG_PATH = os.path.join('autorun_manager/log.json')
from flask import Flask,render_template,request,redirect
from modules.sendtoline import SendToLine
from autorun_manager.app import get_apps, run_it

app = Flask(__name__)

with open(LOG_PATH, 'r', encoding='utf-8') as f:
    log_json = json.load(f)
log_autorun = []
for key,value in log_json.items():
    if value[0] != None:
        log_autorun.append([key,value[0]])

@app.route("/login/")
def login():
    return render_template("login.html",title="login")

@app.route("/")
def index():
    success_info = request.args.get('successinfo')
    path = './'
    flist = os.listdir(path)
    applist = []
    for f in flist:
        if '.' in f:
            continue
        if f == 'app_template':
            continue
        if not os.path.isdir(path+f):
            continue
        if os.path.exists(path+f+'/app.py') and os.path.exists(path+f+'/settings.py'):
            applist.append(f)
    return render_template("index.html",title="success!",log_autorun=log_autorun,applist=applist,success_info=success_info)

@app.route("/",methods=['get'])
def result():
    success_info = request.args.get('successinfo')
    path = './'
    flist = os.listdir(path)
    applist = []
    for f in flist:
        if '.' in f:
            continue
        if f == 'app_template':
            continue
        if not os.path.isdir(path+f):
            continue
        if os.path.exists(path+f+'/app.py') and os.path.exists(path+f+'/settings.py'):
            applist.append(f)
    return render_template("index.html",title="success!",log_autorun=log_autorun,applist=applist,success_info=success_info)

@app.route("/testapp-sendline/")
def sendline():
    return render_template("testapp-sendline.html", title="success!",sidebar=' ')

@app.route("/testapp-sendline/",methods=["post"])
def post():
    sendline_title = request.form["sendline-title"]
    sendline_text = request.form["sendline-text"]
    if sendline_title and sendline_text:
        sendline = SendToLine()
        sendline.send(sendline_title+'\n'+sendline_text)
    return render_template("testapp-sendline.html", title="送信結果", sendline_title=sendline_title, sendline_text=sendline_text, sidebar=' ')


@app.route("/run/",methods=["post"])
def loading_while_runapp():
    app_name = request.form["app-name"]
    apps = get_apps()
    if app_name in apps:
        run_it(app_name)
    return redirect('/?result=success&appname={}'.format(app_name))

@app.route("/success-info/")
def success_info():
    return redirect('/?successinfo={}'.format('やったね！'))


if __name__ == "__main__":
    app.run(debug=True)
