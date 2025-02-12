import flet as ft
import json, os

def main(page: ft.Page):
    page.title = "Sistema de Loja"
    page.theme_mode = "DARK"
    page.padding = 20

    # Arquivo para armazenar usuários
    USERS_FILE = "users.json"
    # Arquivo para armazenar produtos
    PRODUCTS_FILE = "products.json"
     
    #carregando informações
    def load_data(file_name):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                return json.load(file)
        return []
    
    #Salvar informações
    def save_data(file_name, data):
        with open(file_name, "w") as file:
            json.dump(data, file, indent=2)

    users = load_data(USERS_FILE)
    products = load_data(PRODUCTS_FILE)

    #tela de login
    def login(e):
        username = username_input.value
        password = password_input.value
        for user in users:
            if user["username"] == username and user["password"] == password:
                page.clean()
                show_main_screen()
                return
        page.snack_bar = ft.SnackBar(content=ft.Text("Usuário ou senha inválidos"))
        page.snack_bar.open = True
        page.update()

    #registros de usuarios
    def register(e):
        username = username_input.value
        password = password_input.value
        if username and password:
            users.append({"username": username, "password": password})
            save_data(USERS_FILE, users)
            page.snack_bar = ft.SnackBar(content=ft.Text("Usuário registrado com sucesso"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Preencha todos os campos"))
            page.snack_bar.open = True
            page.update()

    #parametros dos botões
    username_input = ft.TextField(label="Usuário", width=300)
    password_input = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)

#tela de login apresentada
    login_view = ft.Column(
        controls=[
            ft.Text("Login", size=32, weight="bold"),
            username_input,
            password_input,
            ft.Row(
                controls=[
                    ft.ElevatedButton("Entrar", on_click=login),
                    ft.ElevatedButton("Registrar", on_click=register),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

#tela de registro de produto

    def add_product(e):
        name = product_name.value
        price = product_price.value
        if name and price:
            try:
                price = float(price)
                products.append({"name": name, "price": price})
                save_data(PRODUCTS_FILE, products)
                product_name.value = ""
                product_price.value = ""
                update_product_list()
                page.snack_bar = ft.SnackBar(content=ft.Text("Produto adicionado com sucesso"))
                page.snack_bar.open = True
                page.update()
            except ValueError:
                page.snack_bar = ft.SnackBar(content=ft.Text("Preço inválido"))
                page.snack_bar.open = True
                page.update()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Preencha todos os campos"))
            page.snack_bar.open = True
            page.update()

    product_name = ft.TextField(label="Nome do Produto", width=300)
    product_price = ft.TextField(label="Preço", width=300)
    product_list = ft.Column(scroll=ft.ScrollMode.AUTO, height=400)

#atualizar lista de produto
    def update_product_list():
        product_list.controls.clear()
        for product in products:
            product_list.controls.append(ft.Text(f"{product['name']} - R$ {product['price']:.2f}"))
        page.update()

    def show_main_screen():
        update_product_list()
        main_view = ft.Column(
            controls=[
                ft.Text("Cadastro de Produtos", size=32, weight="bold"),
                product_name,
                product_price,
                ft.ElevatedButton("Adicionar Produto", on_click=add_product),
                ft.Text("Lista de Produtos", size=20, weight="bold"),
                product_list,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.add(main_view)

    page.add(login_view)

if __name__ == "__main__":
    ft.app(target=main)