from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.gridlayout import MDGridLayout

from kivy import utils 


class Toggle(MDGridLayout):
    def onClick(self,button):        
        button.md_bg_color = app.theme_cls.primary_dark
    
        for child in self.children:
            if child != button:
                child.md_bg_color = app.theme_cls.primary_light
                



class ScreenMain(Screen):
    pass

class ScreenPreparacao(Screen):
    def Return(self):
        app.sm.current = "Main"
        
        self.ids.frase1.text = ''
        self.ids.frase2.text = ''
        self.ids.frase3.text = ''
        
        self.ids.error.text = ''
        
        for child in self.ids.sequencia.children:
            try:
                child.md_bg_color = app.theme_cls.primary_light
            except:
                pass

class ScreenAplicacao(Screen):
    def Return(self):
        app.sm.current = "Main"
        
    def Continue(self):
        
        error = True
        for child in self.ids.notas.children:
            
            if child.md_bg_color != app.theme_cls.primary_light:
                child.md_bg_color = app.theme_cls.primary_light
                error = False
        
        if error:
            self.ids.error.text = 'De uma nota antes de continuar'
            return
        
        listaFrases = ["frase1","frase2","frase3"] #PROVISRIO MUDAR COM DATABASE
        
        index = listaFrases.index(self.ids.FraseAplicacao.text)
        
        try:
            self.ids.FraseAplicacao.text = listaFrases[index+1]
        except:
            self.ids.FraseAplicacao.text = listaFrases[0]
            
        self.ids.error.text = ''


class TabPreparacao(FloatLayout,MDTabsBase):
    pass

class TabAplicacao(FloatLayout,MDTabsBase):
    pass

class VoarApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple" 
        
        self.sm = ScreenManager(transition=NoTransition())
        
        self.screenMain = ScreenMain(name="Main")
        self.sm.add_widget(self.screenMain)
        
        self.screenPreparacao = ScreenPreparacao(name="Preparacao")
        self.sm.add_widget(self.screenPreparacao)
        
        self.screenAplicacao = ScreenAplicacao(name="Aplicacao")
        self.sm.add_widget(self.screenAplicacao)
        
        return self.sm
        
app = VoarApp()
app.run()