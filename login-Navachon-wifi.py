#!/usr/bin/python3

import getpass
import requests as req

def cutStr(url, head, tail):
    start = url.find(head) + len(head)
    end = url.find(tail, start)
    result = url[start : end]
    return result

def main():
    entryUrl = 'http://www.google.com'
    username = input('username: ')
    passwd = getpass.getpass('password: ')
    status = 'failed'
    
    while status == 'failed':
        try:
            session = req.Session()
            res = session.get(entryUrl)
            challenge = cutStr(res.url, 'challenge=', '&')
            uamip = cutStr(res.url, 'uamip=', '&')
            uamport = cutStr(res.url, 'uamport=', '&')
            targetUrl = 'http://' + uamip + '/login/?chal=' + challenge + '&uamip=' + uamip + '&uamport=' + uamport + '&uid=' + username + '&pwd=' + passwd + '&save_login=on&login=Login'
            res = session.get(targetUrl)
            res = session.get(res.url)
            status = cutStr(res.url, 'res=', '&')
            print(status)
            if status == 'failed':
                res = session.get('http://' + uamip + '/checktime/')
                submitValue = cutStr(res.text, 'name=\"Submit\" value=\"', '\"')
                res = session.post('http://' + uamip + '/checktime/', data = { 'username' : username,
                                                                               'password' : passwd,
                                                                               'Submit' : submitValue })
                targetUrl = 'http://' + uamip + '/checktime/' + cutStr(res.text, '<a href=\'', '\'')
                res = session.get(targetUrl)
        except Exception as e:
            errorMessage = str(e)
            print(errorMessage)
    return

if __name__ == '__main__':
    main()
