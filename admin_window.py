import csv
import datetime
import json
import os


import cv2
import pyrebase
import requests
from fpdf import FPDF
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
import numpy as np
from PIL import Image
from admin_GUI import screen_helper
from kivy.uix.screenmanager import Screen, ScreenManager
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from mailing import *


class LoginScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class ProfileScreen(Screen):
    pass


class ShowAdmin(Screen):
    pass


class VoteScreen(Screen):
    pass


class DisplayCandidate(Screen):
    pass


class CandidateScreen(Screen):
    pass


class LogoScreen(Screen):
    pass


class AddCandidateScreen(Screen):
    pass


class Timer(Screen):
    pass


class VotingResult(Screen):
    pass


# class Email(Screen):
#     pass

sm = ScreenManager()
sm.add_widget(LoginScreen(name='Login'))
sm.add_widget(MenuScreen(name='Menu'))
sm.add_widget(ProfileScreen(name='Profile'))
sm.add_widget(ShowAdmin(name='showAdmin'))
sm.add_widget(VoteScreen(name='Vote'))
sm.add_widget(DisplayCandidate(name='display_candidate'))
sm.add_widget(CandidateScreen(name='Candidate'))
sm.add_widget(LogoScreen(name='logoscreen'))
sm.add_widget(AddCandidateScreen(name='Add_Candidate'))
sm.add_widget(Timer(name='clock'))
sm.add_widget(VotingResult(name='voting_result'))


# sm.add_widget(Email(name='email'))


def callback1(obj):
    MDApp.get_running_app().root.current = 'Login'


class FileNotFoundErrors(Exception):
    pass


class CustomPDF(FPDF):

    def header(self):
        # Set up a logo
        self.image('sskenterprise.jpg', 10, 20, 40)
        self.set_font('Arial', 'B', 15)

        # Add an address
        self.cell(100)
        self.cell(0, 5, 'Electronic Voting System', ln=1)
        self.cell(100)
        self.cell(0, 5, 'City: Karachi', ln=1)
        self.cell(100)

        # Line break
        self.ln(60)

    def footer(self):
        self.set_y(-10)

        self.set_font('Arial', 'I', 8)

        # Add a page number
        page = 'Page ' + str(self.page_no()) + '/{nb}'
        self.cell(0, 10, page, 0, 0, 'C')


class AdminAccess(MDApp):
    def __init__(self):
        super().__init__()
        self.ad_adminID = []
        self.ad_mobileNumber = []
        self.ad_password = []
        self.ad_email = []
        self.ad_name = []
        self.ad_imgpath = []
        self.data_list = []
        self.screen = Builder.load_string(screen_helper)
        if not len(firebase_admin._apps):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
        self.theme_cls.primary_palette = 'Amber'
        Clock.schedule_once(self.forTowns)
        Clock.schedule_once(self.forParty)
        # Clock.schedule_once(self.forSector)
        self.db = firestore.client()
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

            # define storage
            self.storage = self.firebase.storage()
        except requests.exceptions.HTTPError as httpErr:
            error_message = json.loads(httpErr.args[1])['error']['message']
        # var = json.loads(np.e.args[1])['error']['message']

    def build(self):
        Clock.schedule_once(callback1, 3)
        return self.screen

    @staticmethod
    def nav_draw():
        MDApp.get_running_app().root.current = 'Add_Candidate'

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
            caller=self.screen.get_screen('Add_Candidate').ids.town,
            position="auto",
            width_mult=4,
            callback=self.drop_down

        )
        self.menu.bind(on_release=self.drop_down)

    def drop_down(self, instance):
        self.screen.get_screen('Add_Candidate').ids.town.text = instance.text

    def forParty(self, *args):
        menu_items_party = [
            {"text": "Party A"},
            {"text": "Party B"},
            {"text": "Party C"},
            {"text": "Party D"},
            {"text": "Party E"},
            {"text": "Party F"},
            {"text": "Independent"},
        ]
        self.menu_party = MDDropdownMenu(
            items=menu_items_party,
            caller=self.screen.get_screen('Add_Candidate').ids.party_name,
            position="auto",
            width_mult=4,
            callback=self.drop_down_party

        )
        self.menu_party.bind(on_release=self.drop_down_party)

    def drop_down_party(self, instance):
        self.screen.get_screen('Add_Candidate').ids.party_name.text = instance.text

    # def forSector(self, *args):
    #     menu_items_sector = [
    #         {"text": "NA-240"},
    #         {"text": "NA-241"},
    #         {"text": "NA-242"},
    #         {"text": "NA-243"},
    #         {"text": "NA-244"},
    #         {"text": "NA-245"},
    #     ]
    #     self.menu_sector = MDDropdownMenu(
    #         items=menu_items_sector,
    #         caller=self.screen.get_screen('Add_Candidate').ids.sector,
    #         position="auto",
    #         width_mult=4,
    #         callback=self.drop_down_sector
    #
    #     )
    #     self.menu_sector.bind(on_release=self.drop_down_sector)
    #
    # def drop_down_sector(self, instance):
    #     self.screen.get_screen('Add_Candidate').ids.sector.text = instance.text

    def admin_login(self):
        self.adminID = self.screen.get_screen('Login').ids.adminID.text
        self.password = self.screen.get_screen('Login').ids.password.text

        if self.adminID.split() == [] or self.password.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            # self.strng.current = 'signupscreen1'
            MDApp.get_running_app().root.current = 'Login'
            return

        else:
            doc_ref = self.db.collection('Admin').document(self.adminID)
            docs = doc_ref.get()
            if docs.exists:
                self.a = docs.to_dict()
                if self.a['Password'] == self.password:
                    MDApp.get_running_app().root.current = 'Menu'

                else:
                    cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                    self.dialog = MDDialog(title='Invalid Password', text='Please Enter a Valid Password',
                                           size_hint=(0.7, 0.2),
                                           buttons=[cancel_btn_username_dialogue])
                    self.dialog.open()
                    MDApp.get_running_app().root.current = 'Login'
                    return

            else:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Invalid AdminID', text='Please Enter a Valid AdminID',
                                       size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                MDApp.get_running_app().root.current = 'Login'
                return

    def close_app(self, *largs):
        super(AdminAccess, self).stop(*largs)

    def logout_admin(self):
        self.screen.get_screen('Login').ids.password.text = ''
        MDApp.get_running_app().stop()
        self.screen.get_screen('Profile').remove_widget(self.screen.get_screen('Profile').ids.viewAdmins)

    def submit(self):
        self.candidateName = self.screen.get_screen('Add_Candidate').ids.candidate_name.text
        self.partyName = self.screen.get_screen('Add_Candidate').ids.party_name.text
        self.CNIC = self.screen.get_screen('Add_Candidate').ids.cnic.text
        self.town = self.screen.get_screen('Add_Candidate').ids.town.text
        self.sector = ''
        if self.candidateName.split() == [] or self.partyName.split() == [] \
                or self.CNIC.split() == [] or self.town.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'Add_Candidate'
            return

        if len(self.CNIC) is not 13:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid CNIC', text='Please Enter a Valid CNIC',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'Add_Candidate'
            return
        self.doc_ref = self.db.collection('Candidates').where(u'CNIC', u'==', self.CNIC).stream()

        for doc in self.doc_ref:
            a = doc.to_dict()
            list = a['CNIC']
            if self.CNIC == list:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Invalid CNIC', text='CNIC Exists', size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                MDApp.get_running_app().root.current = 'Add_Candidate'
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
                if i == self.town:
                    self.sector = 'NA-240'

            for i in NA_241:
                if i == self.town:
                    self.sector = 'NA-241'

            for i in NA_242:
                if i == self.town:
                    self.sector = 'NA-242'

            for i in NA_243:
                if i == self.town:
                    self.sector = 'NA-243'

            for i in NA_244:
                if i == self.town:
                    self.sector = 'NA-244'

            for i in NA_245:
                if i == self.town:
                    self.sector = 'NA-245'

            try:
                data2 = {
                    'Candidate Name': self.candidateName,
                    'PartyName': self.partyName,
                    'CNIC': self.CNIC,
                    'Town': self.town,
                    'Sector': self.sector,
                    'Number of Votes': 0
                }
                self.db.collection('Candidates').document(self.CNIC).set(data2)

                MDApp.get_running_app().root.current = 'Menu'

            except:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Database Error', text='Data insertion failed', size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                return

    def save_time(self):
        self.start_reg = self.screen.get_screen('clock').ids.start_time_registration.text
        self.end_reg = self.screen.get_screen('clock').ids.end_time_registration.text
        self.start_voting = self.screen.get_screen('clock').ids.start_time_voting.text
        self.end_voting = self.screen.get_screen('clock').ids.end_time_voting.text
        self.start_result = self.screen.get_screen('clock').ids.start_result.text

        if self.start_reg.split() == [] or self.end_reg.split() == [] \
                or self.start_voting.split() == [] or self.end_voting.split() == [] or self.start_result.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'clock'
            return

        else:
            try:
                time = {
                    'StartDate Registration': self.start_reg,
                    'EndDate Registration': self.end_reg,
                    'StartDate Voting': self.start_voting,
                    'EndDate Voting': self.end_voting,
                    'Start Result': self.start_result,
                }
                self.db.collection('Time').document('Time').set(time)
                MDApp.get_running_app().root.current = 'Menu'

            except:
                cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
                self.dialog = MDDialog(title='Database Error', text='Data insertion failed', size_hint=(0.7, 0.2),
                                       buttons=[cancel_btn_username_dialogue])
                self.dialog.open()
                return

    def show_voter(self):

        doc_ref = self.db.collection('Voters').get()
        self.data_list_voters = []
        i = 1
        for docs in doc_ref:
            if len(doc_ref) == 0:
                self.screen.get_screen('Vote').ids.vote_label.text = 'Welcome to Voter Table'
            a = docs.to_dict()
            data = [i, a['Name'], a['CNIC'], a['Mobile Number'], a['Email ID'], a['House Number'],
                    a['Town'], a['Sector'], a['City'], a['Date of Birth'], a['Flag'], ]
            self.data_list_voters.append(data)
            i += 1

        self.data_tables_votes = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            # orientation="lr-tb",
            column_data=[
                ("S.No", dp(20)),
                ("Name", dp(30)),
                ("CNIC", dp(30)),
                ("Mobile Number", dp(25)),
                ("Email ID", dp(40)),
                ("House Number", dp(20)),
                ("Town", dp(35)),
                ("Sector", dp(20)),
                ("City", dp(15)),
                ("Date Of Birth", dp(25)),
                ("Vote Cast", dp(10)),
            ],
            row_data=self.data_list_voters
        )
        self.screen.get_screen('Vote').ids.anchor_layout.add_widget(self.data_tables_votes)

    def voter_excel(self):
        data = ["S.No", "Name", "CNIC", "Mobile Number", "Email ID", "House Number", "Town",
                "Sector", "City", "Date Of Birth", "Vote Cast"]
        self.data_list_voters.insert(0, data)
        if (not os.path.isfile(
                "EVSystemVoters.csv")):  # checks if Bike_List_With_Service.csv is in path
            with open("EVSystemVoters.csv", 'w',
                      newline='') as file:  # creates a new csv file named 'Bikelistwithservice.csv'
                a = csv.writer(file)
                a.writerow(['Updated by: ' + self.adminID])
                a.writerows(self.data_list_voters)  # write each line of data
                toast("Excel Sheet Created")
        else:
            file_to_be_overwrite = "EVSystemVoters.csv"
            ov = open(file_to_be_overwrite, "w")
            ov.truncate()  # clears everything in the file and reenter the data
            ov.close()
            with open("EVSystemVoters.csv", 'w',
                      newline='') as file:  # creates a new csv file named 'Bikelistwithservice.csv'
                a = csv.writer(file)
                a.writerow(['Updated by: ' + self.adminID])
                a.writerows(self.data_list_voters)  # write each line of data
                toast("Excel Sheet Created")

    def show_candidate(self):
        self.data_list_can = []
        doc_ref = self.db.collection('Candidates').get()
        i = 1
        for docs in doc_ref:
            a = docs.to_dict()
            data = [i, a['Candidate Name'], a['CNIC'], a['PartyName'], a['Sector'], a['Town'],
                    a['Number of Votes'], ]
            self.data_list_can.append(data)
            i += 1
        print(self.data_list_can)
        self.data_tables_can = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            # orientation="lr-tb",
            column_data=[
                ("S.No", dp(20)),
                ("Candidate Name", dp(35)),
                ("CNIC", dp(30)),
                ("Party Name", dp(25)),
                ("Sector", dp(20)),
                ("Town", dp(40)),
                ("Number of Votes", dp(30)),
            ],
            row_data=self.data_list_can
        )

        self.screen.get_screen('display_candidate').ids.anchor_layout.add_widget(self.data_tables_can)
        # self.screen.get_screen('display_candidate').ids.anchor_layout.add_widget(excel_button)

    def on_enter(self):
        self.data_tables_votes.open()
        self.data_tables_can.open()

    def candidate_excel(self):
        data = ["S.No", "Candidate Name", "CNIC", "Party Name", "Sector", "Town", "Number of Votes"]
        self.data_list_can.insert(0, data)
        if (not os.path.isfile(
                "EVSystemCandidates.csv")):  # checks if Bike_List_With_Service.csv is in path
            with open("EVSystemCandidates.csv", 'w',
                      newline='') as file:  # creates a new csv file named 'Bikelistwithservice.csv'
                a = csv.writer(file)
                a.writerow(['Updated by: ' + self.adminID])
                a.writerows(self.data_list_can)  # write each line of data
                toast("Excel Sheet Created")
        else:
            file_to_be_overwrite = "EVSystemCandidates.csv"
            ov = open(file_to_be_overwrite, "w")
            ov.truncate()  # clears everything in the file and reenter the data
            ov.close()
            with open("EVSystemCandidates.csv", 'w',
                      newline='') as file:  # creates a new csv file named 'Bikelistwithservice.csv'
                a = csv.writer(file)
                a.writerow(['Updated by: ' + self.adminID])
                a.writerows(self.data_list_can)  # write each line of data
                toast("Excel Sheet Created")

    def profile(self):

        self.screen.get_screen('Profile').ids.name.text = self.a['Name']
        self.screen.get_screen('Profile').ids.email.text = self.a['Email']
        self.screen.get_screen('Profile').ids.mobileNumber.text = self.a['Mobile Number']
        self.screen.get_screen('Profile').ids.password.text = self.a['Password']
        self.screen.get_screen('Profile').ids.adminId.text = self.a['AdminID']
        self.screen.get_screen('Profile').ids.imagePath.source = self.a['Image Path']

        if self.a['Priority'] == 1:
            self.screen.get_screen('Profile').ids.viewAdmins.disabled = False
        if self.a['Priority'] == 0:
            self.screen.get_screen('Profile').ids.viewAdmins.remove_widget = True
            self.screen.get_screen('Profile').remove_widget(self.screen.get_screen('Profile').ids.viewAdmins)
        # self.adminImage = self.screen.get_screen('Profile').ids.imagePath.text

    def show_admin(self):

        admin_info = self.db.collection('Admin').where(u'Priority', u'==', 0).get()
        for doc in admin_info:
            dic = doc.to_dict()
            b = dic['Name']
            c = dic['Email']
            d = dic['Password']
            e = dic['Mobile Number']
            f = dic['AdminID']
            g = dic['Image Path']
            self.ad_name.append(b)
            self.ad_email.append(c)
            self.ad_password.append(d)
            self.ad_mobileNumber.append(e)
            self.ad_adminID.append(f)
            self.ad_imgpath.append(g)
        for i in range(0, len(admin_info)):
            self.card = MDCard(
                orientation="vertical",

                elevation=15,
                ripple_behavior=True,
                size_hint=[1, None],
                size=[300, 200]

                # on_touch_down = toast('clicked')
            )

            label_name = MDLabel(
                text='Name: ' + self.ad_name[i - 1],
                pos_hint={'center_x': 0.53, 'center_y': .8}
            )

            label_email = MDLabel(
                text='Email: ' + self.ad_email[i - 1],
                pos_hint={'center_x': 0.53, 'center_y': .8}
            )
            # label_cnic.size_hint = [1, 1]

            label_password = MDLabel(
                text='Password: ' + self.ad_password[i - 1],
                pos_hint={'center_x': 0.53, 'center_y': .8}
            )
            # label_party.size_hint = [1, 1]
            label_mobileNumber = MDLabel(
                text='Mobile Number: ' + self.ad_mobileNumber[i - 1],
                pos_hint={'center_x': 0.53, 'center_y': .8}
            )
            label_adminID = MDLabel(
                text='AdminID: ' + self.ad_adminID[i - 1],
                pos_hint={'center_x': 0.53, 'center_y': .8}
            )
            # img = Image(source=self.ad_imgpath[i - 1])
            # img.size_hint_y = None
            # img.top = 1
            # img.height = dp(100)

            self.card.add_widget(label_name)
            self.card.add_widget(label_email)
            self.card.add_widget(label_password)
            self.card.add_widget(label_mobileNumber)
            self.card.add_widget(label_adminID)
            # self.card.add_widget(img)
            self.screen.get_screen('showAdmin').ids.scroll.add_widget(self.card)

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def download_images(self):
        # os.mkdir('Voters')
        cnic_list = []
        doc_ref = self.db.collection('Voters').get()
        for doc in doc_ref:
            a = doc.to_dict()
            l = a['ImageID']
            cnic_list.append(l)
        print(cnic_list)
        for i in cnic_list:
            print(i)
            for j in range(0, 31):
                self.storage.child('Voter Images/' + str(i) + '.jpg').download(
                    '/',
                    'Voters/Voter.' + str(i) + '.' + str(j) + '.jpeg')

    def training_images(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        Ids, faces = self.getImagesAndLabels('Voters')
        print()
        self.recognizer.train(faces, Ids)
        self.recognizer.save('trainer/trainer.yml')
        cv2.destroyAllWindows()
        toast('Training start. This will take few minutes')
        self.storage.child('trainer.yml').put('trainer/trainer.yml')
        toast('Training done')

    def getImagesAndLabels(self, path):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # get the path of all the files in the folder
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        # create empty face list
        faceSamples = []
        # create empty ID list
        Ids = []
        # now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
            print(Id)
            cv2.imshow('training', imageNp)
            cv2.waitKey(10)
            # extract the face from the training image sample
            # faces = self.face_cascade.detectMultiScale(imageNp)
            # If a face is there then append that in the list as well as Id of it
            # for (x, y, w, h) in faces:
            #     faceSamples.append(imageNp[y:y + h, x:x + w])
            faceSamples.append(imageNp)
            Ids.append(Id)
        return np.array(Ids), faceSamples

    def set_time_result(self):
        doc_ref = self.db.collection('Time').document('Time')
        docs = doc_ref.get()
        startDate = ''
        if docs.exists:
            a = docs.to_dict()
            startDate = a['Start Result']

        year = int(startDate[0:4])
        month = int(startDate[5:7])
        sdate = int(startDate[8:10])

        if datetime.date.today() >= datetime.date(year, month, int(sdate)):
            self.vote_result()
        else:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Time Error', text='Result is not started yet. It will'
                                                            ' be available after ' + startDate,
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'voting_result'
            return

    def vote_result(self):

        MDApp.get_running_app().root.current = 'voting_result'
        candidates_info = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-240').get()
        VoteA = {}
        totalcan_240 = []
        for doc in candidates_info:
            dic = doc.to_dict()

            # VoteA.append(NA_240)
            name = dic['PartyName']
            VoteA[name, dic['Candidate Name'], dic['CNIC']] = str(dic['Number of Votes'])
            totalcan_240.append(name)
            # NA_240.append(self.NA_240)
        print(sorted(totalcan_240))
        # data = sum(int(i) for i in NA_240)
        print('240',  VoteA)
        list = sorted(VoteA.items(), reverse=True, key=lambda x: x[1])
        print(list[0][0][0], list[0][0][1], list[0][0][2], list[0][1])


        candidates_info1 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-241').get()
        totalcan_241 = []
        for doc in candidates_info1:
            dic = doc.to_dict()
            # self.NA_241 = dic['Number of Votes']
            name = dic['PartyName']
            totalcan_241.append(name)
            # NA_241.append(self.NA_241)
        print(sorted(totalcan_241))
        # data1 = sum(int(i) for i in NA_241)
        # print(data1)

        candidates_info2 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-242').get()
        totalcan_242 = []
        for doc in candidates_info2:
            dic = doc.to_dict()
            # self.NA_242 = dic['Number of Votes']
            name = dic['PartyName']
            totalcan_242.append(name)
            # NA_242.append(self.NA_242)
        print(sorted(totalcan_242))
        # data2 = sum(int(i) for i in NA_242)
        # print(data2)

        candidates_info3 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-243').get()
        totalcan_243 = []
        for doc in candidates_info3:
            dic = doc.to_dict()
            # self.NA_243 = dic['Number of Votes']
            name = dic['PartyName']
            totalcan_243.append(name)
            # NA_243.append(self.NA_243)
        print(sorted(totalcan_243))
        # data3 = sum(int(i) for i in NA_243)
        # print(data3)

        candidates_info4 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-244').get()
        totalcan_244 = []
        for doc in candidates_info4:
            dic = doc.to_dict()
            # self.NA_244 = dic['Number of Votes']
            name = dic['PartyName']
            totalcan_244.append(name)
            # NA_244.append(self.NA_244)
        print(sorted(totalcan_244))
        # data4 = sum(int(i) for i in NA_244)
        # print(data4)

        candidates_info5 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-245').get()
        totalcan_245 = []
        for doc in candidates_info5:
            dic = doc.to_dict()
            # self.NA_245 = dic['Number of Votes']
            name = dic['PartyName']
            totalcan_245.append(name)
            # NA_245.append(self.NA_245)
        print(sorted(totalcan_245))
        # data5 = sum(int(i) for i in NA_245)
        # print(data5)

        party_infoA = self.db.collection('Candidates').where(u'PartyName', u'==', 'Party A').get()
        VoteA = {}
        votesA = []
        for doc in party_infoA:
            dic = doc.to_dict()
            voteA = dic['Number of Votes']
            VoteA[dic['Sector']] = voteA
            votesA.append(voteA)
        print(votesA)
        total_voteA = sum(int(i) for i in votesA)
        print(total_voteA)

        party_infoB = self.db.collection('Candidates').where(u'PartyName', u'==', 'Party B').get()
        VoteB = {}
        votesB = []
        for doc in party_infoB:
            dic = doc.to_dict()
            voteB = dic['Number of Votes']
            VoteB[dic['Sector']] = voteB
            votesB.append(voteB)
        print(votesB)
        total_voteB = sum(int(i) for i in votesB)
        print(total_voteB)

        party_infoC = self.db.collection('Candidates').where(u'PartyName', u'==', 'Party C').get()
        VoteC = {}
        votesC = []
        for doc in party_infoC:
            dic = doc.to_dict()
            voteC = dic['Number of Votes']
            VoteC[dic['Sector']] = voteC
            votesC.append(voteC)
        print(votesC)
        total_voteC = sum(int(i) for i in votesC)
        print(total_voteC)

        party_infoD = self.db.collection('Candidates').where(u'PartyName', u'==', 'Party D').get()
        VoteD = {}
        votesD = []
        for doc in party_infoD:
            dic = doc.to_dict()
            voteD = dic['Number of Votes']
            VoteD[dic['Sector']] = voteD
            votesD.append(voteD)
        print(votesD)
        total_voteD = sum(int(i) for i in votesD)
        print(total_voteD)

        party_infoE = self.db.collection('Candidates').where(u'PartyName', u'==', 'Party E').get()
        VoteE = {}
        votesE = []
        for doc in party_infoE:
            dic = doc.to_dict()
            voteE = dic['Number of Votes']
            VoteE[dic['Sector']] = voteE
            votesE.append(voteE)
        print(votesE)
        total_voteE = sum(int(i) for i in votesE)
        print(total_voteE)

        party_infoF = self.db.collection('Candidates').where(u'PartyName', u'==', 'Party F').get()
        VoteF = {}
        votesF = []
        for doc in party_infoF:
            dic = doc.to_dict()
            voteF = dic['Number of Votes']
            VoteF[dic['Sector']] = voteF
            votesF.append(voteF)
        print(votesF)
        total_voteF = sum(int(i) for i in votesF)
        print(total_voteF)

        party_infoInd = self.db.collection('Candidates').where(u'PartyName', u'==', 'Independent').get()
        total_ind = len(party_infoInd)
        print('total ind can', total_ind)
        VoteInd = {}
        votesIND = []
        for doc in party_infoInd:
            dic = doc.to_dict()
            voteInd = dic['Number of Votes']
            VoteInd[dic['Sector']] = voteInd
            votesIND.append(voteInd)
        print(votesF)
        total_voteInd = sum(int(i) for i in votesIND)

        print(VoteA)
        print(VoteB)
        print(VoteC)
        print(VoteD)
        print(VoteE)
        print(VoteF)
        print(VoteInd)
        print(total_voteInd)

        vote_reg = self.db.collection('Voters').get()
        total_vote = len(vote_reg)
        print('total vote registered', total_vote)

        vote_cast = self.db.collection('Voters').where(u'Flag', u'==', 1).get()
        total_vote_cast = len(vote_cast)
        print('total vote cast', total_vote_cast)
        l = []
        partywon = {
            'Party A': total_voteA,
            'Party B': total_voteB,
            'Party C': total_voteC,
            'Party D': total_voteD,
            'Party E': total_voteE,
            'Party F': total_voteF,

        }
        list = sorted(partywon.items(), reverse=True, key=lambda x: x[1])
        won = list[0][0]
        won_votes = list[0][1]
        print(won)
        # Iterate over the sorted sequence
        for elem in list:
            print(elem[0], " :", elem[1])

        total_can = self.db.collection('Candidates').get()
        totalCandiates = len(total_can)
        print('total can', totalCandiates)

        total_voters_240 = self.db.collection('Voters').where(u'Flag', u'==', 1).where(u'Sector', u'==', 'NA-240').get()
        total_voters_240 = len(total_voters_240)
        print('total voters in NA-240', total_voters_240)

        total_voters_241 = self.db.collection('Voters').where(u'Flag', u'==', 1).where(u'Sector', u'==', 'NA-241').get()
        total_voters_241 = len(total_voters_241)
        print('total voters in NA-241', total_voters_241)

        total_voters_242 = self.db.collection('Voters').where(u'Flag', u'==', 1).where(u'Sector', u'==', 'NA-242').get()
        total_voters_242 = len(total_voters_242)
        print('total voters in NA-242', total_voters_242)

        total_voters_243 = self.db.collection('Voters').where(u'Flag', u'==', 1).where(u'Sector', u'==', 'NA-243').get()
        total_voters_243 = len(total_voters_243)
        print('total voters in NA-243', total_voters_243)

        total_voters_244 = self.db.collection('Voters').where(u'Flag', u'==', 1).where(u'Sector', u'==', 'NA-244').get()
        total_voters_244 = len(total_voters_244)
        print('total voters in NA-244', total_voters_244)

        total_voters_245 = self.db.collection('Voters').where(u'Flag', u'==', 1).where(u'Sector', u'==', 'NA-245').get()
        total_voters_245 = len(total_voters_245)
        print('total voters in NA-245', total_voters_245)

        total_voters_reg_240 = self.db.collection('Voters').where(u'Sector', u'==', 'NA-240').get()
        total_voters_reg_240 = len(total_voters_reg_240)
        print('total voters reg in NA-240', total_voters_reg_240)

        total_voters_reg_241 = self.db.collection('Voters').where(u'Sector', u'==', 'NA-241').get()
        total_voters_reg_241 = len(total_voters_reg_241)
        print('total voters reg in NA-241', total_voters_reg_241)

        total_voters_reg_242 = self.db.collection('Voters').where(u'Sector', u'==', 'NA-242').get()
        total_voters_reg_242 = len(total_voters_reg_242)
        print('total voters reg in NA-242', total_voters_reg_242)

        total_voters_reg_243 = self.db.collection('Voters').where(u'Sector', u'==', 'NA-243').get()
        total_voters_reg_243 = len(total_voters_reg_243)
        print('total voters reg in NA-243', total_voters_reg_243)

        total_voters_reg_244 = self.db.collection('Voters').where(u'Sector', u'==', 'NA-244').get()
        total_voters_reg_244 = len(total_voters_reg_244)
        print('total voters reg in NA-244', total_voters_reg_244)

        total_voters_reg_245 = self.db.collection('Voters').where(u'Sector', u'==', 'NA-245').get()
        total_voters_reg_245 = len(total_voters_reg_245)
        print('total voters reg in NA-245', total_voters_reg_245)

        total_can_reg_240 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-240').get()
        total_can_reg_240 = len(total_can_reg_240)
        print('total can reg in NA-240', total_can_reg_240)

        total_can_reg_241 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-241').get()
        total_can_reg_241 = len(total_can_reg_241)
        print('total can reg in NA-242', total_can_reg_241)

        total_can_reg_242 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-242').get()
        total_can_reg_242 = len(total_can_reg_242)
        print('total can reg in NA-242', total_can_reg_242)

        total_can_reg_243 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-243').get()
        total_can_reg_243 = len(total_can_reg_243)
        print('total can reg in NA-243', total_can_reg_243)

        total_can_reg_244 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-244').get()
        total_can_reg_244 = len(total_can_reg_244)
        print('total can reg in NA-244', total_can_reg_244)

        total_can_reg_245 = self.db.collection('Candidates').where(u'Sector', u'==', 'NA-245').get()
        total_can_reg_245 = len(total_can_reg_245)
        print('total can reg in NA-245', total_can_reg_245)

        try:

            data2 = {
                'TotalPopulation': 1000,
                'TotalVoterRegister': total_vote,
                'TotalVoteCast': total_vote_cast,
                'TotalPopulationNA240': 100,
                'TotalVoteRegisterNA240': total_voters_reg_240,
                'TotalVoteCastNA240': total_voters_240,
                'TotalCandidatesRegisterNA240': total_can_reg_240,
                'TotalPopulationNA241': 100,
                'TotalVoteRegisterNA241': total_voters_reg_241,
                'TotalVoteCastNA241': total_voters_241,
                'TotalCandidatesRegisterNA241': total_can_reg_241,
                'TotalPopulationNA242': 200,
                'TotalVoteRegisterNA242': total_voters_reg_242,
                'TotalVoteCastNA242': total_voters_242,
                'TotalCandidatesRegisterNA242': total_can_reg_242,
                'TotalPopulationNA243': 200,
                'TotalVoteRegisterNA243': total_voters_reg_243,
                'TotalVoteCastNA243': total_voters_243,
                'TotalCandidatesRegisterNA243': total_can_reg_243,
                'TotalPopulationNA244': 200,
                'TotalVoteRegisterNA244': total_voters_reg_244,
                'TotalVoteCastNA244': total_voters_244,

                'TotalCandidatesRegisterNA244': total_can_reg_244,
                'TotalPopulationNA245': 200,
                'TotalVoteRegisterNA245': total_voters_reg_245,
                'TotalVoteCastNA245': total_voters_245,
                'TotalCandidatesRegisterNA245': total_can_reg_245,
                'TotalParties': 6,
                'TotalCandidates': totalCandiates,
                'TotalIndependentCandidates': total_ind,
                'TotalVotesPartyA': total_voteA,
                'TotalVotesPartyB': total_voteB,
                'TotalVotesPartyC': total_voteC,
                'TotalVotesPartyD': total_voteD,
                'TotalVotesPartyE': total_voteE,
                'TotalVotesPartyF': total_voteF,
                'Party Won': won,
                'WonPartyVotes': won_votes

            }
            self.db.collection('VoterSummary').document('Karachi').set(data2)



        except:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Database Error', text='Data insertion failed', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            return

        doc_ref = self.db.collection('VoterSummary').document('Karachi')
        docs = doc_ref.get()
        if docs.exists:
            self.vote_summary = docs.to_dict()

        self.screen.get_screen('voting_result').ids.total_population.text = str(self.vote_summary['TotalPopulation'])
        self.screen.get_screen('voting_result').ids.vote_reg.text = str(self.vote_summary['TotalVoterRegister'])
        self.screen.get_screen('voting_result').ids.vote_cast.text = str(self.vote_summary['TotalVoteCast'])
        self.screen.get_screen('voting_result').ids.no_of_parties.text = str(6)
        self.screen.get_screen('voting_result').ids.no_of_ind.text = str(
            self.vote_summary['TotalIndependentCandidates'])
        self.screen.get_screen('voting_result').ids.party_won.text = str(
            self.vote_summary['Party Won']) + '  won by  ' + str(self.vote_summary['WonPartyVotes']) + '  votes'

    def create_pdf(self, pdf_path):
        pdf = CustomPDF()
        # Create the special value {nb}
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Times', '', 12)
        pdf.cell(0, 5, 'General Information:', ln=1)
        pdf.ln(10)
        data_gen = [['Total Population', str(self.vote_summary['TotalPopulation'])],
                    ['Total Voter Registered', str(self.vote_summary['TotalVoterRegister'])],
                    ['Total Vote Casted', str(self.vote_summary['TotalVoteCast'])],
                    ['Number of Parties', str(6)],
                    ['Total Seats', str(6)],
                    ['Number of Candidates', str(self.vote_summary['TotalCandidates'])],
                    ['Number of Independent Candidates', str(self.vote_summary['TotalIndependentCandidates'])],
                    ['Total Votes of Party A', str(self.vote_summary['TotalVotesPartyA'])],
                    ['Total Votes of Party B', str(self.vote_summary['TotalVotesPartyB'])],
                    ['Total Votes of Party C', str(self.vote_summary['TotalVotesPartyC'])],
                    ['Total Votes of Party D', str(self.vote_summary['TotalVotesPartyD'])],
                    ['Total Votes of Party E', str(self.vote_summary['TotalVotesPartyE'])],
                    ['Total Votes of Party F', str(self.vote_summary['TotalVotesPartyF'])],
                    ['Party Won', str(self.vote_summary['Party Won']) + '  won by  ' +
                     str(self.vote_summary['WonPartyVotes']) + '  votes'],
                    ]

        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        for row in data_gen:
            for item in row:
                pdf.cell(col_width * 2, row_height * 2,
                         txt=item, border=1)
            pdf.ln(row_height * 2)

        pdf.ln(20)
        pdf.cell(0, 5, 'NA-240:', ln=1)
        pdf.ln(10)
        data = [['Total Population', str(self.vote_summary['TotalPopulationNA240'])],
                ['Total Voter Registered', str(self.vote_summary['TotalVoteRegisterNA240'])],
                ['Total Vote Casted', str(self.vote_summary['TotalVoteCastNA240'])],
                ['Number of Candidates', str(self.vote_summary['TotalCandidatesRegisterNA240'])],
                ]

        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        for row in data:
            for item in row:
                pdf.cell(col_width * 2, row_height * 2,
                         txt=item, border=1)
            pdf.ln(row_height * 2)

        pdf.ln(20)
        pdf.cell(0, 5, 'NA-241:', ln=1)
        pdf.ln(10)
        data1 = [['Total Population', str(self.vote_summary['TotalPopulationNA241'])],
                 ['Total Voter Registered', str(self.vote_summary['TotalVoteRegisterNA241'])],
                 ['Total Vote Casted', str(self.vote_summary['TotalVoteCastNA241'])],
                 ['Number of Candidates', str(self.vote_summary['TotalCandidatesRegisterNA241'])],
                 ]

        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        for row in data1:
            for item in row:
                pdf.cell(col_width * 2, row_height * 2,
                         txt=item, border=1)
            pdf.ln(row_height * 2)

        pdf.ln(20)
        pdf.cell(0, 5, 'NA-242:', ln=1)
        pdf.ln(10)
        data2 = [['Total Population', str(self.vote_summary['TotalPopulationNA242'])],
                 ['Total Voter Registered', str(self.vote_summary['TotalVoteRegisterNA242'])],
                 ['Total Vote Casted', str(self.vote_summary['TotalVoteCastNA242'])],
                 ['Number of Candidates', str(self.vote_summary['TotalCandidatesRegisterNA242'])],
                 ]

        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        for row in data2:
            for item in row:
                pdf.cell(col_width * 2, row_height * 2,
                         txt=item, border=1)
            pdf.ln(row_height * 2)

        pdf.ln(20)
        pdf.cell(0, 5, 'NA-243:', ln=1)
        pdf.ln(10)
        data3 = [['Total Population', str(self.vote_summary['TotalPopulationNA243'])],
                 ['Total Voter Registered', str(self.vote_summary['TotalVoteRegisterNA243'])],
                 ['Total Vote Casted', str(self.vote_summary['TotalVoteCastNA243'])],
                 ['Number of Candidates', str(self.vote_summary['TotalCandidatesRegisterNA243'])],
                 ]

        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        for row in data3:
            for item in row:
                pdf.cell(col_width * 2, row_height * 2,
                         txt=item, border=1)
            pdf.ln(row_height * 2)

        pdf.ln(20)
        pdf.cell(0, 5, 'NA-244:', ln=1)
        pdf.ln(10)
        data4 = [['Total Population', str(self.vote_summary['TotalPopulationNA244'])],
                 ['Total Voter Registered', str(self.vote_summary['TotalVoteRegisterNA244'])],
                 ['Total Vote Casted', str(self.vote_summary['TotalVoteCastNA244'])],
                 ['Number of Candidates', str(self.vote_summary['TotalCandidatesRegisterNA244'])],
                 ]

        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        for row in data4:
            for item in row:
                pdf.cell(col_width * 2, row_height * 2,
                         txt=item, border=1)
            pdf.ln(row_height * 2)

        pdf.ln(20)
        pdf.cell(0, 5, 'NA-245:', ln=1)
        pdf.ln(10)
        data5 = [['Total Population', str(self.vote_summary['TotalPopulationNA245'])],
                 ['Total Voter Registered', str(self.vote_summary['TotalVoteRegisterNA245'])],
                 ['Total Vote Casted', str(self.vote_summary['TotalVoteCastNA245'])],
                 ['Number of Candidates', str(self.vote_summary['TotalCandidatesRegisterNA245'])],
                 ]

        col_width = pdf.w / 4.5
        row_height = pdf.font_size
        for row in data5:
            for item in row:
                pdf.cell(col_width * 2, row_height * 2,
                         txt=item, border=1)
            pdf.ln(row_height * 2)

        pdf.output(pdf_path)
        admin_email = []
        emails = self.db.collection('Admin').get()
        for admin in emails:
            email = admin.to_dict()
            admin_email.append(email['Email'])
            print(email['Email'])
        print(admin_email)
        send_mail(admin_email)


AdminAccess().run()
