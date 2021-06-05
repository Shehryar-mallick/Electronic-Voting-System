help_str = '''

ScreenManager:
    LogoScreen
    LoginScreen1
    DetectionWindow
    SIGNUPScreen1
    SIGNUPScreen2
    SIGNUPScreen3
    Dashboard

<LogoScreen>
    name :'logoscreen'
    Image:
        source: 'sskenterprise.jpg'
        size: self.texture_size

<LoginScreen1>
    name:'loginscreen1'

    MDScreen :
        md_bg_color : [39/255,36/255,67/255,1]
        size : 1000,900

        MDCard :
            size_hint : None,None
            size : 400,400
            pos_hint : {"center_x":.5,"center_y":.5}
            elevation : 15
            md_bg_color : [255/255,255/255,255/255,1]
            padding :50
            spacing : 30
            orientation : "vertical"
            # Adding items to the card
            MDLabel :
                text : 'LOGIN'
                font_style : 'Button'
                font_size : 45
                halign : "center"
                size_hint_y : None
                height : self.texture_size[1]
                padding_y : 15

            MDTextField :
                id :usercnicno
                hint_text : "Enter your CNIC"
                mode: "rectangle"
                input_filter : 'int'
                mode: "fill"
                max_text_length : 13
                fill_color: 0,0,0,0.03
                size_hint : 1,None
                icon_right : "id-card"
                width : 300
                required: True
                helper_text_mode: "on_error"
                helper_text: "Required"
                font_size : 15
                pos_hint : {"center_x":.5}
                normal_color : [35/255,49/255,48/255,1]
                color_active : [1,1,1,1]


            MDRectangleFlatButton :
                text : "LOGIN"
                font_size : 15
                pos_hint : {"center_x":.5}
                theme_text_color : "Custom"
                text_color : [0,0,0,1]
                on_press:
                    app.set_time_voting() 
                    

            MDRectangleFlatButton :
                text : "REGISTER"
                font_size : 15
                pos_hint : {"center_x":.5}
                theme_text_color : "Custom"
                text_color : [0,0,0,1]
                on_press: 
                    app.set_time_registration()
                    # root.manager.current = 'signupscreen1' 
                    root.manager.transition.direction = 'left'
                    
<DetectionWindow>
    name:'detection'
    
    MDToolbar:
        id: toolbar
        title: 'Almost there!'
        pos_hint: {"top": 1}
        elevation:10

    # MDLabel:
    #     text:'Almost there!'
    #     color: rgba("#ffffff")
    #     font_style:'H2'
    #     pos:(30,250)
    #     canvas.before:
    #         Color:
    #             rgb: 33/243, 150/243, 243/243
    #         Rectangle:
    #             pos: (0,500)
    #             size: 900,250

    MDLabel:
        text:'Read the instructions carefully'
        halign: 'center'
        color: rgba("#120639")
        font_style:'H3'
        pos_hint : {'center_x': 0.5, 'center_y': 0.85}
        # pos:(140,170)

    MDLabel:
        text:'1.Inorder to proceed to voting window you need to validate the identification.\\n2.Press the identification button inorder to start the process.\\n3.Make sure to keep your head infront of the camera to avoid any \\n   inconvenience\\n4.Make sure you have adequate light so that the system does not\\n   reject your access.\\n5.However, if you are not sure to vote at this moment then press back button\\n   because once you enter you are obliged to vote\\n6.Incase if the system does not recognize your face for more than five\\n   seconds then you can press Q to quit\\n7.Dont forget to take your glasses off ;)'
        color: rgba("#120639")
        halign: 'center'
        font_size:24
        pos_hint : {'center_x': 0.5, 'center_y': 0.5}
        # pos:(40,-35)



    Button:
        text:'IDENTIFY'
        font_color: rgba("#ffffff")
        font_size:24
        pos_hint:{'center_x': 0.3, 'center_y': 0.1}
        background_normal: ''
        background_color: rgba("#2196f3")
        size: 250, 50
        size_hint: None, None
        # pos:(530,30)
        on_press:
            app.printpress()

    Button:
        text:'BACK'
        font_color: rgba("#ffffff")
        font_size:24
        pos_hint:{'center_x': 0.75, 'center_y': 0.1}
        background_normal: ''
        background_color: rgba("#2196f3")
        size: 250, 50
        size_hint: None, None
        # pos:(100,30)
        on_press:
            app.logout()



<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color


<Dashboard>
    name: 'dashboard'
    
    ScreenManager:
        id: screen_manager
        Screen:
            id: screen1
            ScrollView:
                
                size_hint_y: 1.0 - toolbar.height/root.height
                spacing: '25dp'
                padding: '40dp'

                MDList:
                    spacing: '25dp'
                    padding: '40dp' 
                    id: scroll
                    
            
                    # MDLabel:
                    #     text : 'Name'
                    #     id : name
                    #     font_style: "Subtitle1"
                    #     size_hint_y: None
                    #     font_size : 15
                    #     halign : "center"
                    #     height : self.texture_size[1]
                    #     padding_y : 5
                    # MDLabel:
                    #     text : 'CNIC'
                    #     id : CNIC
                    #     size_hint_y: None
                    #     font_style: "Caption"
                    #     font_size : 15
                    #     halign : "center"
                    #     height : self.texture_size[1]
                    #     padding_y : 5
                    #     
                    # MDLabel:
                    #     text : 'Sector'
                    #     id : Sector
                    #     size_hint_y: None
                    #     font_style: "Caption"
                    #     font_size : 15
                    #     halign : "center"
                    #     height : self.texture_size[1]
                    #     padding_y : 5
                    # 
                    #          
            BoxLayout:
                orientation: 'vertical'
                id: box_layout
                MDToolbar:
                    id: toolbar
                    title: 'Electronic Voting System'
                    left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
                    elevation:5
                    
                Widget:
                    
                    
                    
                    
    MDNavigationDrawer:
        id: nav_drawer
        disabled: False
        
        ContentNavigationDrawer:
            orientation: 'vertical'
            padding: "8dp"
            spacing: "8dp"
            Image:
                id: avatar
                size_hint: (1,1)
                # source: "1483014874893.jpg"
            MDLabel:
                text : 'Name'
                id : name
                font_style: "Subtitle1"
                size_hint_y: None
                font_size : 15
                halign : "center"
                height : self.texture_size[1]
                padding_y : 5
            MDLabel:
                text : 'CNIC'
                id : CNIC
                size_hint_y: None
                font_style: "Caption"
                font_size : 15
                halign : "center"
                height : self.texture_size[1]
                padding_y : 5
                
            MDLabel:
                text : 'Sector'
                id : Sector
                size_hint_y: None
                font_style: "Caption"
                font_size : 15
                halign : "center"
                height : self.texture_size[1]
                padding_y : 5
            ScrollView:
                DrawerList:
                    id: md_list

                    MDList:
                        
                        

    
                                
                                        
    # name:'dashboard'
    # MDToolbar:
    #     id: toolbar
    #     title: "Electronic Voting System"
    #     #specific_text_color: 0, 0, 0, 1
    #     #md_bg_color: 1, 1, 1, 1
    #     pos_hint: {"top": 1}
    #     elevation: 11
    #     
    # ScreenManager:
    #     Screen:
    #         MDLabel :
    #             text : 'Name'
    #             id : name
    #             font_style : "Button"
    #             pos_hint : {"center_x":.1,"center_y":.85}
    #             font_size : 15
    #             halign : "center"
    #             size_hint_y : None
    #             height : self.texture_size[1]
    #             padding_y : 25
    #         MDLabel :
    #             text : 'CNIC'
    #             id : CNIC
    #             font_style : "Button"
    #             pos_hint : {"center_x":.45,"center_y":.85}
    #             font_size : 15
    #             halign : "center"
    #             size_hint_y : None
    #             height : self.texture_size[1]
    #             padding_y : 25
    #         MDLabel :
    #             text : 'Sector'
    #             id : Sector
    #             font_style : "Button"
    #             pos_hint : {"center_x":.85,"center_y":.85}
    #             font_size : 15
    #             halign : "center"
    #             size_hint_y : None
    #             height : self.texture_size[1]
    #             padding_y : 25
    # 
    # 
    # 
    #         ScrollView:
    # 
    # 
    #             MDList:
    #                 id: scroll
            
<SIGNUPScreen1>
    name:'signupscreen1'
    MDScreen :
        md_bg_color : [39/255,36/255,67/255,1]
        size : 1000,900
        MDCard :
            orientation : 'vertical'
            size_hint : None,None
            id : mdcard1
            size : 500,450
            pos_hint : {"center_x":.5,"center_y":.5}
            elevation : 15
            md_bg_color : [255/255,255/255,255/255,1]
            padding : 20
            spacing : 10
            MDLabel :
                text : "SIGN-UP"
                font_style : "Button"
                pos_hint : {"center_x":.5,"center_y":.1}
                font_size : 25
                halign : "center"
                size_hint_y : None
                height : self.texture_size[1]
                padding_y : 25
            MDTextField :
                id : name
                hint_text : "Full Name"
                on_text_validate:mobilenumber.focus = True
                mode: "rectangle"
                mode: "fill"
                fill_color: 0,0,0,0.03
                color_active : [13/255,227/255,243/255,1]
                text_color : [8/255,68/255,10/255,1]
                color_active : [13/255,227/255,243/255,1]
                line_color_normal : [13/255,227/255,243/255,1]
                size_hint : .7,None
                required: True
                helper_text_mode: "on_error"
                helper_text: "Required"
                icon_right : "account-box"
                width : 270
                font_size : 15
                pos_hint : {"center_x":.5}

            MDTextField :
                hint_text : "mobile number"
                mode: "rectangle"
                input_filter : 'int'
                max_text_length:11
                mode: "fill"
                fill_color: 0,0,0,0.03
                size_hint : .7,None
                icon_right : "phone"
                width : 270
                font_size : 15
                on_text_validate:usercnicno.focus = True
                required: True
                helper_text_mode: "on_error"
                helper_text: "Required"
                pos_hint : {"center_x":.5}
                normal_color : [35/255,49/255,48/255,1]
                color_active : [1,1,1,1]
                id : mobilenumber
            MDTextField :
                hint_text : "user-cnic-no"
                mode: "rectangle"
                input_filter : 'int'
                mode: "fill"
                max_text_length : 13
                fill_color: 0,0,0,0.03
                on_text_validate:useremail.focus = True
                size_hint : .7,None
                icon_right : "id-card"
                width : 270
                required: True
                helper_text_mode: "on_error"
                helper_text: "Required"
                font_size : 15
                pos_hint : {"center_x":.5}
                normal_color : [35/255,49/255,48/255,1]
                color_active : [1,1,1,1]
                id :usercnicno
            MDTextField :                                       
                hint_text : "Email ID"
                mode: "rectangle"
                mode: "fill"
                fill_color: 0,0,0,0.03
                on_text_validate:signup1_btn.focus = True
                size_hint : .7,None
                icon_right : "id-card"
                width : 270
                font_size : 15
                required: True
                helper_text_mode: "on_error"
                helper_text: "Required"
                pos_hint : {"center_x":.5}
                normal_color : [35/255,49/255,48/255,1]
                color_active : [1,1,1,1]
                id :useremail


            MDLabel :
                text : 'Already have a account, LOGIN'
                underline : True
                font_size : 13
                pos_hint : {"center_x":1.13,"center_y":1.2}
                height : self.texture_size[1]
                spacing : 5
                id :login_txt
            MDRectangleFlatButton :
                text : "CONTINUE"
                font_size : 15
                spacing:5
                pos_hint : {"center_x":.5}
                theme_text_color : "Custom"
                disabled: False
                text_color : [0,0,0,1]
                id : signup1_btn
                on_press: 
                    app.signup()
                    root.manager.transition.direction = 'left'

            MDRectangleFlatButton :
                text : "BACK"
                font_size : 15
                pos_hint : {"center_x":.5}
                theme_text_color : "Custom"
                text_color : [0,0,0,1]
                on_press: 
                    root.manager.current = 'loginscreen1'  
                    root.manager.transition.direction = 'right'


<SIGNUPScreen2>
    name:'signupscreen2'
    MDScreen :
        md_bg_color : [39/255,36/255,67/255,1]
        size : 1000,900
        MDCard :
            orientation : 'vertical'
            size_hint : None,None
            id : mdcard2
            size : 500,450
            pos_hint : {"center_x":.5,"center_y":.5}
            elevation : 15
            md_bg_color : [227/255,245/255,245/255,1]
            padding : [15,15,15,15]
            spacing : 10
            MDLabel :
                text : "SIGN-UP"
                font_style : "Button"
                pos_hint : {"center_x":.5,"center_y":.1}
                font_size : 25
                halign : "center"
                size_hint_y : None
                height : self.texture_size[1]
                padding_y : 25

            MDTextField :
                hint_text : "House Number/Flat Number"
                mode: "rectangle"
                on_text_validate:town.focus = True
                mode: "fill"
                fill_color: 0,0,0,0.02
                size_hint : .7,None
                icon_right : "home-city"
                width : 270
                font_size : 15
                pos_hint : {"center_x":.5}
                required: True
                helper_text_mode: "on_error"
                helper_text: "Required"
                normal_color : [35/255,49/255,48/255,1]
                color_active : [1,1,1,1]
                id :address


            MDTextField:
                id: town
                hint_text : "Town"
                on_text_validate:city.focus = True
                mode: "rectangle"
                mode: "fill"
                fill_color: 0,0,0,0.02
                icon_right : "home"
                size_hint : .7,None
                size : 200,200
                font_size : 15
                pos_hint : {"center_x":.5}
                normal_color : [35/255,49/255,48/255,1]
                color_active : [1,1,1,1]
                required: True
                helper_text_mode: "on_error"
                helper_text: "Required"                     
                on_focus: 
                    if self.focus:app.menu.open()



            MDTextField :
                id :city
                text : "Karachi"
                on_text_validate:date_picker.focus = True
                mode: "rectangle"
                mode: "fill"
                fill_color: 0,0,0,0.02
                icon_right : "home"
                size_hint : .7,None
                size : 200,200
                font_size : 15
                pos_hint : {"center_x":.5}
                normal_color : [35/255,49/255,48/255,1]
                color_active : [1,1,1,1]
                required: True
                helper_text_mode: "on_error"
                helper_text: "Required"      
                

            MDRectangleFlatIconButton:
                size_hint : .7,None
                id:date_picker
                text:'Date Of Birth'
                icon_right : "cake"
                required: True
                font_size : 16
                pos_hint : {"center_x":.5}
                text_color:0, 0, 0, .4
                md_bg_color: 0, 0, 0, 0.02

                on_press : app.show_date_picker()
            MDRectangleFlatButton :
                text : "CONTINUE"
                font_size : 15
                spacing:5
                pos_hint : {"center_x":.5}
                theme_text_color : "Custom"
                text_color : [0,0,0,1]
                on_press: 
                    app.signup2() 
                    root.manager.transition.direction = 'left'
            MDRectangleFlatButton :
                text : "CANCEL"
                font_size : 15
                pos_hint : {"center_x":.5}
                theme_text_color : "Custom"
                text_color : [0,0,0,1]
                on_press: 
                    root.manager.current = 'signupscreen1' 
                    root.manager.transition.direction = 'left'

<SIGNUPScreen3>
    name:'signupscreen3'
    MDScreen :
        size : 1000,900
        BoxLayout:
            orientation: "vertical"
            MDToolbar:
                title: "ALMOST THERE!"
                font_size: 20
                bold: True
            BoxLayout:
                padding: [20, 20, 20, 20]
                orientation: "vertical"
                MDLabel:
                    text: "Read the instructions carefully!"
                    text_size: self.size
                    font_size: 20
                    bold: True
                    halign: 'center'
                    valign: 'middle'
                MDLabel:
                    text: "1. After pressing continue button, your webcam will be opened and you will be prompted to take a photo."
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'

                MDLabel:
                    text: "2. Align your face directly in front of camera and press 's' key to take photo only when the square box appears around your face. Don't click anywhere else on the screen."
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                MDLabel:
                    text: "3. Voters must REMOVE any kind of glasses from their faces before taking photograph."
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                MDLabel:
                    text: "4. This process will take place only ONCE. Any kind of disturbance or distortion during the process will result in cancellation of vote."
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                MDLabel:
                    text: "5. You cannot go back once you press the continue button."
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                MDLabel:
                    text: "6. Make sure you take photo in proper lighting. Don't capture the photo in darkness."
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'
                MDLabel:
                    text: "7. As soon as the photo is taken, the webcam will be closed automatically and you will be redirected towards the Login page. "
                    text_size: self.size
                    halign: 'center'
                    valign: 'middle'

                BoxLayout:
                    orientation: "vertical"
                    MDFillRoundFlatButton:
                        text: "Continue"                       
                        pos_hint: {"center_x": .5}
                        on_release:
                            app.detection()


'''
