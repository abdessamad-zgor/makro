import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec

def get_element_until_visible(driver, selector: str, timeout=10):
    return WebDriverWait(driver, timeout).until(
        Ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )
    
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--mute-audio')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

ofppt_langues = "https://app.ofppt-langues.ma/gw/api/saml/init?idp=https://sts.windows.net/dae54ad7-43df-47b7-ae86-4ac13ae567af/"

steps = {
    "enter_email": "#i0116",
    "next_password": "#idSIButton9",
    "enter_password": "#i0118",
    "sign_in": "#idSIButton9",
    "cancel": "#cancelLink",
    "other_account": "#otherTileText",
    "next": "#idSIButton9",
    "submit_again": "#idSIButton9",
    "yes": "#idSIButton9",
    "select_lesson": ".lesson-card-container-is-active > div:nth-child(1)",
    "select_video": ".lesson-menu-activities-list > li:nth-child(1) > altissia-activity-overview-card:nth-child(1) > a:nth-child(1)",
    "video_element": ".media-player-container",
    "mute": "#app-main-content > altissia-app-container > div > main > altissia-app-video-activity > div > div > altissia-media-player > div > div > plyr > div > div.plyr__controls > div.plyr__controls__item.plyr__volume > button",
    "video_id": ".plyr__video-wrapper > video:nth-child(1)",
    "play_btn": "button.plyr__controls__item:nth-child(1)",
    "video_dur": "div.plyr__controls__item:nth-child(3)",
    "continue": ".center-content",
}

email = "email_here@example.com"
password = "password_again"

driver.get(ofppt_langues)
driver.implicitly_wait(30);

try:
    email_input = get_element_until_visible(driver, steps["enter_email"])
    next_password = get_element_until_visible(driver, steps["next_password"])
    email_input.send_keys(email)
    next_password.click()

    password_input = get_element_until_visible(driver, steps["enter_password"])
    submit = get_element_until_visible(driver, steps["sign_in"])   
    password_input.send_keys(password)
    submit.click()

    cancel_btn = get_element_until_visible(driver, steps["cancel"])
    cancel_btn.click()

    different_acc = get_element_until_visible(driver, steps["other_account"])
    different_acc.click()

    email_input = get_element_until_visible(driver, steps["enter_email"])
    email_input.send_keys(email)

    next_btn = get_element_until_visible(driver, steps["next_password"])
    next_btn.click()

    password_input = get_element_until_visible(driver, steps["enter_password"])
    password_input.send_keys(password)

    sign_in_again = get_element_until_visible(driver, steps["submit_again"])
    sign_in_again.click()

    confirm = get_element_until_visible(driver, steps["yes"])
    confirm.click()

    lesson = get_element_until_visible(driver, steps['select_lesson'])
    lesson.click()
    for i in range(100):

        play_video = get_element_until_visible(driver, steps['select_video'])
        play_video.click()
        
        time.sleep(10)
        mute = get_element_until_visible(driver, steps['mute'])
        mute.click()

        durration_span = get_element_until_visible(driver, steps['video_dur']);
        durration = durration_span.get_attribute('innerText')
        dur = durration.split(':')
        dur_to_secs = int(dur[0])*60+int(dur[1])
        print(dur_to_secs)

        play_button = get_element_until_visible(driver, steps['play_btn'])
        play_button.click()

        continue_btn = get_element_until_visible(driver, steps['continue'], timeout=dur_to_secs+5)
        continue_btn.click()

    print("current url: ", driver.current_url)

except Exception as e:
    print(e)

