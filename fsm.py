from transitions.extensions import GraphMachine

from utils import send_text_message,send_button_message
import requests
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    def is_going_to_menu(self,event):
        text = event.message.text
        return text.lower() == "menu"
    def is_going_to_cal_drink_calories(self, event):
        text = event.message.text
        return text.lower() == "計算卡路里"
    def is_going_to_tea_base(self, event):
        text = event.message.text
        return text.lower() == "茶底"
    def is_going_to_tea(self, event):
        global count,text_tmp
        text = event.message.text
        text_tmp='茶'
        return text.lower() == "茶"
    def is_going_to_yakult(self, event):
        global count,text_tmp
        text = event.message.text
        text_tmp='多多'
        return text.lower() == "多多"
    def is_going_to_milk(self, event):
        global count,text_tmp
        text = event.message.text
        text_tmp='鮮奶'
        return text.lower() == "鮮奶"  
    def is_going_to_sugar_content(self, event):
        text = event.message.text
        return text.lower() == "糖度"
    def is_going_to_sugar_free(self, event):
        global count,text_tmp
        text = event.message.text
        if(text_tmp=='茶'):
            count=0
        elif(text_tmp=='多多'):
            count=135
        elif(text_tmp=='鮮奶'):
            count=145
        return text.lower() == "無糖"
    def is_going_to_half_sugar(self, event):
        global count,text_tmp
        text = event.message.text
        if(text_tmp=='茶'):
            count=100
        elif(text_tmp=='多多'):
            count=235
        elif(text_tmp=='鮮奶'):
            count=245
        return text.lower() == "半糖"
    def is_going_to_all_sugar(self, event):
        global count,text_tmp
        text = event.message.text
        if(text_tmp=='茶'):
            count=210
        elif(text_tmp=='多多'):
            count=335
        elif(text_tmp=='鮮奶'):
            count=345
        return text.lower() == "全糖"
    def is_going_to_ingredients(self, event):
        text = event.message.text
        return text.lower() == "配料"
    def is_going_to_fairy_grass(self, event):
        global count,text_tmp
        text = event.message.text
        count=count+35
        return text.lower() == "仙草"
    def is_going_to_coconut(self, event):
        global count,text_tmp
        text = event.message.text
        count=count+65
        return text.lower() == "椰果"
    def is_going_to_pearl(self, event):
        global count,text_tmp
        text = event.message.text
        count=count+220
        return text.lower() == "珍珠"
    def is_going_to_all_calories(self, event):
        text = event.message.text
        return text.lower() == "計算熱量" 
    def is_going_to_food_recommend(self, event):
        text = event.message.text
        return text.lower() == "美食推薦" 
    def is_going_to_tainan_food(self, event):
        text = event.message.text
        return text.lower() == "台南美食"
    def is_going_to_chiayi_food(self, event):
        text = event.message.text
        return text.lower() == "嘉義美食"
    def is_going_to_kaohsiung_food(self, event):
        text = event.message.text
        return text.lower() == "高雄美食"
    def is_going_to_cancel(self, event):
        text = event.message.text
        return text.lower() == "取消操作" 


    def on_enter_menu(self, event):
        print("in the menu")
        reply_token = event.reply_token
        title='請選擇功能'
        text='選擇『美食推薦』、『計算飲料卡路里』'
        btn = [

            MessageTemplateAction(
                label = '計算卡路里',
                text = '計算卡路里'
            ),
            MessageTemplateAction(
                label = '美食推薦',
                text = '美食推薦'
            ),
        ]
        url = 'https://i.imgur.com/0VtFi00.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
    def on_enter_cal_drink_calories(self, event):
        print("in the 計算")
        reply_token = event.reply_token
        title='請選擇功能'
        text='計算飲料卡路里\n選擇『計算』、『離開』'
        btn = [

            MessageTemplateAction(
                label = '計算',
                text = '茶底'
            ),
            MessageTemplateAction(
                label = '離開',
                text = '取消操作'
            ),
        ]
        url = 'https://i.imgur.com/4kvUSO3.png'
        send_button_message(event.reply_token, title, text, btn, url)
    def on_enter_tea_base(self, event):
        print("in the 計算茶底")
        """send_text_message(event.reply_token, '請問茶底?\n(請輸入選項:茶、多多、鮮奶、奶茶)')"""
        reply_token = event.reply_token
        title='請選擇茶底'
        text='茶底種類\n『茶』、『多多』、『鮮奶』、『離開』'
        btn = [

            MessageTemplateAction(
                label = '茶',
                text = '茶'
            ),
            MessageTemplateAction(
                label = '多多',
                text = '多多'
            ),
            MessageTemplateAction(
                label = '鮮奶',
                text = '鮮奶'
            ),
            MessageTemplateAction(
                label = '離開',
                text = '取消操作'
            ),
        ]
        url = 'https://i.imgur.com/xV37B43.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
    def on_enter_tea(self, event):
        print("in the 茶")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<糖度>")
    def on_enter_yakult(self, event):
        print("in the 多多")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<糖度>")
    def on_enter_milk(self, event):
        print("in the 鮮奶")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<糖度>")
    def on_enter_sugar_content(self, event):
        print("in the 計算糖度")
        """send_text_message(event.reply_token, '請問糖度?\n(請輸入選項:無糖、微糖、半糖、少糖、全糖)')"""
        reply_token = event.reply_token
        title='請選擇糖度'
        text='請選擇糖度多寡\n『無糖』、『半糖』、『全糖』'
        btn = [

            MessageTemplateAction(
                label = '無糖',
                text = '無糖'
            ),
            MessageTemplateAction(
                label = '半糖',
                text = '半糖'
            ),
            MessageTemplateAction(
                label = '全糖',
                text = '全糖'
            ),
            MessageTemplateAction(
                label = '離開',
                text = '取消操作'
            ),
        ]
        url = 'https://i.imgur.com/RuBXJ6Z.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
    def on_enter_sugar_free(self, event):
        print("in the 無糖")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<配料>")
    def on_enter_half_sugar(self, event):
        print("in the 半糖")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<配料>")
    def on_enter_all_sugar(self, event):
        print("in the 全糖")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<配料>")
    def on_enter_ingredients(self, event):
        print("in the 計算配料")
        """send_text_message(event.reply_token, '請問加料?\n(請輸入選項:仙草、椰果、珍珠)')"""
        reply_token = event.reply_token
        title='請選擇配料'
        text='請選擇糖度多寡\n『仙草』、『椰果』、『珍珠』'
        btn = [

            MessageTemplateAction(
                label = '仙草',
                text = '仙草'
            ),
            MessageTemplateAction(
                label = '椰果',
                text = '椰果'
            ),
            MessageTemplateAction(
                label = '珍珠',
                text = '珍珠'
            ),
            MessageTemplateAction(
                label = '離開',
                text = '取消操作'
            ),
        ]
        url = 'https://i.imgur.com/kU2nCgg.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
    def on_enter_fairy_grass(self, event):
        print("in the 仙草")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<計算熱量>")
    def on_enter_coconut(self, event):
        print("in the 椰果")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<計算熱量>")
    def on_enter_pearl(self, event):
        print("in the 珍珠")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入<計算熱量>")
    def on_enter_all_calories(self, event):
        global count
        print("in the 計算熱量")
        reply_token = event.reply_token
        text="熱量: "+str(count)+" kcal"
        send_text_message(event.reply_token, text)
        self.go_back()
    def on_enter_food_recommend(self,event):
        print("in the 美食推薦")
        reply_token = event.reply_token
        title='請選擇地區'
        text='『台南』、『嘉義』、『高雄』'
        btn = [

            MessageTemplateAction(
                label = '台南',
                text = '台南美食'
            ),
            MessageTemplateAction(
                label = '嘉義',
                text = '嘉義美食'
            ),
            MessageTemplateAction(
                label = '高雄',
                text = '高雄美食'
            ),
        ]
        url = 'https://i.imgur.com/Ip2CeTF.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
    def on_enter_tainan_food(self,event):
        print("in the 台南美食")
        reply_token = event.reply_token
        send_text_message(reply_token, "=>https://www.youtube.com/watch?v=96evX6lwprQ&t=9s\n=>https://www.youtube.com/watch?v=K3aygxGsBSM\n=>https://www.youtube.com/watch?v=k4NlCMFw-F8\n=>https://www.youtube.com/watch?v=qHNQTnoNe8s\n=>https://www.youtube.com/watch?v=vNBrgAjVQAw")
        self.go_back()
    def on_enter_kaohsiung_food(self,event):
        print("in the 高雄美食")
        reply_token = event.reply_token
        send_text_message(reply_token, "=>https://www.youtube.com/watch?v=An85w3HW_mE\n=>https://www.youtube.com/watch?v=asoG2IIFClo\n=>https://www.youtube.com/watch?v=ETtJ1Xy8Pn4\n=>https://www.youtube.com/watch?v=h5Z2U19R2Hs&t=31s\n=>https://www.youtube.com/watch?v=ZKDx2YXodog")
        self.go_back()  
    def on_enter_chiayi_food(self,event):
        print("in the 嘉義美食")
        reply_token = event.reply_token
        send_text_message(reply_token, "=>https://www.youtube.com/watch?v=VfGerukGTQI\n=>https://www.youtube.com/watch?v=T7O7NARUvVE\n=>https://www.youtube.com/watch?v=-Tem8CylLc8\n=>https://www.youtube.com/watch?v=g5L8BOoE1vE\n=>https://www.youtube.com/watch?v=KO_RECWup3Y")
        self.go_back()     
    def on_enter_cancel(self, event):
        print("in the cancel")
        reply_token = event.reply_token
        send_text_message(reply_token, "離開並回到User")
        self.go_back()  

    def on_exit_all_calories(self):
        print("Leaving all_calories")
    def on_exit_cancel(self):
        print("Leaving cancel") 


 