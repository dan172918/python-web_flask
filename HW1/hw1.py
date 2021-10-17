import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    hwStr=""
    ans=""
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        f = open(filename,'r').read()
        hwStr=f
        f=f.lower()
        arr=[[],[]]
        for i in f:
            if ord(i)-97>=0 and ord(i)-97<=25:
                if(ord(i)-97 in arr[0]):
                    arr[1][arr[0].index(ord(i)-97)]+=1
                else:
                    arr[0].append(ord(i)-97)
                    arr[1].append(1)
        for i in range(0,len(arr[0])):
            ans+=str(chr(arr[0][i]+97))+" = "+str(arr[1][i])
            if(i!=len(arr[0])-1):
                ans+=" , "
        return render_template("hw1_ans.html",hwStr=hwStr,ans=ans)   
    return render_template("hw1_home.html")

if __name__=='__main__':
    app.run()