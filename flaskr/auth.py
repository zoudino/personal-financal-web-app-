


# blueprint and view 都是为了和user进行interaction， 而且blueprint 就是为了能够帮助我们更好的管理很多很多的pages
# 整个py file 都是在Discuss 如何创立一个让用户注册和登录的一个页面出来. 这样user的信息就会被secure。 从而帮助自己理解更多关于web development的东西.
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


#在这个里面我们创造了一个blueprint named 'auth'. 为了让application知道where the module and defined. The url_prefix will be prepended to all the URLs associated with the blueprint --url就是我们的blueprint
#在我们define了我们的blueprint之后， 我们要马上把这个blueprint import and register the blueprint from the factory using app.register_blueprint().


#下面的东西，我们要打起十分的精神进行学习，那就是成功的建立一个login

#require authentication in other views
# Creating, editing, and deleting blog posts will require a user to be logged in. 想要创建， 编辑，和删除blog posts 需要user能够logged in the system
# 这个地方设计的非常的巧妙. 也就是如果user没有log in 我们把用户direct到初始页面里面去. 如果用户log in了，我们就让用户持续的待在原本的页面里面.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view


@bp.before_app_request #在这个地方，我们注册了一个function before the view funciton, no matter what URL is requested.load_logged_in_user回去检查是否用户的id储存在了session里面，然后从数据库里面拿出数据出来，把数据储存在request一直存在的长度里面.
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id=?', (user_id,)
        ).fetchone()

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is requried'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)).fetchone() is not None:
            error = 'User{} is already registered.'.format(username)
        #这个地方就是帮助我们check the user input. 我们要确保user的所有行为都能够被考虑到，这样的话，我们的value就可以被securely saved in out database.

        if error is None:
            db.execute(
               'INSERT INTO user (username, password) VALUES (?,?)',
               (username, generate_password_hash(password)) #这个地方是帮助我们把密码安全的保存下来，这样的话，密码不会被轻易的被盗取.
        )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

"""
    Here, let's explain everything
    1. @bp.route associates the URL /register with the register view function. When Flask receives a request to /auth/register, it will call the register view and use the return value as the response.
    这个地方就是说 我们把register 这个url告诉了application，这个的话当user type url:/auth/register, 他们就能够成功的看到pages

    2. If the user submitted the form, request.method will be 'POST'. In this case, start validating the input. Post这个method就是便于帮助我们对于数据进行传送. 这样的话，我们就可以打开另外一个窗口. 这样的话就可以开始注册账户了. 

3.request.form is a special type of dict mapping submitted form keys and values. The user will input their username and password.

4.Validate that username and password are not empty.

5.Validate that username is not already registered by querying the database and checking if a result is returned. db.execute takes a SQL query with ? placeholders for any user input, and a tuple of values to replace the placeholders with. The database library will take care of escaping the values so you are not vulnerable to a SQL injection attack.

5. fetchone() returns one row from the query. If the query returned no results, it returns None. Later, fetchall() is used, which returns a list of all results.

6. If validation succeeds, insert the new user data into the database. For security, passwords should never be stored in the database directly. Instead, generate_password_hash() is used to securely hash the password, and that hash is stored. Since this query modifies data, db.commit() needs to be called afterwards to save the changes.

7.After storing the user, they are redirected to the login page. url_for() generates the URL for the login view based on its name. This is preferable to writing the URL directly as it allows you to change the URL later without changing all code that links to it. redirect() generates a redirect response to the generated URL.
  url_for 其实的作用就是帮助我们更好的对于URl进行管理，这样在之后我们就不会要对很多的代码进行编辑和转换. 

If validation fails, the error is shown to the user. flash() stores messages that can be retrieved when rendering the template.

When the user initially navigates to auth/register, or there was an validation error, an HTML page with the registration form should be shown. render_template() will render a template containing the HTML, which you’ll write in the next step of the tutorial.


当user click register的时候，这个register的page就应该出现. 
"""


# 明天在同一个地方写login. 一步一步慢慢来！ to build the solution step by step

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/login.html')

# session就是一个dictionary会用来储存信息 across requests. 当用户的信息被成功的储存的时候. the user's id is stored in a new session.用户的id就被储存在了一个新的session里面.
# 数据存在了cookie里面 that is sent to the browser, and the browser then send it back with subsequent requests. 这个在cookie里面的数据被送到了浏览器里面去，然后user所有在数据上面的行为都会被记录下来.







# After, we finished this page. We need to start to write out the user interface. So, user can see a UI and make changes.
# The template will be stored in the templates directory inside the flaskr package.


#Template 是文件包含 静态数据 和 对要动态数据的包裹. 为了能够显示出最后文件的样子, 模板需要被使用.
# Flask uses the Jinja template library to render templates.
"""
# 在Jinja这个东西里面， Anything between {{ and }} is an expression that will be output to the final document. 
   {% and %} denotes a control flow statement like if and for. 
   Unlike Python, blocks are denoted by start and end tags rather than indentation since static text within a block could change indentation.
   在这些block里面，indentation就不会被特别的重要了.
"""


@bp.route('/logout')
def logout():
    """Clear the current seesion, inlcluding the stored user id"""
    session.clear()
    return redirect(url_for('index'))


