import urllib, re, requests

from robobrowser import RoboBrowser

class QuoraConnectionHandler:
    def __init__(self, logger):
        self.logger = logger
        self.url = "https://www.quora.com"


    def getHmacForLogin(self):
        try:
            with urllib.request.urlopen(self.url) as url:
                data = url.read().decode()
                id_raw = re.search(r'\"login\", \"LoggedOutHomeLogin\",(.*?)\"\",', data).group(1)
                id = id_raw.replace('"', '').replace(',', '').replace(' ', '')
                hmac_array_as_string = re.search(r'\"hmacs\":(.*?)}}', data).group(1)
                single_hmac_raw = re.search(r''+id+'(.*?)\",', hmac_array_as_string).group(1)
                single_hmac_clean = single_hmac_raw.replace('"', '').replace(':','').replace(' ','')
                return single_hmac_clean
        except Exception as e:
            self.logger.commit(2, "QuoraConnectionHandler", "getInstanceVariableForLogin", e)

    def login(self):
        try:
            '''
            hmac = str(self.getHmacForLogin())
            login_url = self.url + "/webnode2/server_call_POST?_h="+hmac+"&_m=do_login"
            data = {"json": '{"args":[],"kwargs":{"email":"user@email.com","password":"password"}}',
            "revision": "",
            "formkey": "",
            "postkey": "",
            "window_id": "broadcast_desktop_uozvrefvyohpsxvs",
            "referring_controller": "index",
            "referring_action": "index",
            "__hmac": "",
            "__method": "do_login",
            "__e2e_action_id": "",
            "js_init": '{"translated_complete_captcha_text":"Please complete the CAPTCHA correctly.","current_url":"https://www.quora.com/?time=1562709759950888&uid=850584414&unh=94973d7f1a9a8bf5bc0b5a84c6e906ad"}',
            "__metadata": "{}"
}
            with requests.Session() as session:
                post = session.post(login_url, data=data)
                print(post.status_code)
            '''
            browser = RoboBrowser(history=True)
            browser.open('https://www.quora.com/')

            browser.get_form

        except Exception as e:
            print("error",e)
            self.logger.commit(2, "QuoraConnectionHandler", "login", e)
