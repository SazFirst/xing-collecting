import win32com.shell.shell as shell
import configparser
import sys
import menu as menu

def exit_program():
    input("Press Enter to exit ")
    quit()
    sys.exit(0)


def uac_require():
    '''
        현재 관리자 권한으로 실행되고 있는지 확인한 다음
        관리자 권한이 아닐경우 관리자 권한을 요청하는 함수입니다.
    '''
    import os
    ASADMIN = 'asadmin'
    try:
        if sys.argv[-1] != ASADMIN:
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            sys.exit()
        return True
    except:
        return False


if __name__ == '__main__':
    uac_require()

    '''
        config.ini 파일을 통해 xingAPI가 레지스트리에 등록되어 있는지 확인
        config.ini이 없으면 새로 만들면서 레지스트리에 자동으로 등록하고
        있는 경우 xingapi값을 확인하여 등록되어 있는지 확인한 후
        등록되어 있지 않으면 사용자에게 등록할건지 묻는다
    '''
    config = configparser.ConfigParser(allow_no_value=True)
    if not config.read('config.ini'):
        # 기존 config 파일이 없을 경우
        print("config.ini 파일을 생성합니다...\n")
        config['global'] = {}
        menu.regist_api()
        config['global']['xingapi'] = "True"
    else:
        # config 파일이 있는 경우 xingAPI가 레지스트리에 등록되어 있는지 확인
        if config['global']['xingapi'] != "True":
            print("xingAPI가 레지스트리에 등록되어 있지 않습니다.")
            print("프로그램을 사용할려면 레지스트리에 등록해야만 합니다.")
            ans = input("xingAPI를 레지스트리에 등록하시겠습니까? (동의하면 y 입력) : ")
            print()

            # 사용자가 레지스트리 등록을 원하지 않는 경우 그냥 프로그램 종료
            if ans != "y":
                print("xingAPI를 레지스트리에 등록하지 않으므로 프로그램을 종료합니다.\n")
                config['global']['xingapi'] = "False"
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                menu.exit_program()
            else:
                menu.regist_api()
                config['global']['xingapi'] = "True"
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    '''
        메뉴 목록을 띄워주고 사용자가 선택하여
        해당하는 메뉴를 실행
    '''
    # 메뉴 목록, 각 함수를 리스트 인자로 갖는다
    menus = [exit_program, menu.unregist_api]

    while True:
        print("-" * 50)
        print()
        print("실행할 메뉴를 선택하세요\n")
        print("0 : 프로그램 종료")
        print(f"1 : xingAPI를 레지스트리에서 제거")
        print()
        try:
            user_input = input(">>> ")
            print()
            menus[int(user_input)]()  # 입력받은 인덱스의 함수 실행
        except (ValueError, IndexError):
            print("유효한 숫자를 입력하세요\n")
