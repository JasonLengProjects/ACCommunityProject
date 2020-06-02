from flask import Flask

app = Flask(__name__)


from ACCommunity.core.views import core
from ACCommunity.error_pages.handlers import error_pages
app.register_blueprint(core)
app.register_blueprint(error_pages)



