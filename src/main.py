import flet as ft
import json
import os
from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, username, password):
        self._name = name
        self._username = username
        self._password = password

    @property
    def name(self):
        return self._name

    @property
    def username(self):
        return self._username

    @abstractmethod
    def get_role(self):
        pass

    def to_dict(self):
        return {
            "name": self._name,
            "username": self._username,
            "password": self._password,
            "role": self.get_role()
        }

class Customer(Person):
    def __init__(self, name, username, password):
        super().__init__(name, username, password)
        self._purchases = []

    def add_purchase(self, purchase):
        self._purchases.append(purchase)

    def get_role(self):
        return "customer"

class Employee(Person):
    def __init__(self, name, username, password, employee_id):
        super().__init__(name, username, password)
        self._employee_id = employee_id

    @property
    def employee_id(self):
        return self._employee_id

    def get_role(self):
        return "employee"

class UserManager:
    def __init__(self, filename):
        self._filename = filename
        self._users = self._load_users()

    def _load_users(self):
        if os.path.exists(self._filename):
            with open(self._filename, 'r') as file:
                data = json.load(file)
                return [self._create_user_object(user) for user in data]
        return []

    def _create_user_object(self, user_data):
        if user_data['role'] == 'customer':
            return Customer(user_data['name'], user_data['username'], user_data['password'])
        elif user_data['role'] == 'employee':
            return Employee(user_data['name'], user_data['username'], user_data['password'], user_data.get('employee_id'))
        else:
            raise ValueError(f"Unknown user role: {user_data['role']}")

    def add_user(self, user):
        self._users.append(user)
        self._save_users()

    def get_user(self, username):
        return next((user for user in self._users if user.username == username), None)

    def authenticate(self, username, password):
        user = self.get_user(username)
        return user if user and user._password == password else None

    def _save_users(self):
        with open(self._filename, 'w') as file:
            json.dump([user.to_dict() for user in self._users], file, indent=2)

def main(page: ft.Page):
    page.title = "Sistema de Loja"
    page.theme_mode = "DARK"
    page.padding = 20

    # Arquivo para armazenar usuários
    USERS_FILE = "users.json"
    # Arquivo para armazenar produtos
    PRODUCTS_FILE = "products.json"
     
    user_manager = UserManager(USERS_FILE)

    def load_data(file_name):
        if os.path.exists(file_name):
            with open(file_name, "r") as file:
                return json.load(file)
        return []
    
    def save_data(file_name, data):
        with open(file_name, "w") as file:
            json.dump(data, file, indent=2)

    products = load_data(PRODUCTS_FILE)

    def login(e):
        username = username_input.value
        password = password_input.value
        user = user_manager.authenticate(username, password)
        if user:
            page.clean()
            show_main_screen(user)
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Usuário ou senha inválidos"))
            page.snack_bar.open = True
            page.update()

    def register(e):
        name = name_input.value
        username = username_input.value
        password = password_input.value
        if name and username and password:
            new_user = Customer(name, username, password)
            user_manager.add_user(new_user)
            page.snack_bar = ft.SnackBar(content=ft.Text("Usuário registrado com sucesso"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Preencha todos os campos"))
            page.snack_bar.open = True
            page.update()

    name_input = ft.TextField(label="Nome", width=300)
    username_input = ft.TextField(label="Usuário", width=300)
    password_input = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)

    login_view = ft.Column(
        controls=[
            ft.Text("Login", size=32, weight="bold"),
            name_input,
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

    def update_product_list():
        product_list.controls.clear()
        for product in products:
            product_list.controls.append(ft.Text(f"{product['name']} - R$ {product['price']:.2f}"))
        page.update()

    def show_main_screen(user):
        update_product_list()
        main_view = ft.Column(
            controls=[
                ft.Text(f"Bem-vindo, {user.name}!", size=32, weight="bold"),
                ft.Text("Cadastro de Produtos", size=24, weight="bold"),
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