from typing import List
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec

class ClickStep:
    def __init__(self, selector: str):
        self.selector = selector
        
class InputStep:
    def __init__(self, selector: str="", input =""):
        self.selector = selector
        self.input = input

class ScriptStep:
    def __init__(self, script="", args=[]):
        self.args = args
        self.script = script

SETUP_MODE = "setup"
MACRO_MODE = "mode"
SEAL_MODE = "seal"
NO_MODE = "no_mode"

class Task:
    def __init__(self, url=""):
        self._url = url
        self.setup = []
        self.macro = []
        self.seal = []
        self.recording_mode = SETUP_MODE
        self._repeat_macro_count = 1
        
    def start_setup(self):
        self.recording_mode = SETUP_MODE
        
    def start_macro(self):
        self.recording_mode = MACRO_MODE
        
    def start_seal(self):
        self.recording_mode = SEAL_MODE
        
    def finish(self):
        self.recording_mode = NO_MODE
            
    def add_click_step(self, selector: str):
        if self.recording_mode == SETUP_MODE:
            self.setup.append(ClickStep(selector))
        elif self.recording_mode == MACRO_MODE:
            self.macro.append(ClickStep(selector))
        elif self.recording_mode == SEAL_MODE:
            self.seal.append(ClickStep(selector))
            
    def add_input_step(self, selector: str, input: str):
        if self.recording_mode == SETUP_MODE:
            self.setup.append(InputStep(selector, input))
        elif self.recording_mode == MACRO_MODE:
            self.macro.append(InputStep(selector, input))
        elif self.recording_mode == SEAL_MODE:
            self.seal.append(InputStep(selector, input))
            
    def add_script_step(self, script: str, args: List[str | int]):
        if self.recording_mode == SETUP_MODE:
            self.setup.append(ScriptStep(script, args))
        if self.recording_mode == MACRO_MODE:
            self.macro.append(ScriptStep(script, args))
        if self.recording_mode == SEAL_MODE:
            self.seal.append(ScriptStep(script, args))

    @property
    def repeat_macro_count(self):
        return self._repeat_macro_count
        
    @repeat_macro_count.setter
    def repeat_macro_count(self, value):
        self._repeat_macro_count = value
    @property
    def steps(self):
        return {'setup': self.setup, 'macro': self.macro, 'seal': self.seal}

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value 


def get_visible_element(driver, selector: str, timeout=10):
    return WebDriverWait(driver, timeout).until(
        Ec.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )

def execute_step(driver: Chrome, step: any):
    if isinstance(step, ClickStep):
        element = get_visible_element(driver, step.selector)
        element.click()
    elif isinstance(step, InputStep):
        element = get_visible_element(driver, step.selector)
        element.send_keys(step.input)
    elif isinstance(step, ScriptStep):
        get_visible_element(driver, step.args[0])
        driver.execute_script(step.script, step.args)

class Session:
    def __init__(self, options: List[str]=[]):
        if len(options)!=0:
            chrome_options = ChromeOptions()
            for i in options:
                chrome_options.add_argument("--"+i)

        self.driver = Chrome(options=chrome_options)
        self.driver.implicitly_wait(20)
        
    def execute_task(self, task: Task):
        self.driver.get(task.url)
        task_steps = task.steps
        for step in task_steps['setup']:
            execute_step(self.driver, step)
        for _ in range(task.repeat_macro_count):
            for step in task_steps['macro']:
                execute_step(self.driver, step)
        for step in task_steps['seal']:
            execute_step(self.driver, step)
    def close(self):
        self.driver.quit()

email = "2001031200507@ofppt-edu.ma"
password = "Ccox@10113"
ofppt_langues = "https://app.ofppt-langues.ma/gw/api/saml/init?idp=https://sts.windows.net/dae54ad7-43df-47b7-ae86-4ac13ae567af/"
ofppt_langues_task = Task(ofppt_langues)

ofppt_langues_task.start_setup()
ofppt_langues_task.add_input_step("#i0116", email)
ofppt_langues_task.add_click_step("#idSIButton9")
ofppt_langues_task.add_input_step("#i0118", password)
ofppt_langues_task.add_click_step("#idSIButton9")
ofppt_langues_task.add_click_step("#cancelLink")        
ofppt_langues_task.add_click_step("#otherTileText")
ofppt_langues_task.add_input_step("#i0116", email)
ofppt_langues_task.add_click_step("#idSIButton9")
ofppt_langues_task.add_input_step("#i0118", password)
ofppt_langues_task.add_click_step("#idSIButton9")
ofppt_langues_task.add_click_step("#idSIButton9")
ofppt_langues_task.add_click_step(".lesson-card-container-is-active > div:nth-child(1)")
ofppt_langues_task.start_macro()
ofppt_langues_task.add_click_step(".lesson-menu-activities-list > li:nth-child(1)")
ofppt_langues_task.add_script_step('''
window.setTimeout(()=>{}, 15000);
let callback = arguments[arguments.length-1];
let videoId = arguments[0];
let videoElement = document.querySelector(videoId);;
videoElement.play();
window.setTimeout(()=>{
    callback('done');
}, (videoElement.durration+5)*1000);
''', [".plyr__video-wrapper > video:nth-child(1)"])
ofppt_langues_task.add_click_step(".center-content")
ofppt_langues_task.repeat_macro_count = 100
ofppt_langues_task.finish()



if __name__ == "__main__":
    session = Session(["mute-audio"])
    session.execute_task(ofppt_langues_task)
    session.close()

