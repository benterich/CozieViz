from flask import Flask
from my_project.routes import dashboard
from my_project.tab_upload.app_upload import upload

# Explicitly set the paths to the templates and static folders
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='assets',
    static_url_path='/assets'
)
app.secret_key = 'your_secret_key'

app.register_blueprint(dashboard)
app.register_blueprint(upload, url_prefix='/upload')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
