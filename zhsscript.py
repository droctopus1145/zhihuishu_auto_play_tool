from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import re

class ZhihuishuHelper:
    def __init__(self):
        # 保持浏览器不随程序结束而关闭
        self.progress=0
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options)
        # 设置显示等待
        self.wait = WebDriverWait(self.driver, 5)

    def handle_quiz_popup(self):
        """检测并处理答题弹窗"""
        try:
            # 1. 检测弹窗容器是否存在
            locator = (By.CSS_SELECTOR, ".ai-test-question-wrapper")
            popup = self.wait.until(EC.presence_of_element_located(locator))
            print("发现弹窗！正在处理...")
            
            # 2. 稍微等待动画完成，重新获取选项以防 Stale 错误
            time.sleep(1) 
            options = self.driver.find_elements(By.CLASS_NAME, "class-question-select")
            
            if len(options) > 1:
                time.sleep(random.uniform(1.5, 3.0)) # 模拟思考
                try:
                    options[1].click() # 点击第二个选项
                    print("已点击选项 B")
                except StaleElementReferenceException:
                    print("元素失效，尝试重新定位点击...")
                    # 重新获取一次
                    self.driver.find_elements(By.CLASS_NAME, "class-question-select")[1].click()

            # 3. 处理后续按钮（采用防御性点击：找不到不报错）
            # 步骤一：点击“完成”或“确定”
            try:
                time.sleep(random.uniform(1.0, 2.0))
                done_btn = self.driver.find_element(By.CSS_SELECTOR, ".submits")
                done_btn.click()
            except NoSuchElementException:
                pass # 没找到就不管它

            # 步骤二：点击关闭叉叉
            try:
                time.sleep(random.uniform(1.0, 2.0))
                close_btn = self.driver.find_element(By.CSS_SELECTOR, ".close-box")
                close_btn.click()
            except NoSuchElementException:
                pass

            try:
                time.sleep(random.uniform(1.0, 2.0))
                close_btn = self.driver.find_element(By.CSS_SELECTOR, ".videoArea")
                close_btn.click()
            except NoSuchElementException:
                pass

            print("当前弹窗处理流程结束。")

        except TimeoutException:
            # 正常情况：没有弹窗
            pass
        except Exception as e:
            # 捕获其他未知错误，防止脚本崩溃
            print(f"处理弹窗时发生异常: {type(e).__name__}")
        
        try:
            # 1. 检测弹窗容器是否存在
            locator = (By.CSS_SELECTOR, ".mastery-level-wrapper")
            popup = self.wait.until(EC.presence_of_element_located(locator))
            print("发现弹窗！正在处理...")
            
            # 步骤二：点击关闭叉叉
            try:
                time.sleep(random.uniform(1.0, 2.0))
                close_btn = self.driver.find_element(By.CSS_SELECTOR, ".close-box")
                close_btn.click()
            except NoSuchElementException:
                pass

            try:
                time.sleep(random.uniform(1.0, 2.0))
                close_btn = self.driver.find_element(By.CSS_SELECTOR, ".videoArea")
                close_btn.click()
            except NoSuchElementException:
                pass
            
            try:
                time.sleep(random.uniform(1.0, 2.0))
                close_btn = self.driver.find_element(By.CSS_SELECTOR, ".nextButton")
                close_btn.click()
            except NoSuchElementException:
                pass

            print("当前弹窗处理流程结束。")
            progress_bar = self.driver.find_element(By.CLASS_NAME, "passTime")

        except TimeoutException:
            # 正常情况：没有弹窗
            pass
        except Exception as e:
            # 捕获其他未知错误，防止脚本崩溃
            print(f"处理弹窗时发生异常: {type(e).__name__}")
        
        try:
            # 1. 定位你想要移上去的对象（比如进度条、头像或隐藏菜单）
            target_element = self.driver.find_element(By.CLASS_NAME, "videoArea")

            # 2. 实例化动作链
            actions = ActionChains(self.driver)

            # 3. 执行“移动到元素”动作
            # move_to_element：将鼠标移到元素的正中心
            actions.move_to_element(target_element).perform()

            # 1. 定位到该进度条元素
            progress_bar = self.driver.find_element(By.CLASS_NAME, "passTime")

            # 2. 获取 style 属性的字符串内容
            style_content = progress_bar.get_attribute("style") 
            print(style_content)
            # 此时 style_content 的内容类似于 "max-width: 100%; width: 31.1475%;"

            # 3. 提取 width 的数值
            # 方法 A：简单的字符串分割（适用于结构固定时）
            match=re.search(r";\swidth:\s*([\d.]+)%", style_content)
            width_percent=float(match.group(1))
            print(f"当前进度：{width_percent}%")
            if width_percent>=90.0 :
                try:
                    time.sleep(random.uniform(1.0, 2.0))
                    close_btn = self.driver.find_element(By.CSS_SELECTOR, ".nextButton")
                    try:
                        close_btn.click()
                    except ElementClickInterceptedException:
                        print("点击被拦截，尝试使用 JS 强制点击...")
                        # 3. 拦截时使用 JS 兜底
                        self.driver.execute_script("arguments[0].click();", close_btn)
                except NoSuchElementException:
                    pass
            elif width_percent<90.0 and width_percent==self.progress :
                try:
                    time.sleep(random.uniform(1.0, 2.0))
                    play_btn = self.driver.find_element(By.CSS_SELECTOR, ".playButton")
                    print("发现意外暂停，正在尝试重新播放")
                    try:
                        play_btn.click()
                    except ElementClickInterceptedException:
                        print("点击被拦截，尝试使用 JS 强制点击...")
                        # 3. 拦截时使用 JS 兜底
                        self.driver.execute_script("arguments[0].click();", play_btn)
                except NoSuchElementException:
                    pass
                print("成功重新播放")
            self.progress=width_percent

        except TimeoutException:
            # 正常情况：没有弹窗
            pass
        except Exception as e:
            # 捕获其他未知错误，防止脚本崩溃
            print(f"处理弹窗时发生异常: {type(e).__name__}")

    def run(self):
        print("监控启动，正在循环扫描页面...")
        while True:
            try:
                # 检查浏览器是否还处于连接状态
                _ = self.driver.current_url
                self.handle_quiz_popup()
            except Exception:
                print("检测到浏览器已关闭或连接断开，脚本停止。")
                break
            
            # 扫描频率不宜过快，0.5-2秒均可
            time.sleep(2)

if __name__ == "__main__":
    helper = ZhihuishuHelper()
    helper.run()