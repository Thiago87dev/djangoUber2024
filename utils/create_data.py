import os
import django
import sys
import faker
from pathlib import Path
import random
from django.conf import settings
from datetime import timedelta, datetime

DJANGO_BASE_DIR = Path(__file__).parent.parent

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
settings.USE_TZ =False

# Configurando o Django
django.setup()

from uber.models import ResultUber
from django.contrib.auth.models import User

# Criando uma instância do Faker
fake = faker.Faker('pt-br')

# Função para gerar um tempo aleatório entre 6 e 10 horas
def random_time(start_hour, end_hour):
    delta = timedelta(hours=random.randint(start_hour, end_hour),minutes=random.randint(0, 59))
    random_time = (datetime.min + delta).time()
    return random_time

# Função para gerar dados aleatórios
def create_fake_data(num_records, username):
    user = User.objects.get(username=username)
    for _ in range(num_records):
        data_criacao = fake.date_time_this_year()
        preco_comb = round(random.uniform(5.0, 5.9),2)
        desc_comb = round(random.uniform(0, 10), 2)
        km_por_litro = round(random.uniform(12.0, 14.0), 2)
        km_rodado = round(random.uniform(100, 200), 2)
        horas_trab = random_time(7, 10)
        faturamento = round(random.uniform(100, 300), 2)
        
        # Realizando cálculos
        comb_com_desc = round(preco_comb - desc_comb / 100 * preco_comb, 2)
        gasto_por_km = round(comb_com_desc / km_por_litro, 2)
        gasto_com_comb = round(km_rodado * gasto_por_km, 2)
        lucro = round(faturamento - gasto_com_comb, 2)
        ganho_hora = round(lucro / ((horas_trab.hour * 60 + horas_trab.minute) / 60), 2)
        ganho_por_km = round(lucro / km_rodado, 2)
        
        # Criando o registro no banco de dados
        ResultUber.objects.create(
            data_criacao=data_criacao,
            gasto_por_km=gasto_por_km,
            gasto_com_comb=gasto_com_comb,
            comb_com_desc=comb_com_desc,
            lucro=lucro,
            ganho_por_km=ganho_por_km,
            km_rodado=km_rodado,
            preco_comb=preco_comb,
            horas_trab=horas_trab,
            faturamento=faturamento,
            km_por_litro=km_por_litro,
            ganho_hora=ganho_hora,
            desc_comb=desc_comb,
            owner=user
        )

# Gerar registros falsos
create_fake_data(5,'mariazinha')