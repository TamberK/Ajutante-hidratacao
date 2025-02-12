import flet as ft
from abc import ABC, abstractmethod

# Classe Abstrata (Abstração)
class Tela(ABC):
    def __init__(self, titulo):
        self._titulo = titulo  # Encapsulamento: atributo protegido

    @abstractmethod
    def construir(self):
        pass  # Método abstrato que deve ser implementado pelas classes filhas

# Herança: Telas específicas herdam da classe Tela
class TelaInicial(Tela):
    def construir(self):
        return ft.Column(
            controls=[
                ft.Text(value=f"=== {self._titulo} ===", size=20, weight="bold"),
                ft.ElevatedButton(text="Registrar consumo de água", on_click=self.ir_para_registro),
                ft.ElevatedButton(text="Ver histórico de consumo", on_click=self.ir_para_historico),
                ft.ElevatedButton(text="Configurações", on_click=self.ir_para_configuracoes),
                ft.ElevatedButton(text="Sair", on_click=self.sair),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def ir_para_registro(self, e):
        e.page.go("/registro")

    def ir_para_historico(self, e):
        e.page.go("/historico")

    def ir_para_configuracoes(self, e):
        e.page.go("/configuracoes")

    def sair(self, e):
        e.page.window_close()

class TelaRegistro(Tela):
    def construir(self):
        return ft.Column(
            controls=[
                ft.Text(value=f"=== {self._titulo} ===", size=20, weight="bold"),
                ft.TextField(label="Quantidade de água (ml)", width=300),
                ft.ElevatedButton(text="Registrar", on_click=self.registrar_consumo),
                ft.ElevatedButton(text="Voltar", on_click=self.voltar),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def registrar_consumo(self, e):
        quantidade = e.control.page.controls[1].value  # Acessa o valor do TextField
        if quantidade.isdigit():
            e.control.page.client_storage.set("historico", int(quantidade))  # Simula o armazenamento
            e.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"{quantidade} ml registrados com sucesso!")))
            e.page.go("/")
        else:
            e.page.show_snack_bar(ft.SnackBar(content=ft.Text("Digite um valor válido!")))

    def voltar(self, e):
        e.page.go("/")

class TelaHistorico(Tela):
    def construir(self):
        historico =e.page.client_storage.get("historico") or []  # Recupera o histórico
        return ft.Column(
            controls=[
                ft.Text(value=f"=== {self._titulo} ===", size=20, weight="bold"),
                ft.ListView(controls=[ft.Text(f"{i + 1}. {consumo} ml") for i, consumo in enumerate(historico)]),
                ft.ElevatedButton(text="Voltar", on_click=self.voltar),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def voltar(self, e):
        e.page.go("/")

class TelaConfiguracoes(Tela):
    def construir(self):
        return ft.Column(
            controls=[
                ft.Text(value=f"=== {self._titulo} ===", size=20, weight="bold"),
                ft.TextField(label="Meta diária de água (ml)", width=300),
                ft.ElevatedButton(text="Salvar", on_click=self.salvar_meta),
                ft.ElevatedButton(text="Voltar", on_click=self.voltar),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def salvar_meta(self, e):
        meta = e.control.page.controls[1].value  # Acessa o valor do TextField
        if meta.isdigit():
            e.control.page.client_storage.set("meta", int(meta))  # Simula o armazenamento
            e.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Meta diária definida: {meta} ml")))
        else:
            e.page.show_snack_bar(ft.SnackBar(content=ft.Text("Digite um valor válido!")))

    def voltar(self, e):
        e.page.go("/")

# Função principal do Flet
def main(page: ft.Page):
    page.title = "App de Hidratação"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Rotas para as telas
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(ft.View(route="/", controls=[TelaInicial("Tela Inicial").construir()]))
        elif page.route == "/registro":
            page.views.append(ft.View(route="/registro", controls=[TelaRegistro("Registrar Consumo").construir()]))
        elif page.route == "/historico":
            page.views.append(ft.View(route="/historico", controls=[TelaHistorico("Histórico de Consumo").construir()]))
        elif page.route == "/configuracoes":
            page.views.append(ft.View(route="/configuracoes", controls=[TelaConfiguracoes("Configurações").construir()]))
        page.update()

    page.on_route_change = route_change
    page.go("/")

# Inicia o app
ft.app(target=main)