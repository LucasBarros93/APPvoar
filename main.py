from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.gridlayout import MDGridLayout



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
            
    def Save(self):
        sequencia = ''
        for child in self.ids.sequencia.children:
            if child.md_bg_color != app.theme_cls.primary_light:
                sequencia = child.text
                break
        
        data = {"Frase1":self.ids.frase1.text,
                "Frase2":self.ids.frase2.text,
                "Frase3":self.ids.frase3.text,
                "Sequencia": sequencia}
        
        for key in data:
            if data[key] == "":
                self.ids.error.text = 'Preencha todos os itens antes de continuar'
                return
        
        #ENVIAR PARA O DRIVE()      ADICIONAR NO FUTURO
        self.Return()
        #app.screenMain.ids.TabPreparacao.ids."".disabled = True

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
        
        self.ids.error.text = ''
        
        
        listaFrases = ["frase1","frase2","frase3"] #PROVISRIO MUDAR COM DATABASE
        sequencia = "C" #PROVISRIO MUDAR COM DATABASE
        
        rotina = int(self.ids.contador.text[-1]) #da merda se passar de 10
        
        if rotina > 8:
            app.sm.current = "Main"
            self.ids.contador.text = "Rotina: 1"
            
            nextFrase = app.sequencias[sequencia][0]  
            self.ids.FraseAplicacao.text = listaFrases[nextFrase]
            return
        
        
        nextFrase = app.sequencias[sequencia][rotina]       
        self.ids.FraseAplicacao.text = listaFrases[nextFrase]
        
        
        self.ids.contador.text = f"Rotina: {rotina+1}"


class TabPreparacao(FloatLayout,MDTabsBase):
    pass

class TabAplicacao(FloatLayout,MDTabsBase):
    pass

class VoarApp(MDApp):
    def build(self):
        
        self.sequencias = {"A":[0,1,2,0,1,2,0,1,2],     #A IDEIA É TROCAR
                           "B":[2,1,0,2,1,0,2,1,0],     #PELAS REAIS
                           "C":[0,0,0,1,1,1,2,2,2]}
        
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