from flask import Blueprint,render_template,url_for,request,flash,redirect
from .user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth",__name__)

@auth.route("/",methods=["POST","GET"])
@auth.route("/login",methods=["POST","GET"])
def login():
    """
    funciton for handling logging in user
    """
    if request.method == "POST":
        # get values from form
        name = request.form.get("username")
        password = request.form.get("password")
        hash_p = User.logUser(name,hash)# hashing password for security
        if hash_p:
            if check_password_hash(hash_p,password):
                flash("successfully logged in","succes")
                return redirect(url_for("views.feed",user=User.current_user))
        flash("Username and passwords does not match","error")

    return render_template("login.html",user=User.current_user)

@auth.route("/sign-up",methods=["POST","GET"])
def sign_up():
    """
    function for handling signing up user
    """
    if request.method == "POST":
        # get values from form
        name = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        # checking for input errors
        msg = "Too short "
        error_flag = False
        if len(name) < 3 : 
            msg += "name"
            error_flag=True
        elif len(email) < 5 :
            msg += "email"
            error_flag = True
        elif len(password1) < 3 :
            msg += "password"
            error_flag = True
        elif password1 != password2 : 
            msg = "Passwords don\'t match"
            error_flag = True
        if error_flag:
            flash(msg,"error")
        else:
            hash = generate_password_hash(password1,method="sha256")# hashing password for security
            User.signUpUser(name,email,hash)
            if User.current_user:
                flash("Successfully sign up","success")
                return redirect(url_for("views.feed",user=User.current_user))
            else:
                flash("Username or email already taken","error")
    return render_template("sign-up.html",user=User.current_user)

@auth.route("/logout")
def logout():
    User.logoutUser()
    return render_template("logout.html",user=User.current_user)