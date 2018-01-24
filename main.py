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
    owner_id = database.Column(database.Integer, forg)

    def __init__(self,title,body):
        self.title = title
        self.body = body

class User(database.Model):
    id = database.Column(database.Integer, primary_key = True
    username = database.Column(database.String(15))
    password =database.Column(database.String(10))
    blogs = database.Column(database.refernce)




@app.route('/blog', methods=['POST', 'GET'])
def main():  
    all_posts = Blog.query.all()
    all_posts.reverse()
    return render_template('blog_post.html',top = 'My Blog.', posts = all_posts)

@app.route('/new_post', methods = ['POST','GET'])
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
        new_post = Blog(title,body)
        database.session.add(new_post)
        database.session.commit() 
        htmlSTR = str(new_post.id)
        
        return redirect('/single_post?id='+htmlSTR)
        

    post_id = int(request.args.get('id'))
    stuff = Blog.query.get(post_id)
    return render_template('single_post.html', title = stuff.title, body = stuff.body)

if __name__ == '__main__':
    app.run()


