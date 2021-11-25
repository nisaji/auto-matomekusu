from automatome import AutoMatome
import ssl
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
ssl._create_default_https_context = ssl._create_unverified_context


def main():
    automatome = AutoMatome()
    ita_url = automatome.set_ita_url()
    print(ita_url)
    soup = automatome.get_soup(ita_url)
    automatome.fetch_items(soup)
    automatome.login_matomekusu()
    # automatome.move_home()
    #   対策: Message: no such element: Unable to locate element
    for _ in range(automatome.loop_time):
        try:
            automatome.set_api()
            break
        except NoSuchElementException as e:
            print(e)
            print("まとめくす再ログイン")
            automatome.login_matomekusu()
    thread_dict = automatome.thread_dict
    thread_len = len(thread_dict)
    num = automatome.num
    for title, url in thread_dict.items():
        automatome.fetch_content(title, url)
        automatome.format_content()
        automatome.issue_tag(thread_len, num)
        num += 1
        for _ in range(automatome.loop_time):
            try:
                automatome.move_home()
                break
            except TimeoutException as e:
                print(e)
    automatome.wordpress_login()
    automatome.wordpress_publish()


if __name__ == "__main__":
    main()
