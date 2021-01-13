import configparser
import menu as menu


if __name__ == '__main__':
    '''
        config.ini 파일을 통해 계정 정보 가져오고
        config.ini 파일이 없으면 프로그램 종료
    '''
    config = configparser.ConfigParser(allow_no_value=True)
    if not config.read('config.ini'):
        # 기존 config 파일이 없을 경우
        print("config.ini 파일이 없습니다...\n")
        config['xing']['id'] = ''
        config['xing']['password'] = ''
        config['xing']['cert_password'] = ''
        config['global']['res_directory'] = './Res'
        config['oracle_db']['user_id'] = ''
        config['oracle_db']['password'] = ''
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        menu.exit_program()

    xing = menu.Xing(config['xing']['id'], config['xing']['password'], config['xing']['cert_password'])
    xing.set_res(config['global']['res_directory'])

    '''
        메뉴 목록을 띄워주고 사용자가 선택하여
        해당하는 메뉴를 실행
    '''
    # 메뉴 목록, 각 함수를 리스트 인자로 갖는다
    menus = [menu.exit_program, xing.get_stock_list]

    while True:
        print("-" * 50)
        print()
        print("실행할 메뉴를 선택하세요\n")
        print("0 : 프로그램 종료")
        print(f"1 : xingAPI를 레지스트리에서 제거")
        print("2: 테스트")
        print()
        try:
            user_input = input(">>> ")
            print()
            menus[int(user_input)]()  # 입력받은 인덱스의 함수 실행
        except (ValueError, IndexError):
            print("유효한 숫자를 입력하세요\n")
