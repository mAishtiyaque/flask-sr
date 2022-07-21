from flask import request,jsonify,make_response
import string,random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], future=True)
#session = Session(engine)
#print(app.config)

#lst=[['Hello Bhai', 312], ['Mr. Owais', 313], ['Hello World', 314], ['Owais Bhai', 315]]

def bad_req(arg=None):
    print('Bad Request',arg)
    return "<title>Bad Request</title>%s<h1>Bad Request</h1><p>Bad requested URL.</p>" % arg, 400
def check_token(sess,req):
    istoken=False
    try:
        userid=req['username']
        token=req['token']
        #stmt = select(Tokens).where(Tokens.userid == userid,Tokens.token==token)
        #istoken=sess.execute(stmt)
        istoken=sess.query(Tokens).filter_by(userid=userid,token=token).first()
        print('Hr',istoken.token)
    except Exception:
        bad_req("Exception occured")
    return istoken
@app.route('/')
def home():
    return "<title>400 Method Not Allowed</title><h1>Method Not Allowed**</h1><p>The method is not allowed for the requested URL.</p>", 400

@app.route('/users/register', methods=['POST'])
def handleRegister():
        if request.method !='POST': return bad_req()
        if request.is_json:
            req=request.get_json()
            with Session(engine) as sess:
                try:
                    fname=req["firstName"]
                    lname=req["lastName"]
                    userid=req['username']
                    passw=req['password']
                    user=sess.query(Users).filter_by(userid=userid).count()
                    print('>>>> ',user)
                    if user:
                        res_body= { "ok": False,
                                "statusText": "Username Already taken",
                        }
                        return make_response(jsonify(res_body),200)
                    #stmt = select(Users).where(Users.userid == userid,Users.passw==passw)
                    #user=sess.execute(stmt).scalars()
                    #print('>>>> ',fname,lname,userid,passw)
                    sess.add(Users(userid,passw,fname,lname))
                    sess.commit()
                    #user=sess.query(Users).filter_by(userid=userid,passw=passw).first()
                    res_body= { "ok": True,
                                "statusText": "Registeration Success",
                            }
                    return make_response(jsonify(res_body),200)
                except Exception:
                     return bad_req("Exception occured Flag")
        else:
            return bad_req()
@app.route('/users/authenticate', methods=['GET','POST'])
def handleLogin():
        if request.method !='POST': return bad_req()
        if request.is_json:
            req=request.get_json()
            with Session(engine) as sess:
                try:
                    userid=req['username']
                    passw=req['password']
                    #stmt = select(Users).where(Users.userid == userid,Users.passw==passw)
                    #user=sess.execute(stmt).scalars()
                    #print('>>>>',[i for i in user],user.__dict__)
                    user=sess.query(Users).filter_by(userid=userid,passw=passw).first()
                except Exception:
                    return bad_req("Exception occured")
                #print(user)
                if user:
                    token=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(15))
                    print(">>>Loggedin",user.userid)
                    #stmt = select(Userdata).where(Users.userid == userid)
                    #userdata=sess.execute(stmt)
                    sess.add(Tokens(userid=userid,token=token))
                    sess.commit()
                    res_body= { 
                            "ok": True,
                            "statusText": "User Login Success",
                            "id": user.userid,
                            "username": user.userid,
                            "firstName": user.fname,
                            "lastName": user.lname,
                            "token": token
                        }
                else:
                    res_body={
                        "ok": False,
                        "statusText": "Username or password invalid!",
                    }
                return make_response(jsonify(res_body),200)
        else:
            return bad_req()

@app.route('/users/logout', methods=['GET','POST'])
def handleLogout():
        if request.method !='POST': return bad_req()
        if request.is_json:
            req=request.get_json()
            with Session(engine) as sess:
                #print("print",req)
                token=check_token(sess,req)
                if token:
                    token=req['token']
                    userid=req['username']
                    noitem=sess.query(Tokens).filter(Tokens.userid==userid,Tokens.token==token).delete()
                    sess.commit()
                    if noitem>0:
                        print("Logout",userid)
                        res_body= { "ok": True,
                            "statusText": "Logout Successfully",
                        }
                    else: bad_req()
                else:
                    res_body={
                        "ok": False,
                        "statusText": "Unknown Error occured !!",
                    }
                return make_response(jsonify(res_body),200)
        else:
            return bad_req()

@app.route('/users/delete', methods=['GET','POST'])
def handleItemDelete():
        if request.method !='POST': return bad_req()
        if request.is_json:
            req=request.get_json()
            with Session(engine) as sess:
                #print("print",req)
                token=check_token(sess,req)
                #check and delete item
                if token:
                    itemid=req['itemID']
                    userid=req['username']
                    #dat=Tokens.query.filter_by(userid=userid).delete()
                    noitem=sess.query(Userdata).filter(Userdata.userid==userid,Userdata.textid==itemid).delete()
                    sess.commit()
                    if noitem>0:
                        print("Deleted",userid)
                        res_body= { "ok": True,
                            "statusText": "Deleted Successfully",
                        }
                    else: bad_req()
                else:
                    res_body={
                        "ok": False,
                        "statusText": "Unknown Error occured !!",
                    }
                return make_response(jsonify(res_body),200)
        else:
            return bad_req()
@app.route('/users/getlist', methods=['GET','POST'])
def handleListget():
        if request.method !='POST': return bad_req()
        if request.is_json:
            req=request.get_json()
            with Session(engine) as sess:
                token=check_token(sess,req)
                if token:
                    userid=req['username']
                    userdata=sess.query(Userdata).filter_by(userid=userid).all()
                    lst2o=[ud.serialize() for ud in userdata]
                    print('List Fetched',userid,token)
                    res_body= { 
                            "ok": True,
                            "statusText": "Fetched success",
                            "list":lst2o
                        }
                else:
                    res_body={
                            "ok": False,
                            "statusText": "Please Login again"
                    }
                return make_response(jsonify(res_body),200)
        else:
            return bad_req()
@app.route('/users/additem', methods=['GET','POST'])
def handleAddItem():
        if request.method !='POST': return bad_req()
        if request.is_json :
            req=request.get_json()
            #check and delete item
            with Session(engine) as sess:
                token=check_token(sess,req)
                if token:
                    #add item in db
                    print(req)
                    userid=req['username']
                    newitem=req['newitem']
                    nextid=str(int(datetime.now().timestamp()*100)) 
                    #print("Time >>> ",datetime.now().timestamp())
                    sess.add(Userdata(userid,textid=nextid,rtext=newitem))
                    sess.commit()
                    print('Added',userid,newitem) #remove newitem arg due to security
                    #lst.append([req['newitem'],nextid])
                    res_body= { "ok": True,
                                "statusText": "added success",
                                "id":nextid
                            }
                    #return make_response(jsonify(res_body),200)
                else: res_body={"ok": False,
                                "statusText": "Unknown Error occured !!"
                                }
                return make_response(jsonify(res_body),200)
        else:
            return bad_req()

@app.errorhandler(404)
def handle_404(path):
    return '<title>405 Method Not Allowed</title><b>%s</b> <h1>Method Not Allowed**</h1><p>The method is not allowed for the requested URL.</p>' % path ,404
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.PORT)