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
        
        i = self.name[-1]
        app.screenMain.ids.TabPreparacao.ids[i].disabled = True
        app.screenMain.ids.TabAplicacao.ids[i].disabled = False
        app.sm.get_screen(f'Aplicacao{i}').setting([data["Frase1"],data["Frase2"],data["Frase3"]],
                                           data["Sequencia"])
        
        

class ScreenAplicacao(Screen):
    
    def setting(self, listaFrases, sequencia):
        self.listaFrases = listaFrases
        self.sequencia = sequencia
        
        nextFrase = app.sequencias[self.sequencia][0]  
        self.ids.FraseAplicacao.text = self.listaFrases[nextFrase]
    
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
        
        
        rotina = int(self.ids.contador.text[-1]) #da merda se passar de 10
        if rotina+1 == 9:
            self.ids.continuar.text = "Terminar"
            self.ids.error.text = "Ultima rotina..."
            
        if rotina > 8:
            app.sm.current = "Main"
            self.ids.contador.text = "Rotina: 1"
            self.ids.continuar.text = "Continuar"
            
            i = self.name[-1]
            app.screenMain.ids.TabPreparacao.ids[i].disabled = False
            app.screenMain.ids.TabAplicacao.ids[i].disabled = True
            return
        
        
        nextFrase = app.sequencias[self.sequencia][rotina]       
        self.ids.FraseAplicacao.text = self.listaFrases[nextFrase]
        
        
        self.ids.contador.text = f"Rotina: {rotina+1}"
        
    def Voltar(self):
        
        self.ids.error.text = ''
        self.ids.continuar.text = "Continuar"
        
        rotina = int(self.ids.contador.text[-1])-1
                
        if rotina < 1:
            self.ids.error.text = 'Primeira rotina, impossivel voltar.'
            return
        
        previousFrase = app.sequencias[self.sequencia][rotina-1]       
        self.ids.FraseAplicacao.text = self.listaFrases[previousFrase]
        
        
        self.ids.contador.text = f"Rotina: {rotina}"



class TabPreparacao(FloatLayout,MDTabsBase):
    pass



class TabAplicacao(FloatLayout,MDTabsBase):
    pass



class VoarApp(MDApp):
    def on_start(self):
        
        for child in self.screenMain.ids.TabAplicacao.ids.BotoesApli.children:
            child.disabled = True
        
    def build(self):
        
        self.sequencias = {"A":[0,1,2,0,1,2,0,1,2],     #A IDEIA É TROCAR
                           "B":[2,1,0,2,1,0,2,1,0],     #PELAS REAIS
                           "C":[0,0,0,1,1,1,2,2,2]}
        
        self.theme_cls.primary_palette = "Purple" 
        
        self.sm = ScreenManager(transition=NoTransition())
        
        self.screenMain = ScreenMain(name="Main")
        self.sm.add_widget(self.screenMain)
        
        self.screenPreparacaoC = ScreenPreparacao(name="PreparacaoC")
        self.sm.add_widget(self.screenPreparacaoC)
        
        self.screenAplicacaoC = ScreenAplicacao(name="AplicacaoC")
        self.sm.add_widget(self.screenAplicacaoC)
        
        self.screenPreparacaoN = ScreenPreparacao(name="PreparacaoN")
        self.sm.add_widget(self.screenPreparacaoN)
        
        self.screenAplicacaoN = ScreenAplicacao(name="AplicacaoN")
        self.sm.add_widget(self.screenAplicacaoN)
        
        self.screenPreparacaoI = ScreenPreparacao(name="PreparacaoI")
        self.sm.add_widget(self.screenPreparacaoI)
        
        self.screenAplicacaoI = ScreenAplicacao(name="AplicacaoI")
        self.sm.add_widget(self.screenAplicacaoI)
        
        return self.sm
        
app = VoarApp()
app.run()