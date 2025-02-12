import flet as ft

def main(page: ft.Page):
    page.title = "Ajudante da Hidratação"
    
    def go_to_page1(e):
        page.controls.clear()
        page.add(ft.Text("Seja Bem-Vindo ao nosso Ajudante da hidratação"))
        page.add(ft.Text("Realize seu cadastro para começar com sua jornada para se manter hidratado"))
        page.add(ft.ElevatedButton("Cadastramento de Login", on_click=go_to_page2))
        page.update()
    
    def go_to_page2(e):
        page.controls.clear()
        page.add(ft.Text("Cadastramento de Login"))
        
        dropdown = ft.Dropdown(
            label="Faixa de idade",
            options=[
                ft.dropdown.Option("8-12 anos"),
                ft.dropdown.Option("13-17 anos"),
                ft.dropdown.Option("18-24 anos"),
            ]
        )
        
        row_buttons = ft.Row(
            controls=[
                ft.FilledButton("Refazer", on_click=go_to_page1),
                ft.ElevatedButton("Concluído", on_click=go_to_page3),
            ]
        )
        
        page.add(
            ft.TextField(label="Digite seu nome completo"),
            ft.TextField(label="Digite seu e-mail"),
            ft.TextField(label="Digite sua senha", password=True),
            dropdown,
            row_buttons
        )
        page.update()

    def go_to_page3(e):
        page.controls.clear()
        page.add(ft.Text("PARABÉNS!!! Você é o nosso Mais Novo Membro"))
        page.add(ft.ElevatedButton("Voltar", on_click=go_to_page2))
        page.add(ft.ElevatedButton("Seguir", on_click=go_to_page4))
        page.update()

    def go_to_page4(e):
        page.controls.clear()
        page.add(ft.Text("Agora com o seu Cadastramento de Login concluído, coloque as seguintes informações"))
   
        page.add(
            ft.TextField(label="Seu peso"),
            ft.TextField(label="Sua Altura"),
        )
   
        dropdown = ft.Dropdown(
            label="Objetivos de Hidratação",
            options=[
               ft.dropdown.Option("Manter-se hidratado"),
               ft.dropdown.Option("Perder peso"),
               ft.dropdown.Option("Melhorar saúde"),
            ]
        )
        page.add(dropdown)
 
        row_buttons = ft.Row(
            controls=[
                ft.FilledButton("Refazer", on_click=go_to_page2),
                ft.ElevatedButton("Enviar", on_click=go_to_page3),
            ]
        )
        page.add(row_buttons)
        page.update()

    # Inicia o aplicativo na primeira página
    go_to_page1(None)

ft.app(target=main)