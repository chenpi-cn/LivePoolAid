from Tkinter import *
from VideoCapture import CameraTracking
import thread

settings_vars = [
    'canny_threshold1',
    'canny_threshold2',
    'hough_circles_dp',
    'hough_circles_minDist',
    'hough_circles_param1',
    'hough_circles_param2',
    'hough_circles_minRadius',
    'hough_circles_maxRadius',
    'hough_lines_rho',
    'hough_lines_theta',
    'hough_lines_threshold',
    'hough_lines_minLineLength',
    'hough_lines_maxLineGap',
    'cue_line_slope',
    'cue_line_dist_max',
    'cue_line_dist_min',
    'circle_validator_frames',
    'circle_validator_overlap',
    'circle_validator_delta_x',
    'circle_validator_delta_y',
    'circle_validator_delta_radius',
    'line_validator_frames',
    'line_validator_overlap',
    'rotate_angle',
]

settings = []
root = None
tracker = None
images = None

def main():
    global root
    global tracker
    tracker = CameraTracking()
    root = Tk()

    initWindow(root)
    initUI(root)
    thread.start_new_thread(execute_computer_vision, ())
    root.after(25, draw_loop)
    root.mainloop()

def initWindow(root):
    root.geometry('400x800+100+100')
    root.title('Live Pool Aid')

def initUI(root):
    global lines_checkbox
    global circles_checkbox
    lines_checkbox = IntVar()
    circles_checkbox = IntVar()

    for i in range(len(settings_vars)):
        settings.append(Setting(root, i, settings_vars[i]))

    Label(root, text='Lines').grid(row=len(settings_vars))
    Label(root, text='Circles').grid(row=len(settings_vars) + 1)
    Checkbutton(root, variable=lines_checkbox).grid(row=len(settings_vars), column=1)
    Checkbutton(root, variable=circles_checkbox).grid(row=len(settings_vars) + 1, column=1)

    Button(root, text='Update', command=update_callback).grid(row=len(settings_vars) + 2, column=1)

def update_callback():
    print 'Updating...'
    root.after(1, update_settings)

def execute_computer_vision():
    global images
    global tracker
    while True:
        images = tracker.process_video()

def draw_loop():
    global tracker
    global root
    global images
    if images != None:
        tracker.show_image(**images)
        images = None
    root.after(25, draw_loop)


def cv_loop():
    global tracker
    while True:
        tracker.process_video()

def update_settings():
    global tracker
    global lines_checkbox
    global circles_checkbox
    params = {}
    for setting in settings:
        if setting.entry.get() != '' and is_number(setting.entry.get()):
            params[setting.var_name] = setting.entry.get()
    tracker.update_settings(**params)

    tracker.set_lines(not not (lines_checkbox.get()))
    tracker.set_circles(not not (circles_checkbox.get()))

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class Setting:
    def __init__(self, root, num, var_name):
        self.var_name = var_name
        Label(root, text=var_name).grid(row=num)
        self.entry = Entry(root)
        self.entry.grid(row=num, column=1)

if __name__ == '__main__':
    main()
