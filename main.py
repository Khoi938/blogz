from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:123456@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

database = SQLAlchemy(app)


class Blog(database.Model):
    id = database.Column(database.Integer, primary_key = True)
    title = database.Column(database.String(100))
    body = database.Column(database.Text)
    owner_id = database.Column(database.Integer, database.ForeignKey('user.id'))

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





@app.route('/blog', methods=['POST', 'GET'])
def index():  
    all_posts = Blog.query.all()
    all_posts.reverse()
    return render_template('blog_post.html',top = 'My Blog.', posts = all_posts)

@app.route('/signup', methods = ['POST','GET'])
def signup():
    if methods == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(password) < 3 or len username < 3:
            return redirect('/signup')
        email = request.form['email']
        gender = request.form['gender']

        userObject = User(username, password, email, gender)
        database.session.add(userObject)
        database.session.commit()


    return render_template('signup.html')

@app.route('/login', methods = ['GET'])
def login():
    return render_template('login.html')

@app.route('/newpost', methods = ['POST','GET'])
def newpost():
    return render_template('new_post.html')

@app.route('/single_post', methods = ['POST','GET'])
def single():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if len(title) == 0 or len(body) == 0:
            return render_template('new_post.html',body = body, title = title, 
            top = 'New Post!', message = 'Fill in all Boxes!')
        user = user.query.filter_by(user = session['email']).first()
        new_post = Blog(title,body,user)
        database.session.add(new_post)
        database.session.commit() 
        htmlSTR = str(new_post.id)
        
        return redirect('/single_post?id='+htmlSTR)
        

    post_id = int(request.args.get('id'))
    new_post = Blog.query.get(post_id)
    return render_template('single_post.html', title = new_post.title, body = new_post.body)

if __name__ == '__main__':
    app.run()


