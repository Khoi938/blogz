from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

database = SQLAlchemy(app)
app.secret_key = 'secretkey'


class Blog(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    title = database.Column(database.String(100))
    body = database.Column(database.Text)
    owner_id = database.Column(database.String(15), database.ForeignKey('user.username'))
    #owner_id = database.Column(database.Integer, database.ForeignKey('user.id'))


    def __init__(self,title,body,user):
        self.title = title
        self.body = body
        self.owner = user

class User(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(15),unique = True)
    password = database.Column(database.String(10))
    email = database.Column(database.String(50))
    gender = database.Column(database.String(20))
    blogs = database.relationship('Blog', backref = 'owner')

    def __init__(self, username, password, email, gender):
        self.email = email
        self.username = username
        self.password = password
        self.gender = gender

@app.before_request
def authenticate():
    public = ['blog', 'signup','login','index']
    if request.endpoint not in public and 'username' not in session:
        session['authenticate']='Please login first.'
        return redirect('/login')

@app.route('/', methods = ['GET'])
def index():
    user = User.query.all()
    return render_template('index.html', users = user, top = 'User List')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if 'authenticate'in session:  
        del session['authenticate']
    
    if request.args.get('username') != None: 
        username = request.args.get('username')
        posts = Blog.query.filter_by(owner_id=username).all()
        posts.reverse()
        return render_template('singleUser.html', top = 'Individual Post', 
        username = username, posts = posts)

    all_posts = Blog.query.all()
    all_posts.reverse()
    return render_template('blog_post.html',top = 'Home Page', posts = all_posts)

@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        passwordC = request.form['passwordC']
        email = request.form['email']
        user_object = User.query.filter_by(username = username).first()
        
        if username == '' or password == '' or passwordC == '':
            return render_template('signup.html', invalid = 'Username and/or Password is missing.', email = email)
        if len(username) < 3:
            return render_template('signup.html', invalid = 'Please make your username longer', email = email)
        if username.isalnum() == False:
            return render_template('signup.html', invalid = 'Invalid Character!!', email = email)
        if user_object != None:
            return render_template('signup.html', invalid = 'Username is taken.', email = email)
        if len(password) < 3:
            return render_template('signup.html', shortPW = 'Please make your password longer.', email = email)
        if password != passwordC:
            return render_template('signup.html', invalid = "Password doesn't match", email = email)

        gender = request.form['gender']
        userObject = User(username, password, email, gender)
        database.session.add(userObject)
        database.session.commit()
        session['username'] = username
        return redirect('/newpost')

    if 'authenticate'in session:  
        del session['authenticate']
    return render_template('signup.html', top = 'Registration')

@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        #limit the number of attempt with session['attempt'] = 10
        username = request.form['username']
        password = request.form['password']
        user_object = User.query.filter_by(username = username).first()
        if user_object == None:
            return render_template('login.html', top = 'Login', user = 'Username not found.')
        if user_object.password == password:
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('login.html', top = 'Login', wrong = 'Incorrect Password.',username = username)
    if session.get('authenticate') != None:
        verify = session.get('authenticate')
        return render_template('login.html', top = 'Login', authenticate = verify)

    return render_template('login.html', top = 'Login')

@app.route('/logout', methods = ['GET'])
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/newpost', methods = ['POST','GET'])
def newpost():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if len(title) == 0 or len(body) == 0:
            return render_template('newpost.html',body = body, title = title, 
            top = 'New Post', message = 'A post need a Title and Message')
        user_object = User.query.filter_by(username = session['username']).first()
        new_post = Blog(title,body,user_object)
        database.session.add(new_post)
        database.session.commit() 
        htmlSTR = str(new_post.id)
        
        return redirect('/newpost?id='+htmlSTR)
        
    if request.args.get('id') != None: 
        post_id = int(request.args.get('id'))
        new_post = Blog.query.get(post_id)
        return render_template('single_post.html', title = new_post.title, body = new_post.body)

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()


