import json
import tkinter
import threading
import requests
class music_gui:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('QQ音乐专辑下载器')
        self.root.geometry('605x480')
        self.root.attributes("-alpha", 1)
        self.tmp_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=57023280141677220&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={}&g_tk=5381&loginUin=2268598464&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"
        #self.song_name = ''
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Referer": "https://y.qq.com/portal/player.html"
        }
        #控制窗口大小是否可变
        self.root.resizable(True, True)

        self.L1 = tkinter.Label(self.root, text='请输入您想下载的专辑中任意一首歌曲的名称：')
        self.L1.place(x=20, y=5)

        self.L2 = tkinter.Label(self.root, text=' © copyright 何同学')
        self.L2.place(x=400, y=438)

        self.photo = tkinter.PhotoImage(file='1.gif')

        self.L3 = tkinter.Label(self.root, text='作者QQ: 2268598464')
        self.L3.place(x=400, y=460)

        self.L4 = tkinter.Label(self.root, text='xx',image = self.photo)
        self.L4.place(x=530, y=410)

        self.L5 = tkinter.Label(self.root, text='打赏作者: >>>>>>>')
        self.L5.place(x=400, y=420)

        self.E1 = tkinter.Entry(self.root)
        self.E1.place(x=270, y=6)

        self.t = tkinter.Text(self.root, height=28)
        self.t.place(x=20, y=40)

        self.b = tkinter.Button(self.root, text="下载", command=self.parse_musci_name)
        self.b.place(x=430, y=0)
        self.root.mainloop()

    def parse_musci_name(self):
        song_name = self.E1.get()
        my_thread = threading.Thread(target=self.my_thread_func, args=(song_name,))
        my_thread.start()

    def my_thread_func(self, song_name):
        url = self.tmp_url.format(song_name)
        r = requests.get(url)
        r = json.loads(r.content.decode("utf-8"))
        self.albummid = r["data"]["song"]["list"][0]['album']['mid']  # 获取专辑ID
        self.song_dict_url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?ct=24&albummid=" + self.albummid + "&g_tk=5381&loginUin=2268598464&hostUin=0&format=j"
        # 1.获取歌曲所在专辑信息
        song_dict = self.get_song_dict(self.song_dict_url)
        # 2.获取专辑歌曲列表
        song_list = self.get_song_list(song_dict)
        for song in song_list:
            # 3.获取专辑中每一首歌的真实url的信息
            song_real_url = self.get_real_url(song["songmid"])
            # 4.解析真实地址
            content = self.parse_url(song_real_url)
            # 5.保存歌曲到本地
            self.write_to_file(content, song["name"])

    def get_song_dict(self,dict_url):
        r = requests.get(dict_url, headers = self.headers)
        song_dict = json.loads(r.content.decode("utf-8"))
        return song_dict

    def get_song_list(self,song_dict):
        song_list = song_dict["data"]["list"]
        new_song_list = [{"name": song["songname"], "songmid": song["songmid"]} for song in song_list]
        return new_song_list

    def get_real_url(self,songmid):
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey5934270628479392&g_tk=5381&loginUin=2268598464&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data={"req":{"module":"CDN.SrfCdnDispatchServer","method":"GetCdnDispatch","param":{"guid":"9159363373","calltype":0,"userip":""}},"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"9159363373","songmid":["' + songmid + '"],"songtype":[0],"uin":"123456","loginflag":1,"platform":"20"}},"comm":{"uin":"123456","format":"json","ct":24,"cv":0}}'
        r = requests.get(url, headers=self.headers)
        song_dict = json.loads(r.content.decode("utf-8"))
        sip = song_dict["req_0"]["data"]["sip"][0]
        purl = song_dict["req_0"]["data"]["midurlinfo"][0]["purl"]
        url = sip + purl
        return url

    def parse_real_url(self,song_real_url):
        r = requests.get(song_real_url, headers = self.headers)
        return r.content

    def parse_url(self,song_real_url):
        r = requests.get(song_real_url,headers = self.headers)
        return r.content

    def write_to_file(self,content,song_name):
        with open(song_name + '.m4a', "wb") as f:
            f.write(content)
            self.t.insert('insert',song_name + '.m4a下载成功'+'\n')

if __name__ == "__main__":
    a = music_gui()
