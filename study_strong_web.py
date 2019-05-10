# 2019年05月10日
# 源源源
# 功能：自动化登录学习强国，完成当日任务
# 问题点：因为还在测试，目前尚不知网站任务完成检测机制原理，故而时间周期设置的比较久，后续还在测试，优化ing
# 程序基本功能已经实现，可以使用

from selenium import webdriver
import time

VIDEO_LINK = 'https://www.xuexi.cn/a191dbc3067d516c3e2e17e2e08953d6/b87d700beee2c44826a9202c75d18c85.html?pageNumber=39'  # 其它视频视频链接
TEST_VIDEO_LINK = 'https://www.xuexi.cn/8e35a343fca20ee32c79d67e35dfca90/7f9f27c65e84e71e1b7189b7132b4710.html'  # 新闻联播链接
SCORES_LINK = 'https://pc.xuexi.cn/points/my-points.html'  # 个人分数链接
LOGIN_LINK = 'https://pc.xuexi.cn/points/login.html'  # 学习强国登录链接
ARTICLES_LINK = 'https://www.xuexi.cn/d05cad69216e688d304bb91ef3aac4c6/9a3668c13f6e303932b5e0e100fc248b.html'  # 文章链接

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 设置为开发者模式，防止被各大网站识别为自动化程序
browser = webdriver.Chrome(options=options)
num = 7  # 此处是在确定要打开的基础文章数，在此上加了1个，例如，如果要打开6个，这写7
num_01 = 8  # 此处定义视频打开数量
first_time = 900  # 这里定义的是第一篇文章需要等待的时长，这里单独打开一片是为了防止检测，测试中，尚不清楚检测机制，后期如果没用可以取消
book_time = 30  # 此处定义的是后续文章打开的时间
watch_tv_time = 240  # 此处定义需要看的视频时间，全部定义的只播放4分钟就打开新的视频链接


def login_simulation():  # 模拟登陆学习强国网站
    browser.get(LOGIN_LINK)
    browser.maximize_window()
    browser.execute_script("var q=document.documentElement.scrollTop=1000")
    time.sleep(10)  # 设置等待二维码扫描的时间
    # browser.set_window_size(500, 1000) #如果觉得浏览器太大可以设置，免得影响界面，这里是设置浏览器大小的界面


def read_book():  # 阅读文章的方法
    browser.get(ARTICLES_LINK)  # 打开文章链接
    time.sleep(3)
    articles = browser.find_elements_by_xpath(
        "//div[@class='_3wnLIRcEni99IWb4rSpguK']/div[@class='text-link-item-title']/div[@class='text-wrap']")
    articles_001 = articles[0]
    articles_001.click()
    handles = browser.window_handles  # 定义窗口位置
    browser.switch_to.window(handles[-1])  # 确定为最后一个窗口
    browser.execute_script("var q=document.documentElement.scrollTop=1000")  # 滑动界面，因为不明白任务检测机制，所以滑动一下界面，保险起见
    time.sleep(first_time)
    browser.close()
    handles = browser.window_handles  # 定义窗口位置
    browser.switch_to.window(handles[0])  # 确定窗口位置
    articles = browser.find_elements_by_xpath(
        "//div[@class='_3wnLIRcEni99IWb4rSpguK']/div[@class='text-link-item-title']/div[@class='text-wrap']")
    articles_01 = articles[1:num]
    for i in articles_01:
        i.click()
        time.sleep(book_time)


def watch_new():  # 打开新闻联播的方法
    browser.get(TEST_VIDEO_LINK)
    video_duration_str = browser.find_element_by_xpath("//span[@class='duration']").get_attribute('innerText')
    video_duration = int(video_duration_str.split(':')[0]) * 60 + int(video_duration_str.split(':')[1])
    handles = browser.window_handles  # 定义窗口位置
    browser.switch_to.window(handles[0])  # 确定为最后一个窗口
    time.sleep(video_duration + 5)  # 根据新闻联播时长来睡眠等待，确保视频播放完毕


def watch_tv():  # 查看其它视频的方法
    browser.get(VIDEO_LINK)
    time.sleep(3)
    handles = browser.window_handles  # 定义窗口位置
    browser.switch_to.window(handles[0])  # 确定为最后一个窗口
    videos = browser.find_elements_by_xpath(
        "//div[@class='_3wnLIRcEni99IWb4rSpguK']/div[@class='text-link-item-title']/div[@class='text-wrap']")
    videos_01 = videos[0:num]
    for i in videos_01:
        i.click()
        time.sleep(watch_tv_time)


def get_scores():  # 获得积分方法
    browser.get(SCORES_LINK)
    time.sleep(3)
    handles = browser.window_handles  # 定义窗口位置
    browser.switch_to.window(handles[0])  # 确定为最后一个窗口
    gross_score = browser.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]") \
        .get_attribute('innerText')
    today_score = browser.find_element_by_xpath("//span[@class='my-points-points']").get_attribute('innerText')
    print("当前总积分：" + str(gross_score))
    print("今日积分：" + str(today_score))
    print("获取积分完毕，今日学习已经完成，即将退出，余下积分请参与答题获得\n")


if __name__ == '__main__':
    login_simulation()  # 模拟登录
    read_book()  # 阅读文章
    watch_new()  # 观看新闻视频
    watch_tv()  # 观看视频
    get_scores()  # 获得今日积分
    browser.close()  # 关闭界面，并退出浏览器
    browser.quit()
