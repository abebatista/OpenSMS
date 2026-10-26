from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDListItem

from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ColorProperty
from kivy.metrics import dp, sp
from kivy.utils import platform

Builder.load_string('''

<EndPointUrl>
    padding: dp(16)
    MDListItemLeadingIcon:
        icon: "link"
    MDListItemHeadlineText:
        text: root.url
    MDListItemSupportingText:
        text: root.iface_name
    MDFabButton:
        icon: "content-copy"
        style: "small"
        theme_bg_color: "Custom"
        md_bg_color: "#adcfdb"
        pos_hint: {'center_y': 0.5}
        on_release: root.copy_url(root.url)

<ButtonControl>
    pos_hint: {"center_x": .5}
    theme_bg_color: "Custom"
    md_bg_color: self.btn_colour
    MDButtonIcon:
        icon: root.btn_icon
    MDButtonText:
        text: root.btn_txt

<DocButton>
    pos_hint: {"center_x": .5}
    theme_bg_color: "Custom"
    md_bg_color: self.btn_colour
    on_release: app.api_doc_link()
    MDButtonIcon:
        icon: root.btn_icon
    MDButtonText:
        text: root.btn_txt
        theme_text_color: "Custom"
        text_color: "black"

<AppHomeBox>:
    orientation: 'vertical'
    #md_bg_color: '#7643a8'
    spacing: dp(8)

    MDScrollView:
        do_scroll_x: False
        bar_width: 0

        MDBoxLayout:
            id: home_scr_main_box
            orientation: "vertical"
            adaptive_height: True
            spacing: dp(8)

            MDCard:
                orientation: "vertical"
                size_hint_y: None
                height: dp(192)
                padding: dp(16)
                spacing: dp(8)
                radius: [24, 24, 24, 24]
                theme_bg_color: "Custom"
                md_bg_color: "#17345c"

                MDLabel:
                    text: "SMS API / GATEWAY"
                    font_style: "Headline"
                    role: "small"
                    theme_text_color: "Custom"
                    text_color: "#b8cae2"
                    adaptive_height: True

                MDLabel:
                    text: "Status"
                    font_style: "Label"
                    role: "medium"
                    theme_text_color: "Custom"
                    text_color: "#ffffff"
                    adaptive_height: True

                MDLabel:
                    id: api_srv_lbl
                    text: "API Server is not running"
                    font_style: "Body"
                    role: "medium"
                    theme_text_color: "Custom"
                    text_color: "#e4ecf7"
                    adaptive_height: True

                Widget:
                    size_hint_y: 1

                ButtonControl:
                    id: api_srv_btn
                    btn_colour: "#168b68"
                    style: "filled"
                    on_release: app.api_server_mgr(self)

            MDCard:
                orientation: "vertical"
                size_hint_y: None
                adaptive_height: True
                padding: dp(16)
                spacing: dp(8)
                radius: [24, 24, 24, 24]
                theme_bg_color: "Custom"
                md_bg_color: "#0b4537"

                MDLabel:
                    text: "API Endpoints"
                    font_style: "Headline"
                    role: "small"
                    theme_text_color: "Custom"
                    text_color: "#b8cae2"
                    adaptive_height: True

                MDBoxLayout:
                    id: endpoint_box
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: dp(16)


''')

class AppHomeBox(MDBoxLayout):
    pass

class ButtonControl(MDButton):
    btn_icon = StringProperty("play")
    btn_txt = StringProperty("Start Server")
    btn_colour = "green"

class DocButton(MDButton):
    btn_icon = StringProperty("file-document-check")
    btn_txt = StringProperty("API Docs")
    btn_colour = "#d5b9eb"

class EndPointUrl(MDListItem):
    url = StringProperty("")
    iface_name = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_name = "opensms"

    def copy_url(self, instance=None):
        Clipboard.copy(self.url)
