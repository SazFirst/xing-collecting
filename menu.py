import sys
import subprocess
import configparser
import pythoncom
import win32com.client


def exit_program():
    input("Press Enter to exit ")
    sys.exit(0)


def regist_api():
    '''
        xing api를 레지스트리에 등록합니다.
        저장된 위치는 컴퓨터\HKEY_CLASSES_ROOT\CLSID 입니다.
        -s 옵션을 지우고 command 실행 시 결과를 알 수 있습니다.
    '''
    cmd = ['regsvr32', '-s', 'XA_Common.dll']
    subprocess.run(cmd, shell=True, encoding='cp949')
    cmd = ['regsvr32', '-s', 'XA_DataSet.dll']
    subprocess.run(cmd, shell=True, encoding='cp949')
    cmd = ['regsvr32', '-s', 'XA_Session.dll']
    subprocess.run(cmd, shell=True, encoding='cp949')
    print("레지스트리에 XA_Common.dll을 등록합니다.")
    print("레지스트리에 XA_DataSet.dll을 등록합니다.")
    print("레지스트리에 XA_Session.dll을 등록합니다.")
    print()


def unregist_api():
    '''
        레지스트리에 등록된 xing api를 제거합니다.
        -s 옵션을 지우고 command 실행 시 결과를 알 수 있습니다.
    '''
    cmd = ['regsvr32', '/u', '-s', 'XA_Common.dll']
    subprocess.run(cmd, shell=True, encoding='cp949')
    cmd = ['regsvr32', '/u', '-s', 'XA_DataSet.dll']
    subprocess.run(cmd, shell=True, encoding='cp949')
    cmd = ['regsvr32', '/u', '-s', 'XA_Session.dll']
    subprocess.run(cmd, shell=True, encoding='cp949')
    print("레지스트리에 등록된 XA_Common.dll을 제거합니다.")
    print("레지스트리에 등록된 XA_DataSet.dll을 제거합니다.")
    print("레지스트리에 등록된 XA_Session.dll을 제거합니다.")
    print()

    # config.ini의 값 False로 수정
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('config.ini')
    config['global']['xingapi'] = "False"
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def loginTest():
    class XASessionEventHandler:
        login_state = 0

        def OnLogin(self, code, msg):
            if code == "0000":
                print("로그인 성공")
                XASessionEventHandler.login_state = 1
            else:
                print("로그인 실패")

    instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)

    id = "id"
    passwd = "pwd"
    cert_passwd = "crtpwd!"

    instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
    instXASession.Login(id, passwd, cert_passwd, 0, 0)

    while XASessionEventHandler.login_state == 0:
        pythoncom.PumpWaitingMessages()
