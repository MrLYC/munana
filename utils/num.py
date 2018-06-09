# coding: utf-8

import re

from pycnnum import cn2num

num_re = re.compile(r"(?P<num>\d+)")
cnnums = u"〇零一二两三四五六七八九十百千万壹贰兩叁肆伍陆柒捌玖拾佰仟萬貳參陸亿兆京垓秭穰沟涧正载亿兆京垓秭穰沟涧正载"
cnnum_re = re.compile(r"(?P<num>(?:%s)+)" % "|".join(cnnums))


def convert_index(content):
    match = num_re.search(content)
    if match:
        result = match.groupdict()
        return int(result["num"])

    match = cnnum_re.search(content)
    if match:
        result = match.groupdict()
        content = result["num"]
    try:
        return cn2num(content)
    except:
        return 0