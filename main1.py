import json
import datetime
import random
import requests.exceptions

import pyrebase
from google.cloud import storage
from kivy import Config
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.theming import ThemableBehavior
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import IRightBodyTouch, MDList, ThreeLineAvatarIconListItem
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.selectioncontrol import MDCheckbox

from GUI import help_str
import firebase_admin
from firebase_admin import credentials, firestore, storage
import cv2
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
import re


class LogoScreen(Screen):
    pass


class LoginScreen1(Screen):
    pass


class DetectionWindow(Screen):
    pass


class Dashboard(Screen, MDCard):
    text = StringProperty()


class SIGNUPScreen1(Screen):
    pass


class SIGNUPScreen2(Screen):
    pass


class SIGNUPScreen3(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LogoScreen(name='logoscreen'))
sm.add_widget(LoginScreen1(name='loginscreen1'))
sm.add_widget(DetectionWindow(name='detection'))
sm.add_widget(SIGNUPScreen1(name='signupscreen1'))
sm.add_widget(SIGNUPScreen2(name='signupscreen2'))
sm.add_widget(SIGNUPScreen3(name='signupscreen3'))


class MyCheckbox(IRightBodyTouch, MDCheckbox):
    pass


def callbackfun(obj):
    MDApp.get_running_app().root.current = 'loginscreen1'


class SignUPApp(MDApp):
    dialog1: MDDialog
    dialog: MDDialog

    class ContentNavigationDrawer(BoxLayout):
        pass

    class DrawerList(ThemableBehavior, MDList):
        pass

    def __init__(self, **kwargs):
        # self.ref = db.reference()
        super(SignUPApp, self).__init__(**kwargs)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.data = []
        self.checks = []
        self.check_ref = {}
        self.can_party = []
        self.can_cnic = []
        self.sector = ''

        Clock.schedule_once(self.forTowns)
        if not len(firebase_admin._apps):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred,
                                          {'storageBucket': 'electronicvotingsystem-50180.appspot.com'})

        self.db = firestore.client()

        self.bucket = storage.bucket()

        self.strng = Builder.load_string(help_str)
        self.regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        self.count = 0
        try:
            firebaseconfig = {
                "apiKey": "AIzaSyDPUAJhlgVdg3KMlUtsYEonw-EJjSVWNSY",
                "authDomain": "electronicvotingsystem-50180.firebaseapp.com",
                "databaseURL": "https://electronicvotingsystem-50180.firebaseio.com",
                "projectId": "electronicvotingsystem-50180",
                "storageBucket": "electronicvotingsystem-50180.appspot.com",
                "messagingSenderId": "1084797426587",
                "appId": "1:1084797426587:web:90c9c0dd986f0ba0e95f3e",
                "measurementId": "G-11FL2TP01C"
            }
            self.firebase = pyrebase.initialize_app(firebaseconfig)

            self.storage = self.firebase.storage()
        except requests.exceptions.HTTPError as httpErr:
            error_message = json.loads(httpErr.args[1])['error']['message']

    def forTowns(self, *args):
        menu_items = [
            {"text": "Baldia Town"},
            {"text": "Bin Qasim Town"},
            {"text": "Civil Line"},
            {"text": "Clifton Cantonment"},
            {"text": "Garden"},
            {"text": "Gulistan-e-Johar"},
            {"text": "Gadap Town"},
            {"text": "Gulberg Town"},
            {"text": "Gulshan-e-Iqbal Town"},
            {"text": "Jamshed Town"},
            {"text": "Kiamari Town"},
            {"text": "Korangi Town"},
            {"text": "Landhi Town"},
            {"text": "Liaquatabad Town"},
            {"text": "Lyari Town"},
            {"text": "Malir Town"},
            {"text": "Nazimabad Town"},
            {"text": "New Karachi Town"},
            {"text": "North Nazimabad Town"},
            {"text": "North Karachi Town"},
            {"text": "Orangi Town"},
            {"text": "Saddar Town"},
            {"text": "Shah Faisal Town"},
            {"text": "SITE Town"},
            {"text": "Surjani Town"},
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            caller=self.strng.get_screen('signupscreen2').ids.town,
            position="auto",
            width_mult=4,
            callback=self.drop_down

        )
        self.menu.bind(on_release=self.drop_down)

    def drop_down(self, instance):
        self.strng.get_screen('signupscreen2').ids.town.text = instance.text

    def build(self):
        Clock.schedule_once(callbackfun, 4)
        return self.strng

    @staticmethod
    def change_screen(screen):
        sm.current = screen

    @staticmethod
    def signup_win():
        MDApp.get_running_app().root.current = 'signupscreen1'

    def set_time_registration(self):
        doc_ref = self.db.collection('Time').document('Time')
        docs = doc_ref.get()
        startDate = ''
        endDate = ''
        if docs.exists:
            a = docs.to_dict()
            startDate = a['StartDate Registration']
            endDate = a['EndDate Registration']

        year = int(startDate[0:4])
        month = int(startDate[5:7])
        sdate = int(startDate[8:10])
        edate = int(endDate[8:10])
        if datetime.date.today() <= datetime.date(year, month, int(edate)):
            if datetime.date.today() >= datetime.date(year, month, int(sdate)):
                MDApp.get_running_app().root.current = 'signupscreen1'
            else:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Time Error', text='Registration for voting is not started yet. It will'
                                                                ' be available after ' + startDate,
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                MDApp.get_running_app().root.current = 'loginscreen1'
                return
        else:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Time Error', text='Registration for voting has ended. Last date was '
                                                            + endDate, size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'loginscreen1'
            return

    def signup(self):
        self.signupEmail = self.strng.get_screen('signupscreen1').ids.useremail.text
        self.signupCNIC = self.strng.get_screen('signupscreen1').ids.usercnicno.text
        self.signupMobileNo = self.strng.get_screen('signupscreen1').ids.mobilenumber.text
        self.signupName = self.strng.get_screen('signupscreen1').ids.name.text
        self.doc_ref = self.db.collection('Voters').where(u'CNIC', u'==', self.signupCNIC).stream()

        if self.signupName.split() == [] or self.signupEmail.split() == [] or self.signupName.split() == [] or self.signupMobileNo.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'signupscreen1'
            return

        if len(self.signupCNIC) is not 13:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid CNIC', text='Please Enter a Valid CNIC',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'signupscreen1'
            return

        if len(self.signupMobileNo) is not 11:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Mobile Number', text='Please Enter a valid Mobile Number',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'signupscreen1'
            return
        for doc in self.doc_ref:
            a = doc.to_dict()
            list = a['CNIC']
            if self.signupCNIC == list:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Invalid CNIC', text='CNIC Exists', size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                MDApp.get_running_app().root.current = 'signupscreen1'
                return

        if not re.search(self.regex, self.signupEmail):
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Email', text='Please Enter a valid email', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'signupscreen1'
            return

        else:
            MDApp.get_running_app().root.current = 'signupscreen2'

    def id_check(self, id):
        ID = id
        print(ID)

        for doc in self.doc_ref:
            a = doc.to_dict()
            list = a['CNIC']
            if ID == list:
                self.id_check(random.randint(0, 999))
        return ID

    def signup2(self):
        self.signupAddress = self.strng.get_screen('signupscreen2').ids.address.text
        self.signupDOB = self.strng.get_screen('signupscreen2').ids.date_picker.text
        self.signupTown = self.strng.get_screen('signupscreen2').ids.town.text
        self.signupCity = self.strng.get_screen('signupscreen2').ids.city.text
        if self.signupAddress.split() == [] or self.signupTown.split() == []:
            if self.signupDOB.split() == 'Date Of Birth':
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                MDApp.get_running_app().root.current = 'signupscreen2'
                return
        if self.strng.get_screen('signupscreen2').ids.city.text != 'Karachi':
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid City Name', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            return

        for doc in self.doc_ref:
            a = doc.to_dict()
            list = a['CNIC']
            if self.signupCNIC == list:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Invalid CNIC', text='CNIC Exists', size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                MDApp.get_running_app().root.current = 'signupscreen2'
                return

        else:

            NA_240 = ['Clifton Cantonment', 'Landhi Town', 'Korangi Town', 'Kiamari Town',
                      'Lyari Town', 'Bin Qasim Town']
            NA_241 = ["Garden", 'Saddar Town', 'Civil Line', 'Jamshed Town']

            NA_242 = ["Gulistan-e-Johar", 'Gulshan-e-Iqbal Town', 'Shah Faisal Town',
                      'Malir Town']
            NA_243 = ["Nazimabad Town", 'North Nazimabad Town', 'New Karachi Town',
                      'Liaquatabad Town', 'Gulberg Town', 'North Karachi Town']
            NA_244 = ["Gadap Town", 'Surjani Town']
            NA_245 = ["SITE Town", 'Baldia Town', 'Orangi Town']

            for i in NA_240:
                if i == self.signupTown:
                    self.sector = 'NA-240'

            for i in NA_241:
                if i == self.signupTown:
                    self.sector = 'NA-241'

            for i in NA_242:
                if i == self.signupTown:
                    self.sector = 'NA-242'

            for i in NA_243:
                if i == self.signupTown:
                    self.sector = 'NA-243'

            for i in NA_244:
                if i == self.signupTown:
                    self.sector = 'NA-244'

            for i in NA_245:
                if i == self.signupTown:
                    self.sector = 'NA-245'

            try:
                self.image_id = self.id_check(random.randint(0, 999))
                print(self.image_id)
                data2 = {
                    'Name': self.signupName,
                    'Mobile Number': self.signupMobileNo,
                    'CNIC': self.signupCNIC,
                    'Email ID': self.signupEmail,
                    'House Number': self.signupAddress,
                    'Town': self.signupTown,
                    'City': self.signupCity,
                    'Date of Birth': self.signupDOB,
                    'ImageID': self.image_id,
                    'Flag': 0,
                    'Sector': self.sector,
                }
                self.db.collection('Voters').document(self.signupCNIC).set(data2)

                cancel_btn_username_dialogue = MDFlatButton(text='Continue', on_release=self.next_window)
                self.dialog = MDDialog(title='CNIC Registered', text='Please follow the given instructions for '
                                                                     'face recognition',
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                MDApp.get_running_app().root.current = 'signupscreen3'

            except:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Database Error', text='Data insertion failed', size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                return

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date, year=2001, month=1, day=23, )
        date_dialog.open()

    def get_date(self, date):
        self.dob = date
        self.strng.get_screen('signupscreen2').ids.date_picker.text = str(self.dob)

    def set_time_voting(self):
        doc_ref = self.db.collection('Time').document('Time')
        docs = doc_ref.get()
        startDate = ''
        endDate = ''
        if docs.exists:
            a = docs.to_dict()
            startDate = a['StartDate Voting']
            endDate = a['EndDate Voting']

        year = int(startDate[0:4])
        month = int(startDate[5:7])
        sdate = int(startDate[8:10])
        edate = int(endDate[8:10])
        if datetime.date.today() <= datetime.date(year, month, int(edate)):
            if datetime.date.today() >= datetime.date(year, month, int(sdate)):
                self.login()
            else:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Time Error', text='Voting is not started yet. It will'
                                                                ' be available after ' + startDate,
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                MDApp.get_running_app().root.current = 'loginscreen1'
                return
        else:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Time Error', text='Time of  voting has ended. Last date was '
                                                            + endDate, size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'loginscreen1'
            return

    def login(self):
        self.loginCNIC = self.strng.get_screen('loginscreen1').ids.usercnicno.text
        if self.loginCNIC.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Error', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid CNIC', text='Please enter your CNIC',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            return

        doc_ref = self.db.collection('Voters').document(self.loginCNIC)
        docs = doc_ref.get()

        if docs.exists:
            self.a = docs.to_dict()
            if self.a['Flag'] == 1:
                cancel_btn_username_dialogue = MDFlatButton(text='Error', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Already Casted vote', text='Vote already been casted',
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                return
            # self.storage.child('Voter Images/')
            imageList = []
            a = self.bucket.list_blobs()
            for i in a:
                # print(i.name)
                imageList.append(i.name)

            print(imageList)
            self.imgPath = str(self.a['ImageID'])
            if ('Voter Images/' + str(self.a['ImageID']) + '.jpg') in imageList:
                MDApp.get_running_app().root.current = 'detection'

            else:
                cancel_btn_username_dialogue = MDFlatButton(text='Continue', on_release=self.face_detect)
                self.dialog = MDDialog(title='Face has not Recognized', text='Click on the Continue Button for face recognition',
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()



        else:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid CNIC', text='CNIC does not Exist', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            return

    def facial_recognition(self):
        self.storage.child('trainer.yml').download('/', 'trainingData.yml')
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        rec = cv2.face.LBPHFaceRecognizer_create()
        rec.read("trainer/trainer.yml")

        cam = cv2.VideoCapture(0)

        flag = 0
        font = cv2.FONT_HERSHEY_SIMPLEX
        user_id = self.a['ImageID']
        print(user_id)

        while (True):

            ret, img = cam.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                id, conf = rec.predict(gray[y:y + h, x:x + w])
                print(conf)
                print(id)
                print(user_id)

                if user_id == id:
                    flag = 1

                else:
                    # print(id)
                    # print(user_id)
                    id = "Face not recognized"

                cv2.putText(img, str(id), (x, y + h), font, 0.9, (0, 0, 255), 2)

            cv2.imshow('frame', img)

            if cv2.waitKey(700) == ord('q'):
                flag = -1
                break

            elif cv2.waitKey(700) & flag == 1:
                break

        cam.release()
        cv2.destroyAllWindows()
        return flag

    def printpress(self):
        print('Button has been pressed')
        flag = self.facial_recognition()
        if flag == 1:
            print('this is my flag:', flag)
            self.switch()
        elif flag == -1:
            self.logout()
        else:
            pass

    def switch(self):
        print('function called')
        MDApp.get_running_app().root.current = 'dashboard'
        self.dashboard()

    def dashboard(self):
        directory = str(self.a['ImageID'])
        print(directory)
        self.strng.get_screen('dashboard').ids.name.text = 'Name: ' + str(self.a['Name'])
        self.strng.get_screen('dashboard').ids.CNIC.text = 'CNIC: ' + str(self.a['CNIC'])
        self.strng.get_screen('dashboard'). \
            ids.Sector.text = 'Sector: ' + str(self.a['Sector'])
        self.storage.child('Voter Images/' + directory + '.jpg').download('/', 'user.' + directory + ".jpg")
        self.strng.get_screen('dashboard').ids.avatar.source = 'user.' + directory + ".jpg"

        candidates_info = self.db.collection('Candidates').where(u'Sector', u'==', self.a['Sector']).get()
        self.can_sector = ''
        for doc in candidates_info:
            dic = doc.to_dict()
            self.can_sector = dic['Sector']
            b = dic['Candidate Name']
            c = dic['PartyName']
            self.can_cnic.append(b)
            self.can_party.append(c)

        checkboxes = []
        for i in range(0, len(candidates_info)):
            self.list = ThreeLineAvatarIconListItem(text='Sector: ' + self.can_sector,
                                                    secondary_text='Candidate Name: ' + self.can_cnic[i - 1],
                                                    tertiary_text='Party Name: ' + self.can_party[i - 1],
                                                    )
            self.check_box = MDCheckbox(
                active=False,
                pos_hint={'center_x': 0.95, 'center_y': .3},
                group="test" + str(i),
            )
            self.checks.append(self.check_box)
            checkboxes.append(self.check_box)
            checkboxes.append(self.list.text)
            checkboxes.append(self.list.secondary_text)
            checkboxes.append(self.list.tertiary_text)
            self.check_ref["CheckBox" + str(i)] = self.check_box
            self.list.add_widget(self.check_box)
            self.strng.get_screen('dashboard').ids.scroll.add_widget(self.list)
        for i in range(0, len(checkboxes), 4):
            self.data.append(checkboxes[i:i + 4])
        submit_button = MDRectangleFlatButton(
            text='Submit',
            on_press=self.cast_vote,
            pos_hint={"x": .7, "y": .1},
        )
        self.strng.get_screen('dashboard').ids.scroll.add_widget(submit_button)

    def logout(self):
        MDApp.get_running_app().stop()
        SignUPApp().run()

    def cast_vote(self, obj):
        a = []
        for idx, wgt in self.check_ref.items():
            if wgt.active:
                a.append(wgt)
        can_cnic = ''
        cnic = []
        if len(a) == 1:
            for i in range(len(self.data)):
                check_true = self.data[i][0]
                for j in a:
                    if check_true == j:
                        can_cnic = self.data[i][2]
                        cnic.append(self.data[i][2])

            CNIC = can_cnic[6:19]
            inc_vote = self.db.collection('Candidates').document(CNIC)
            docs = inc_vote.get()

            if docs.exists:
                votes = docs.to_dict()
                vote = int(votes['Number of Votes']) + int(1)
                self.db.collection('Candidates').document(CNIC).set({'Candidate Name': votes['Candidate Name'],
                                                                     'PartyName': votes['PartyName'],
                                                                     'CNIC': votes['CNIC'],
                                                                     'Town': votes['Town'],
                                                                     'Sector': votes['Sector'],
                                                                     'Number of Votes': int(vote)
                                                                     })
                self.db.collection('Voters'). \
                    document(self.loginCNIC).update({'Flag': 1})
                cancel_btn_username_dialogue = MDFlatButton(text='OK', on_release=self.close_window)
                self.dialog = MDDialog(title='Congrats', text='Your vote has been casted to '
                                                              + votes['Candidate Name'] +
                                                              ' having CNIC Number ' + votes['CNIC'],
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                Clock.schedule_once(self.close, 10)

        if len(a) > 1:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='One Candidate', text='Please select only one candidate', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

            return

        if len(a) == 0:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='One Candidate', text='Please select a candidate', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            return

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def next_window(self, obj):
        self.dialog.dismiss()
        MDApp.get_running_app().root.current = 'signupscreen3'

    def face_detect(self, obj):
        self.dialog.dismiss()
        MDApp.get_running_app().root.current = 'signupscreen3'
        self.image_id = self.imgPath
        # self.detection()

    def close(self, obj):
        MDApp.get_running_app().stop()

    def close_window(self, obj):
        self.dialog.dismiss()
        MDApp.get_running_app().stop()

    def detection(self):
        self.dialog.dismiss()
        global y, h, w, x
        cap = cv2.VideoCapture(0)
        count = 1
        directory = str(self.image_id)
        print(self.image_id)
        print(directory)

        while 1:
            k = cv2.waitKey(1) & 0xFF
            ret, img = cap.read()
            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Initializing the haar classifier with the face detector model

            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(img, 'Face Detected', (x + 20, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                            2, cv2.LINE_AA)
                if k == ord('s'):
                    for i in range(0, 1):
                        i = count

                        cv2.imwrite('user.' + directory + ".jpg", gray[y:y + h, x:x + w])

                        count += 1
                    break
            cv2.imshow('img', img)
            if (x, y, w, h) not in faces:  # ek dafa andar indent krke run. close then place this
                # block like current position again
                if k == ord('s'):
                    print('no face')
                    cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                    self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input',
                                           size_hint=(0.7, 0.2),
                                           buttons=[cancel_btn_username_dialogue])
                    self.dialog.open()
                    return
                # break
            if k == ord('s'):
                break
            # k = cv2.waitKey(1) & 0xFF

            # if k == ord('s'):
            #     for i in range(0, 1):
            #         i = count
            #
            #         cv2.imwrite('user.' + directory + ".jpg", gray[y:y + h, x:x + w])
            #
            #         count += 1
            #     break

        cap.release()
        cv2.destroyAllWindows()
        self.storage.child('Voter Images/' + directory + '.jpg').put('user.' + directory + ".jpg")
        toast('Image Uploaded')
        MDApp.get_running_app().root.current = 'loginscreen1'


Config.set('graphics', 'fullscreen', 0)
SignUPApp().run()
