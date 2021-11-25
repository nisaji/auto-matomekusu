from dotenv import load_dotenv
from os.path import join, dirname
import os


load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# matomekusu
MATOMEKUSU_EMAIL = os.environ.get("MATOMEKUSU_EMAIL")
MATOMEKUSU_URL = os.environ.get("MATOMEKUSU_URL")
MATOMEKUSU_PASSWD = os.environ.get("MATOMEKUSU_PASSWD")
# wordpress
WORDPRESS_DOMAIN = os.environ.get("WORDPRESS_DOMAIN")
WORDPRESS_ADMIN_URL = os.environ.get("WORDPRESS_ADMIN_URL")
WORDPRESS_USER = os.environ.get("WORDPRESS_USER")
WORDPRESS_PASSWD = os.environ.get("WORDPRESS_PASSWD")
# 2captha
TWOCAPTCHA_API = os.environ.get("API_KEY")
GOOGLE_SITE_KEY = os.environ.get("GOOGLE_SITE_KEY")
TWOCAPTCHA_URL = "http://2captcha.com/in.php?key=" + TWOCAPTCHA_API + \
    "&method=userrecaptcha&googlekey=" + \
    GOOGLE_SITE_KEY + "&pageurl=" + MATOMEKUSU_URL
# ikioi ranking
NEWS_PLUS = "http://2ch-ranking.net/index.html?board=newsplus"
NEWS = "http://2ch-ranking.net/index.html?board=news"
LIVE_PLUS = "http://2ch-ranking.net/index.html?board=liveplus"
