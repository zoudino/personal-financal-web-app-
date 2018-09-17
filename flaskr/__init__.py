# User will crate an app inside a function.

# The function is known as the application factory. 所有的设置，注册，和其他的需要建立application的东西都需要被设置在这个function里面，然后这个应用才会被返回


import os
from flask import Flask

def create_app(test_config =None):
    # create and configure the app (在这个function里面，我们把所有的东西都设定好了)
    app = Flask(__name__, instance_relative_config = True) # __name__, 说明的就是告诉flask，python在那个地方，然后我们才能够run他.
    app.config.from_mapping(
        SECRET_KEY = 'dev', #建立这个秘钥的目的是为了保护我们的数据不被窃取.
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite') #这个地方我们建立了一个数据库. 我们需要了解更多的知识. 如何建立一个数据库.
    )
    if test_config is None:
        #load the instance config, if it exists, when no existing
        app.config.from_pyfile('config.py', silent = True) #overrides the default configuration with values taken from the config.py file in the instance folder if it exists.
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

     #上面那个，我是完全没有搞懂,关于这个test, config的东西，我们需要更多的理解.


     # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path) #ensures that app.instance_path exists.
    except OSError:
        pass

    # a simple page that says hello, creates a simple route so you can see the application working before getting into the rest of the tutorial.
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)


    from flaskr import auth, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='index')

    return app

