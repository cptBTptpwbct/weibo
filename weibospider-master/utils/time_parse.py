import datetime

def timeParse(str):
    print(str)
    now_time = datetime.datetime.now()
    if str.find('秒钟前')>=0:
        return now_time.strftime('%Y-%m-%d %H:%M')
    if str.find("今天")>=0:
        return now_time.strftime("%Y-%m-%d")+str.replace('今天', '')
    if str.find('分钟前')>=0:
        yes_time = now_time + datetime.timedelta(minutes=0-int(str.replace('分钟前', '')))
        return yes_time.strftime('%Y-%m-%d %H:%M')
    if str.find("201")>=0:
        return str
    return now_time.strftime('%Y-')+str



