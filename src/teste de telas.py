import flet as ft

def main(page: ft.Page):
    page.title = "Ajudante da Hidratação"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def create_page1():
        return ft.View(
            "/",
            [
                ft.Text("Seja Bem-Vindo ao nosso Ajudante da hidratação", size=20),
                ft.Text("Realize seu cadastro para começar com sua jornada para se manter hidratado"),
                ft.ElevatedButton("Cadastramento de Login", on_click=lambda e: page.go("/cadastro")),
            ],
            padding=20,
            spacing=20,
        )

    def create_page2():
        dropdown = ft.Dropdown(
            label="Faixa de idade",
            options=[
                ft.dropdown.Option("8-12 anos"),
                ft.dropdown.Option("13-17 anos"),
                ft.dropdown.Option("18-24 anos"),
            ],
            width=200,
        )

        return ft.View(
            "/cadastro",
            [
                ft.Text("Cadastramento de Login", size=20),
                ft.TextField(label="Digite seu nome completo", width=300),
                ft.TextField(label="Digite seu e-mail", width=300),
                ft.TextField(label="Digite sua senha", password=True, width=300),
                dropdown,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Refazer", on_click=lambda e: page.go("/")),
                        ft.FilledButton("Concluído", on_click=lambda e: page.go("/parabens")),
                    ],
                    spacing=20,
                ),
            ],
            padding=20,
            spacing=20,
        )

    def create_page3():
        return ft.View(
            "/parabens",
            [
                ft.Text("PARABÉNS!!! Você é o nosso Mais Novo Membro", size=20),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/cadastro")),
                        ft.FilledButton("Seguir", on_click=lambda e: page.go("/informacoes")),
                    ],
                    spacing=20,
                ),
            ],
            padding=20,
            spacing=20,
        )

    def create_page4():
        dropdown = ft.Dropdown(
            label="Objetivos de Hidratação",
            options=[
                ft.dropdown.Option("Manter-se hidratado"),
                ft.dropdown.Option("Perder peso"),
                ft.dropdown.Option("Melhorar saúde"),
            ],
            width=200,
        )

        return ft.View(
            "/informacoes",
            [
                ft.Text("Agora com o seu Cadastramento de Login concluído, coloque as seguintes informações", size=20),
                ft.TextField(label="Seu peso", width=300),
                ft.TextField(label="Sua Altura", width=300),
                dropdown,
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Refazer", on_click=lambda e: page.go("/cadastro")),
                        ft.FilledButton("Enviar", on_click=lambda e: page.go("/parabens")),
                    ],
                    spacing=20,
                ),
            ],
            padding=20,
            spacing=20,
        )

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            page.views.append(create_page1())
        elif page.route == "/cadastro":
            page.views.append(create_page2())
        elif page.route == "/parabens":
            page.views.append(create_page3())
        elif page.route == "/informacoes":
            page.views.append(create_page4())
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main)