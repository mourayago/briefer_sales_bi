from faker import Faker

fake = Faker('pt_BR')


def set_sellers(number_of_sellers) -> list:
    sellers = []
    for i in range(number_of_sellers):
        temp_dict = {}
        id = i + 1
        seller_name = fake.name()
        temp_dict = {'seller_id': id, 'seller_name': seller_name}
        sellers.append(temp_dict)
    return sellers


def get_state_sales():
    return fake.estado_nome()
