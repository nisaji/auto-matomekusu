from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import settings
import sys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
# import requests
from twocaptcha import TwoCaptcha


class AutoMatome:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--window-size=3840,2160')
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=self.options)
        self.settings = settings
        self.matomekusu_login_url = settings.MATOMEKUSU_URL
        self.matomekusu_email = settings.MATOMEKUSU_EMAIL
        self.matomekusu_password = settings.MATOMEKUSU_PASSWD
        self.ita = sys.argv[1]
        self.thread_dict = {}
        self.loop_time = 10
        self.num = 1
        self.editor = "https://2mtmex.com/editor"
        self.wordpress_url = settings.WORDPRESS_ADMIN_URL
        self.wordpress_user = settings.WORDPRESS_USER
        self.wordpress_password = settings.WORDPRESS_PASSWD
        self.ita_news = settings.NEWS
        self.ita_news_plus = settings.NEWS_PLUS
        self.ita_live_plus = settings.LIVE_PLUS
        self.two_captcha_key = settings.TWOCAPTCHA_API
        self.data_site_key = settings.GOOGLE_SITE_KEY
        self.solver = TwoCaptcha(self.two_captcha_key)
        print("Automatome init end")

    def set_ita_url(self):
        ita = self.ita
        ita = sys.argv[1]
        if ita == "newsplus":
            ITA_URL = self.ita_news_plus
        elif ita == "liveplus":
            ITA_URL = self.ita_live_plus
        elif ita == "news":
            ITA_URL = self.ita_news
        else:
            print("wrong ITA value set")
            exit()
        return ITA_URL

    def get_soup(self, ITA_URL):
        ita = ITA_URL
        html = urlopen(ita)
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def fetch_items(self, soup):
        table = soup.find("table", {"class": "forces first_f"})
        rows = table.findAll("td", {"class": "title"})
        for row in rows:
            # タイトルの整形
            title = re.sub('★\d*', '', row.get_text())
            title = re.sub('\[.+?\]', '', title)
            url = row.find('a').get('href')
            self.thread_dict[title] = url
        return

    def pass_recaptcha(self):
        driver = self.driver
        response = self.solver.recaptcha(
            sitekey=self.data_site_key, url=self.matomekusu_login_url, invisible=1)
        code = response['code']
        print(code)
        textarea = driver.find_element_by_id('g-recaptcha-response-100000')
        print(textarea)
        driver.execute_script(f'arguments[0].value = "{code}";', textarea)
        # driver.find_element_by_css_selector('button[type="submit"]').click()
        # result = driver.find_element_by_css_selector(
        #     'body>main>h2:nth-child(3)').text
        # print(result)
        return

    def login_matomekusu(self):
        driver = self.driver
        driver.get(self.matomekusu_login_url)
        driver.implicitly_wait(3)
        print('まとめくすログインページにアクセスしました')
        login_id = driver.find_element_by_name("email")
        login_id.send_keys(self.matomekusu_email)
        driver.implicitly_wait(3)
        password = driver.find_element_by_name("password")
        password.send_keys(self.matomekusu_password)
        driver.implicitly_wait(3)
        # self.pass_recaptcha()
        buttons = driver.find_elements_by_tag_name("button")
        for button in buttons:
            if button.text == "ログイン":
                # random_time = random.randint(5, 10)
                # time.sleep(random_time)
                button.click()
                print("まとめくすログイン中...")
                break
        return

    def set_api(self):
        driver = self.driver
        select = Select(driver.find_element_by_id('registered_api'))
        select.select_by_visible_text(settings.WORDPRESS_DOMAIN)
        driver.find_element_by_xpath("//input[@value='設定']").click()
        print("APIを設定完了")
        return

    def fetch_content(self, title, url):
        driver = self.driver
        # print(thread_dict)
        url_input = driver.find_element_by_id("ready_ourl")
        thread_num_input = driver.find_element_by_id("ready_target")
        url_input.send_keys(url)
        driver.implicitly_wait(3)
        thread_num_input.send_keys("1-100")
        driver.implicitly_wait(3)
        driver.find_element_by_id("ready_get").click()
        time.sleep(10)
        print(f"記事を取得：{title}:{url}")
        return

    def format_content(self):
        driver = self.driver
        driver_action = ActionChains(driver)
        target_title = " レスの一括操作▼ "
        driver_action.move_to_element(driver.find_element_by_xpath(
            "//*[text()='%s']" % target_title)).perform()
        actions = driver.find_elements_by_class_name("deal_button")
        '''
        actions
        [0]全て太字
        [1]全て太字を解除
        [2]全て本文
        [3]全て続きを読む
        [4]全てのレスを選択
        [5]NGレス以外を選択
        [6]全ての選択状態を解除
        [7]ホームに移動
        '''
        actions[0].click()
        action_4 = actions[4]
        # Other element would receive the click の回避
        driver.execute_script('arguments[0].click();', action_4)
        return

    def issue_tag(self, thread_len, num):
        driver = self.driver
        driver.find_element_by_link_text("タグ発行").click()
        title_form = driver.find_element_by_id("pub_title")
        # titleの成形と入力
        title_name = title_form.get_attribute('value')
        title_form.clear()
        title_name = re.sub('★\d', '', title_name)
        title_name = re.sub('\[.+?\]', '', title_name)
        try:
            title_form.send_keys(title_name)
        except WebDriverException as e:
            print(e)
            INPUT_EMOJI = """
                arguments[0].value += arguments[1];
                arguments[0].dispatchEvent(new Event('change'));
                """
            driver.execute_script(INPUT_EMOJI, title_form, title_name)
        driver.find_element_by_link_text("上記の内容でブログに投稿").click()
        time.sleep(4)
        print(f"Wordpressへ送信完了：{title_name} ({num}/{thread_len})")

    def move_home(self):
        driver = self.driver
        editor = self.editor
        driver.get(editor)
        print("記事作成画面に移動")
        return

    def wordpress_login(self):
        driver = self.driver
        # ログイン情報入力
        loop_time = 30
        for _ in range(loop_time):
            try:
                driver.get(self.wordpress_url)
                print('wp-adminにアクセス...')
                # freqently out NoSuchElement
                driver.implicitly_wait(3)
                user_input = driver.find_element_by_id("user_login")
            except NoSuchElementException as e:
                print(e)
                print('wp-adminに再アクセス')
            else:
                break
        else:
            exit
        user_input.send_keys(self.wordpress_user)
        driver.implicitly_wait(3)
        password_input = driver.find_element_by_id("user_pass")
        password_input.send_keys(self.wordpress_password)
        # ログイン処理
        driver.find_element_by_id("wp-submit").click()
        time.sleep(10)
        print("wp-admin:ログイン成功")
        return

    def wordpress_publish(self):
        driver = self.driver
        # 投稿画面に遷移
        driver.get(self.wordpress_url + "/edit.php?post_status=draft")
        # Select 25 items
        driver.find_element_by_id("cb-select-all-1").click()
        # 編集ボタンを押して公開状態にする
        dropdown = driver.find_element_by_id('bulk-action-selector-top')
        select = Select(dropdown)
        select.select_by_visible_text('編集')
        driver.find_element_by_id("doaction").click()
        status = driver.find_element_by_name('_status')
        select = Select(status)
        select.select_by_visible_text('公開済み')
        bulk_edit = driver.find_element_by_id("bulk_edit")
        driver.execute_script('arguments[0].click();', bulk_edit)
        time.sleep(60)
        print("記事の公開を完了")
        return
