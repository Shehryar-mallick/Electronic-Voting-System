screen_helper = '''
#:import CardTransition kivy.uix.screenmanager.CardTransition
#:import FallOutTransition kivy.uix.screenmanager.FallOutTransition
#:import NoTransition kivy.uix.screenmanager.NoTransition

ScreenManager:
    LogoScreen
    LoginScreen:
    MenuScreen:
    ProfileScreen:
    ShowAdmin:
    DisplayCandidate:
    VoteScreen:
    CandidateScreen:
    AddCandidateScreen:
    Timer:
    VotingResult:
    # Email:
<LogoScreen>
    name :'logoscreen'
    size : 1000,900
    Image:
        source: 'sskenterprise.jpg'
        size: self.texture_size
<LoginScreen>:
    name:'Login'
    MDLabel :
        text : 'ADMIN LOGIN '
        font_style : 'Button'
        font_size : 50
        halign : "center"
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        pos_hint : {"center_x":.5,"center_y":.9}
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDTextField:
        id: adminID
        hint_text:'enter AdminID'
        on_text_validate:password.focus = True
        required: True
        helper_text:'Required'
        helper_text_mode: 'on_error'
        icon_right:"account-box"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.65}
        size_hint_x:None
        width:280
    MDTextField:
        id: password
        hint_text:'enter password'
        password: True
        required: True
        helper_text:'Required'
        helper_text_mode: 'on_error'
        icon_right:"eye-off"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:280
    MDRectangleFlatButton:
        text:'Continue'
        pos_hint:{'center_x': 0.5, 'center_y': 0.33}
        custom_color: app.theme_cls.primary_color
        on_press:
            app. admin_login()
            app.root.transition = CardTransition(direction='left',mode='pop') 
<MenuScreen>:
    name:'Menu'
    MDCard:
        size_hint:(None,None)
        width:120
        height: 120
        pos_hint : {"center_x":.3,"center_y":.35}
        elevation:10
        padding:0
        focus_behavior: True
        MDIconButton:
            icon: "view-list"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            user_font_size: "100sp"
            elevation_normal: 12
            on_press:
                app.root.transition = CardTransition(direction='down',mode='pop') 
                root.manager.current = 'Candidate'
    MDCard:
        size_hint:(None,None)
        width:120
        height: 120
        pos_hint : {"center_x":.3,"center_y":.7}
        elevation:10
        padding:1
        focus_behavior: True
        MDIconButton:
            icon: "archive-arrow-down"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            user_font_size: "100sp"
            elevation_normal: 12
            on_press:
                app.root.transition = CardTransition(direction='left',mode='pop')  
                root.manager.current = 'display_candidate'
                app.show_candidate()
    MDCard:
        size_hint:(None,None)
        width:120
        height: 120
        pos_hint : {"center_x":.73,"center_y":.35}
        elevation:10
        padding:1
        focus_behavior: True
        MDIconButton:
            icon: "account"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            user_font_size: "100sp"
            elevation_normal: 12
            on_press:
                app.root.transition = CardTransition(direction='right',mode='pop')  
                root.manager.current = 'Profile'
                app.profile()
    MDCard:
        size_hint:(None,None)
        width:120
        height: 120
        pos_hint : {"center_x":.73,"center_y":.7}
        elevation:10
        padding:1
        focus_behavior: True
        MDIconButton:
            icon: "logout"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            user_font_size: "100sp"
            elevation_normal: 12
            on_press:
                app.root.transition = CardTransition(direction='left',mode='pop')  
                root.manager.current = 'Vote'
                app.show_voter()
    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.root.transition = NoTransition()
                root.manager.current = 'clock'
            icon: 'clock'
    MDRectangleFlatIconButton:
        text:'Logout'
        # size_hint:(0.8, 0.09)
        icon: "logout"
        font_size:25
        pos_hint:{'center_x': 0.87, 'center_y': 0.95}
        on_press: 
            # app.stop()
            app.logout_admin()
<ProfileScreen>:
    name:'Profile'
    BoxLayout:
        orientation: 'vertical'
    Image:
        id: imagePath
        size_hint_y: None  # Tells the layout to ignore the size_hint in y dir
        height: dp(200)
        pos_hint: {"center_x":.2,"center_y":.65}
    MDLabel :
        text : 'Profile Window '
        font_style : 'Button'
        font_size : 40
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.96}
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        text : 'Name: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        pos_hint : {"center_x":.5,"center_y":.7}
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        text : 'Email: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.6}
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        text : 'Password: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.5}
        size_hint_y : None
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        text : 'Mobile Number:'
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.4}
        size_hint_y : None
        height : self.texture_size[1]
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        padding_y : 15
    MDLabel :
        text : 'AdminID: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.3}
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        id: name
        # text : 'Name: '
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        pos_hint : {"center_x":.7,"center_y":.7}
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        id: email
        # text : 'Email: '
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.75,"center_y":.6}
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        id: password
        # text : 'Password: '
        # font_style : 'Button'
        type: 'Password'
        font_size : 20
        # Password: True
        halign : "center"
        pos_hint : {"center_x":.71,"center_y":.5}
        size_hint_y : None
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        id: mobileNumber
        # text : 'Mobile Number:'
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.69,"center_y":.4}
        size_hint_y : None
        height : self.texture_size[1]
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        padding_y : 15
    MDLabel :
        id: adminId
        # text : 'AdminID: '
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.7,"center_y":.3}
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDRectangleFlatButton:
        id: viewAdmins
        text:'View Admins'
        disabled: True
        remove_widget: False
        pos_hint:{'center_x': 0.6, 'center_y': 0.2}
        border: 30,30,30,30
        on_press:
            root.manager.current = 'showAdmin'
            app. show_admin()
            app.root.transition = CardTransition(direction='left',mode='pop') 
    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.root.transition = NoTransition()
                root.manager.current = 'Menu'
            icon: 'language-python'
<ShowAdmin>
    name: 'showAdmin'  
    ScrollView:               
        MDList:
            spacing: '25dp'
            padding: '45dp' 
            id: scroll
    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.root.transition = NoTransition()
                root.manager.current = 'Profile'
            icon: 'language-python'
<VoteScreen>:
    name:'Vote'
    AnchorLayout:
        id:anchor_layout
    MDToolbar:
        title: 'SHOW VOTERS'
        type: 'top'
        pos_hint: {"top": 1}
        right_action_items: [["plus", lambda x: app.voter_excel()]]
        elevation:5
    # MDLabel:
    #     id: vote_label
    #     halign:'center'
    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.root.transition = NoTransition()
                root.manager.current = 'Menu'
            icon: 'language-python'
<DisplayCandidate>:
    name:'display_candidate'
    AnchorLayout:
        id:anchor_layout
    # MDLabel:
    #     id: candidate_label
    #     halign:'center'
    MDToolbar:
        title: 'ADD CANDIDATES'
        type: 'top'
        pos_hint: {"top": 1}
        right_action_items: [["account-plus", lambda x: app.nav_draw()],["plus", lambda x: app.candidate_excel()]]
        elevation:5
    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.root.transition = NoTransition()
                root.manager.current = 'Menu'
            icon: 'language-python'
<CandidateScreen>:
    name:'Candidate'
    MDRectangleFlatButton:
        text:'Download Images'
        font_size:25
        pos_hint:{'center_x': 0.5, 'center_y': 0.75}
        on_press:
            app.download_images()
    MDRectangleFlatButton:
        text:'Training Images'
        font_size:25
        pos_hint:{'center_x': 0.5, 'center_y': 0.55}
        on_press:
            app.training_images()
    MDRectangleFlatButton:
        text:'Vote Summary'
        font_size:25
        pos_hint:{'center_x': 0.5, 'center_y': 0.35}
        on_press:
            app.set_time_result()
    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.root.transition = NoTransition()
                root.manager.current = 'Menu'
            icon: 'language-python'
<AddCandidateScreen>:
    name:'Add_Candidate'
    MDTextField:
        id : candidate_name
        hint_text: "Candidate Name"
        on_text_validate:party_name.focus = True
        icon_right : "account-box"
        required: True
        helper_text_mode: "on_error"
        helper_text: "Required"
        size_hint_x:None
        width:250
        pos_hint:{'center_x': 0.5, 'center_y': 0.8}
    MDTextField:
        id : party_name
        hint_text: "Political Party Name"
        on_text_validate:cnic.focus = True
        required: True
        helper_text_mode: "on_error"
        icon_right : "account-box"
        helper_text: "Required"
        size_hint_x:None
        width:250
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        on_focus: if self.focus: app.menu_party.open()
    MDTextField:
        id : cnic
        hint_text: "CNIC"
        on_text_validate:town.focus = True
        input_filter : 'int'
        required: True
        helper_text_mode: "on_error"
        icon_right : "id-card"
        helper_text: "Required"
        max_text_length: 13
        size_hint_x:None
        width:250
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
    MDTextField:
        id : town
        hint_text: "Town"
        on_text_validate:sector.focus = True
        required: True
        helper_text_mode: "on_error"
        icon_right : "home"
        helper_text: "Required"
        size_hint_x:None
        width:250
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        on_focus: if self.focus: app.menu.open()
    # MDTextField:
    #     id : sector
    #     hint_text: "Sector"
    #     required: True
    #     helper_text_mode: "on_error"
    #     helper_text: "Required and must not exceed 30 characters"
    #     max_text_length: 20
    #     size_hint_x:None
    #     width:250
    #     pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    #     on_focus: if self.focus: app.menu_sector.open()
    MDRectangleFlatButton:
        text:'SUBMIT'
        font_size:25
        pos_hint:{'center_x': 0.5, 'center_y': 0.35}
        on_press: app.submit()
    MDRectangleFlatButton:
        text:'BACK'
        font_size:25
        pos_hint:{'center_x': 0.5, 'center_y': 0.25}
        on_press: 
            app.root.transition = NoTransition()
            root.manager.current = 'display_candidate'      
<Timer>:
    name:'clock'
    MDTextField:
        id: start_time_registration
        hint_text:'enter start time for registration'
        on_text_validate:end_time_registration.focus = True
        helper_text:'2021-01-25'
        helper_text_mode: 'on_focus'
        icon_right:"clock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.85}
        size_hint_x:None
        width:280
    MDTextField:
        id: end_time_registration
        hint_text:'enter end time for registration'
        on_text_validate:start_time_voting.focus = True
        helper_text:'2021-01-25'
        helper_text_mode: 'on_focus'
        icon_right:"clock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.75}
        size_hint_x:None
        width:280
    MDTextField:
        id: start_time_voting
        hint_text:'enter start time for voting'
        on_text_validate:end_time_voting.focus = True
        helper_text:'2021-01-25'
        helper_text_mode: 'on_focus'
        icon_right:"clock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.65}
        size_hint_x:None
        width:280
    MDTextField:
        id: end_time_voting
        hint_text:'enter end time for voting'
        helper_text:'2021-01-25'
        helper_text_mode: 'on_focus'
        icon_right:"clock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.55}
        size_hint_x:None
        width:280
    MDTextField:
        id: start_result
        hint_text:'enter start time for Result'
        helper_text:'2021-01-25'
        helper_text_mode: 'on_focus'
        icon_right:"clock"
        icon_right_color: app.theme_cls.primary_color
        pos_hint:{'center_x': 0.5, 'center_y': 0.45}
        size_hint_x:None
        width:280
    MDRectangleFlatButton:
        text:'Submit'
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
        on_press:app.save_time() 
    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.root.transition = NoTransition()
                root.manager.current = 'Menu'
            icon: 'language-python'
<VotingResult>
    name:'voting_result'
    MDLabel :
        text : 'Voting Result'
        font_style : 'Button'
        font_size : 40
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.96}
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        text : 'Total Population: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        pos_hint : {"center_x":.5,"center_y":.8}
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        text : 'Vote Registered: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.7}
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        text : 'Total Number of Vote Cast: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.6}
        size_hint_y : None
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        text : 'Number of Parties:'
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.5}
        size_hint_y : None
        height : self.texture_size[1]
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        padding_y : 15
    MDLabel :
        text : 'Number of Independent: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.4}
        size_hint_y : None
        height : self.texture_size[1]
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        padding_y : 15
    MDLabel :
        text : 'Party won The Election: '
        font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.5,"center_y":.3}
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15   
    MDLabel :
        id: total_population
        # text : 'Name: '
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        pos_hint : {"center_x":.7,"center_y":.8}
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        id: vote_reg
        # text : 'Email: '
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.65,"center_y":.7}
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        id: vote_cast
        # text : 'Password: '
        # font_style : 'Button'
        type: 'Password'
        font_size : 20
        # Password: True
        halign : "center"
        pos_hint : {"center_x":.71,"center_y":.6}
        size_hint_y : None
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        height : self.texture_size[1]
        padding_y : 15
    MDLabel :
        id: no_of_parties
        # text : 'Mobile Number:'
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.69,"center_y":.5}
        size_hint_y : None
        height : self.texture_size[1]
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        padding_y : 15
    MDLabel :
        id: no_of_ind
        # text : 'Mobile Number:'
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.69,"center_y":.4}
        size_hint_y : None
        height : self.texture_size[1]
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        padding_y : 15
    MDLabel :
        id: party_won
        # text : 'AdminID: '
        # font_style : 'Button'
        font_size : 20
        halign : "center"
        pos_hint : {"center_x":.8,"center_y":.3}
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        size_hint_y : None
        height : self.texture_size[1]
        padding_y : 15   
    # MDRectangleFlatButton:
    #     text:'Add mailing address'
    #     pos_hint:{'center_x': 0.5, 'center_y': 0.23}
    #     on_press:root.manager.current = 'email'
    #     

    MDRectangleFlatButton:
        text:'Detailed Report'
        pos_hint:{'center_x': 0.5, 'center_y': 0.15}
        on_press:app.create_pdf('DetailedReport.pdf')
    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.root.transition = NoTransition()
                root.manager.current = 'Menu'
            icon: 'language-python'
# <Email>:
#     name:'email'
#     MDLabel :
#         text : 'Add New Email'
#         font_style : 'Button'
#         font_size : 50
#         halign : "center"
#         theme_text_color: "Custom"
#         text_color: app.theme_cls.primary_color
#         pos_hint : {"center_x":.5,"center_y":.9}
#         size_hint_y : None
#         height : self.texture_size[1]
#         padding_y : 15
#     
#     MDTextField:
#         id: emailID
#         hint_text:'enter New Email'
#         on_text_validate:password.focus = True
#         required: True
#         helper_text:'Required'
#         helper_text_mode: 'on_error'
#         icon_right:"account-box"
#         icon_right_color: app.theme_cls.primary_color
#         pos_hint:{'center_x': 0.5, 'center_y': 0.65}
#         size_hint_x:None
#         width:280
# 
#     MDRectangleFlatButton:
#         text:'ENTER'
#         pos_hint:{'center_x': 0.5, 'center_y': 0.45}
#         on_press:app.add_new_mail()
#         
# 
# 
#     MDRectangleFlatButton:
#         text:'BACK'
#         pos_hint:{'center_x': 0.5, 'center_y': 0.25}
#         on_press:root.manager.current = 'voting_result'
# 
# 
'''