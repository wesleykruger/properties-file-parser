from pathlib import Path
import requests

def load_properties(filepath, sep='=', comment_char='#'):
    props = {}
    with open(filepath, "rt") as f:
        lines = f.readlines()
        # The Cron job will always follow several lines behind a comment line that follows #Group=*;Cron job syntax
        # We want to find one of these comment lines, then find the next uncommented line to pull the job
        look_for_cron = False
        for index, line in enumerate(lines):
            l = line.strip()
            if not look_for_cron:
                if l and l.startswith(comment_char) and l.find('#Group=') == 0 and (l.find(';Cron job') > -1 or l.find(';Cron Job') > -1):
                    look_for_cron = True
            else:
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"')
                    props[key] = value
                    look_for_cron = False
    return props


def translate_crons(cron_list):
    results_dict = {}
    for job in cron_list:
        cron_arr = cron_list[job].split(' ')
        if len(cron_arr) == 6 and not cron_arr[5] == '2099':
            results_dict[job] = convert_value(cron_arr)
            print(job + ' - ' + results_dict[job])
        elif len(cron_arr) == 7 and not cron_arr[6] == '2099':
            results_dict[job] = convert_value(cron_arr)
            print(job + ' - ' + results_dict[job])


def convert_value(arr):
    expression = '+'.join(arr)
    response = requests.get(
    'https://cronexpressiondescriptor.azurewebsites.net/api/descriptor/?expression={}&locale=en-US'.format(expression))
    return response.text[response.text.index(':') + 1 : response.text.index('}') - 1].replace('"', '')


cron_jobs = load_properties(Path('path/to/properties/file'))
translate_crons(cron_jobs)