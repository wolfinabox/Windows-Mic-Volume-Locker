import os,subprocess
from subprocess import CREATE_NO_WINDOW
import time
from infi.systray import SysTrayIcon
from utils import local_path,script_dir
import tkinter as tk
import tkinter.simpledialog
import json
resource_dir=local_path('resources')
NIRCMDC_PATH=os.path.join(resource_dir,'nircmdc.exe')
CONFIG_PATH=os.path.join(script_dir(),'config.json')
CONFIG={}
DEFAULT_CONFIG={
    'volume_percent':75,
    'time_between_runs':0.5
}
STOP=False
def _on_quit(systray):
    global STOP
    STOP=True

def _on_change_vol_click(systray):
    global CONFIG
    root=tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    tmp=tkinter.simpledialog.askinteger(title="Change Volume",
                                  prompt="Volume to limit to:",minvalue=0,maxvalue=100,initialvalue=CONFIG['volume_percent'])
    if tmp is not None:
        CONFIG['volume_percent']=tmp
        save_config()

    root.destroy()

def load_config():
    global CONFIG
    if not os.path.exists(CONFIG_PATH):
        CONFIG=DEFAULT_CONFIG.copy()
        with open(CONFIG_PATH,'w') as f:
            json.dump(CONFIG,f)
    else:
        with open(CONFIG_PATH,'r') as f:
            CONFIG=json.load(f)

def save_config():
    with open(CONFIG_PATH,'w') as f:
        json.dump(CONFIG,f)

load_config()
menu_options = (('Change Volume',None, _on_change_vol_click),)
sys_tray=SysTrayIcon(os.path.join(resource_dir,'icon.ico'),'Mic Volume Fixer',menu_options,on_quit=_on_quit)
sys_tray.start()


process:subprocess.Popen=None
while not STOP:
    start=time.time()
    # print(CONFIG['volume_percent'])
    cmd=f'{NIRCMDC_PATH} setsysvolume {int(65535*(CONFIG["volume_percent"]/100))} default_record'
    process=subprocess.Popen(cmd,stdout=None,stderr=None,creationflags = CREATE_NO_WINDOW)
    end=time.time()
    sleep_time=CONFIG['time_between_runs']-(end-start)
    if sleep_time>0:
        # print(f'Sleeping {sleep_time}')
        time.sleep(sleep_time)