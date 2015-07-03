#!/usr/bin/env python

__author__ = "jack deloach"

__doc__ = """a wrapper for taskwarrior which extends its functionality in a
variety of ways.

added commands:
bump --
standup --

"""
import sh
import sys
import taskw
import datetime
import subprocess

DEFAULTS = {
    'scheduled': datetime.datetime.today().strftime("%Y-%m-%d"),
    'priority': 'L'
}

def main():
    run_command(sys.argv)

def run_command(args):
    """ takes in the full arglist (sys.argv) and returns a dict with
    """
    if len(args) < 2:
        subprocess.call(['task'])
    elif args[1] == "add":
        task_add(args_to_task_dict(args[2:]))
    elif args[1] == "bump":
        bump()
    elif args[1] == "standup":
        standup()
    elif args[1] == "time":
        if len(args) > 2:
            total_est_task_time(datetime.datetime.strptime(args[2],'%Y-%m-%d').date())
        else:
            total_est_task_time()
    elif len(args) > 2 and args[2] == "open":
        open_task(args[1])
    else:
        subprocess.call(['task'] + sys.argv[1:])

def args_to_task_dict(args):
    ans = {}
    for item in args:
        if item.startswith("+"):
            tag = [item[1:]] #strip the +
            if 'tags' in ans:
                ans['tags'] += tag
            else:
                ans['tags'] = tag
        elif not ':' in item or '\:' in item:
            ans['description'] = item
        else:
            k,v = item.split(':')
            ans[k] = v
    return ans

def task_add(task_dict):
    w = taskw.TaskWarrior()
    output = w.task_add(**inject_defaults(normalize_dict(task_dict, w), DEFAULTS))
    print "Created task %s." % output['id']

def get_string_from_abbrev(abbrev, word_list):
    ml = [word for word in word_list if abbrev in word]
    if len(ml) == 1:
        return ml[0]
    else:
        raise ValueError('Cannot find abbrev "%s" in word list: %s' % abbrev, word_list)

def normalize_dict(task_dict, w):
    skeys = {key for status in w.load_tasks().values() for task in status for key in task.keys()}
    keys = task_dict.keys()
    return {(key if key in skeys else get_string_from_abbrev(key, skeys)):task_dict[key] for key in keys}

def inject_defaults(task_dict, defaults_dict):
    ans = task_dict
    a = set(defaults_dict.keys())
    b = set(task_dict.keys())
    defaults_to_inject = a - (a & b)
    for key in defaults_to_inject:
        ans[key] = DEFAULTS[key]
    return ans

def str_to_datetime(string, format="%Y%m%dT%H%M%SZ"):
    return datetime.datetime.strptime(string, format)

def bump():
    w = taskw.TaskWarrior()
    pending_tasks = [(task['id'], str_to_datetime(task['scheduled']))
                     for task in w.load_tasks()['pending']]
    print "Bringing old tasks up to date."
    y = datetime.datetime.today().year
    m = datetime.datetime.today().month
    d = datetime.datetime.today().day
    today = datetime.datetime(y,m,d)
    for id, date in pending_tasks:
        if date < today:
            _, task = w.get_task(id=id)
            task['scheduled'] = datetime.datetime.today().strftime("%Y-%m-%d")
            try:
                w.task_update(task)
                print "Updated task %s." % id
            except taskw.exceptions.TaskwarriorError, e:
                print "Taskwarrior error on task %s: %s" % (id, e)

def standup():
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    y = datetime.datetime.today().year
    m = datetime.datetime.today().month
    d = datetime.datetime.today().day
    today = datetime.datetime(y,m,d)
    last_workday = today - datetime.timedelta(1 if today.weekday() != 0 else 3)
    print "%s's tasks:" % weekdays[last_workday.weekday()]
    subprocess.call(("task all scheduled:%s" % last_workday.strftime("%Y-%m-%d")).split())
    print "============================================\nToday's tasks:"
    subprocess.call(("task all scheduled:%s -learn -home" % today.strftime("%Y-%m-%d")).split())

def total_est_task_time(date=datetime.datetime.today().date()):
    w = taskw.TaskWarrior()
    todays_tasks = [task for task in w.load_tasks()['pending']
            if datetime.datetime.strptime(task['scheduled'].split('T')[0],
                                          '%Y%m%d').date() == date]
    total_secs = sum([int(task['estimate']) if 'estimate' in task else 0
                     for task in todays_tasks])
    total_hrs = total_secs / 60 / 60
    total_mins = int(((total_secs / 60. / 60.) - total_hrs) * 60)
    print "total task time for date %s is: %s h %s min" % (date.strftime('%Y-%m-%d'), total_hrs, total_mins)

def open_task(task_id):
    """opens any URL found in the description or annotation of a task.
    depends on chrome-cli, which you can install with 'brew install chrome-cli'
    """
    task_id = int(task_id)
    w = taskw.TaskWarrior()
    try:
        task = [task for task in w.load_tasks()['pending']
                if int(task['id']) == task_id][0]
    except IndexError, e:
        print "Task %s does not exist." % task_id
        sys.exit(1)
    try:
        annotations = ' '.join(t['description'] for t in task['annotations']).split()
    except KeyError, e:
        print "No annotations found for this task"
        sys.exit(1)
    urls = []
    for an in annotations:
        if an.startswith('http://') or an.startswith('https://'):
            urls.append(an)

    print "opening %s in new window." % urls[0]
    stdout = sh.chrome_cli('open', urls[0], '-n')
    window_id = int([x.split(':')[1].strip()
                 for x in stdout.split('\n') if 'Id:' in x][0]) - 1
    for url in urls[1:]:
        print "opening %s in new tab." % url
        sh.chrome_cli('open', url, w=window_id)
    sh.chrome_cli('activate', t=window_id+1)
    sys.exit(0)

if __name__ == '__main__':
    main()

