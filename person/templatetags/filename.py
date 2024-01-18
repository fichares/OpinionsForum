import os
import pathlib

from django import template


register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value.file.name)

@register.filter
def extension(value):
    format = ''
    my_file = str(value)
    for e in reversed(my_file):
        if (e != '.'):
            format += e
        else:
            break

    my_extension = format[::-1]

    return my_extension

@register.filter
def check_on_video(value):
    current_format = extension(value)
    video_format = ['MP4', 'AVI', 'MKV', 'ASF', 'GP', 'MOV', 'FLV', 'VRO', 'VOB', 'PS', 'TS', 'SVAF', 'WEBM']
    flag = False
    for e in video_format:
        if e.lower() == current_format:
            flag = True
            break

    return flag

@register.filter
def check_on_pdf(value):
    current_format = extension(value)
    video_format = ['PDF']
    flag = False
    for e in video_format:
        if e.lower() == current_format:
            flag = True
            break

    return flag