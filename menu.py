import sys
import pythoncom
import win32com.client

''' py2exe를 사용할 경우 필요
    if win32com.client.gencache.is_readonly == True:
        # allow gencache to create the cached wrapper objects
        win32com.client.gencache.is_readonly = False
        # under p2exe the call in gencache to __init__() does not happen
        # so we use Rebuild() to force the creation of the gen_py folder
        win32com.client.gencache.Rebuild()
'''


def exit_program():
    input("Press Enter to exit ")
    sys.exit(0)


class Xing:
    class XASessionEventHandler:
        login_state = 0

        def OnLogin(self, code, msg):
            if code == "0000":
                print("로그인 성공")
                Xing.XASessionEventHandler.login_state = 1
            else:
                print("로그인 실패: ", code)
                exit_program()

    class XAQueryEventHandlerT8430:
        query_state = 0

        def OnReceiveData(self, code):
            Xing.XAQueryEventHandlerT8430.query_state = 1

    def __init__(self, id, password, cert_password):
        self.__id = id
        self.__password = password
        self.__cert_password = cert_password
        self.res_dir = "./Res"

        instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", Xing.XASessionEventHandler)
        instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
        instXASession.Login(self.__id, self.__password, self.__cert_password, 0, 0)

        while Xing.XASessionEventHandler.login_state == 0:
            pythoncom.PumpWaitingMessages()

    def set_res(self, res_dir):
        self.res_dir = res_dir

    def get_stock_list(self):
        # ----------------------------------------------------------------------------
        # T8430
        # ----------------------------------------------------------------------------
        instXAQueryT8430 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", Xing.XAQueryEventHandlerT8430)
        instXAQueryT8430.ResFileName = self.res_dir + "/t8430.res"

        instXAQueryT8430.SetFieldData("t8430InBlock", "gubun", 0, 0)
        instXAQueryT8430.Request(0)

        while Xing.XAQueryEventHandlerT8430.query_state == 0:
            pythoncom.PumpWaitingMessages()

        count = instXAQueryT8430.GetBlockCount("t8430OutBlock")
        for i in range(count):
            hname = instXAQueryT8430.GetFieldData("t8430OutBlock", "hname", i)
            shcode = instXAQueryT8430.GetFieldData("t8430OutBlock", "shcode", i)
            expcode = instXAQueryT8430.GetFieldData("t8430OutBlock", "expcode", i)
            etfgubun = instXAQueryT8430.GetFieldData("t8430OutBlock", "etfgubun", i)
            print(i, hname, shcode, expcode, etfgubun)
