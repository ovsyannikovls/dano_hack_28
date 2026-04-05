import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.patches import Patch

df = pd.read_excel('/mnt/user-data/uploads/salary_gender_region.xlsx')

region_names = {
    1: 'Республика Адыгея', 2: 'Республика Башкортостан', 3: 'Республика Бурятия',
    4: 'Республика Алтай', 5: 'Республика Дагестан', 6: 'Республика Ингушетия',
    7: 'Кабардино-Балкария', 8: 'Республика Калмыкия', 9: 'Карачаево-Черкессия',
    10: 'Республика Карелия', 11: 'Республика Коми', 12: 'Республика Марий Эл',
    13: 'Республика Мордовия', 14: 'Республика Саха (Якутия)', 15: 'Республика Северная Осетия',
    16: 'Республика Татарстан', 17: 'Республика Тыва', 18: 'Республика Удмуртия',
    19: 'Республика Хакасия', 20: 'Чеченская Республика', 21: 'Чувашская Республика',
    22: 'Алтайский край', 23: 'Краснодарский край', 24: 'Красноярский край',
    25: 'Приморский край', 26: 'Ставропольский край', 27: 'Хабаровский край',
    28: 'Амурская область', 29: 'Архангельская область', 30: 'Астраханская область',
    31: 'Белгородская область', 32: 'Брянская область', 33: 'Владимирская область',
    34: 'Волгоградская область', 35: 'Вологодская область', 36: 'Воронежская область',
    37: 'Ивановская область', 38: 'Иркутская область', 39: 'Калининградская область',
    40: 'Калужская область', 41: 'Камчатский край', 42: 'Кемеровская область',
    43: 'Кировская область', 44: 'Костромская область', 45: 'Курганская область',
    46: 'Курская область', 47: 'Ленинградская область', 48: 'Липецкая область',
    49: 'Магаданская область', 50: 'Московская область', 51: 'Мурманская область',
    52: 'Нижегородская область', 53: 'Новгородская область', 54: 'Новосибирская область',
    55: 'Омская область', 56: 'Оренбургская область', 57: 'Орловская область',
    58: 'Пензенская область', 59: 'Пермский край', 60: 'Псковская область',
    61: 'Ростовская область', 62: 'Рязанская область', 63: 'Самарская область',
    64: 'Саратовская область', 65: 'Сахалинская область', 66: 'Свердловская область',
    67: 'Смоленская область', 68: 'Тамбовская область', 69: 'Тверская область',
    70: 'Томская область', 71: 'Тульская область', 72: 'Тюменская область',
    73: 'Ульяновская область', 74: 'Челябинская область', 75: 'Забайкальский край',
    76: 'Ярославская область', 77: 'Москва', 78: 'Санкт-Петербург',
    79: 'Еврейская АО', 83: 'Ненецкий АО', 86: 'ХМАО-Югра',
    87: 'Чукотский АО', 89: 'Ямало-Ненецкий АО', 91: 'Республика Крым', 92: 'Севастополь',
}

pivot = df.pivot(index='region_code', columns='gender', values='mean_salary').dropna()
pivot['label'] = pivot.index.map(lambda x: region_names.get(x, f'Регион {x}'))
pivot['gap'] = pivot['Мужской'] - pivot['Женский']
pivot = pivot.sort_values('gap', ascending=True).reset_index()

n = len(pivot)
y = np.arange(n)
height = 0.38

mpl.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.left': False,
    'xtick.labelsize': 8.5,
    'ytick.labelsize': 8.5,
})

fig, ax = plt.subplots(figsize=(13, n * 0.28 + 2))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

COLOR_F = '#c75040'
COLOR_M = '#3266ad'

bars_f = ax.barh(y - height/2, pivot['Женский'], height=height, color=COLOR_F, zorder=3, label='Женщины')
bars_m = ax.barh(y + height/2, pivot['Мужской'], height=height, color=COLOR_M, zorder=3, label='Мужчины')

ax.set_yticks(y)
ax.set_yticklabels(pivot['label'], fontsize=8)
ax.xaxis.grid(True, color='#eeeeee', linewidth=0.8, zorder=0)
ax.yaxis.grid(False)
ax.axvline(0, color='#aaaaaa', linewidth=0.8, zorder=4)

ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}К ₽'))

ax.set_xlabel('Средняя зарплата, руб.', fontsize=10, labelpad=10, color='#444444')
ax.set_title('Средняя зарплата мужчин и женщин по регионам России\n'
             'Регионы отсортированы по величине гендерного разрыва (меньший → больший)',
             fontsize=12, fontweight='normal', pad=16, color='#222222')

legend_elements = [
    Patch(facecolor=COLOR_F, label='Женщины (средняя зп)'),
    Patch(facecolor=COLOR_M, label='Мужчины (средняя зп)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
          frameon=False, labelcolor='#444444')

ax.tick_params(axis='y', length=0, pad=6)
ax.tick_params(axis='x', colors='#888888')
ax.spines['bottom'].set_color('#cccccc')

plt.tight_layout()
plt.savefig('chart_salary_gender_region.png', dpi=150, bbox_inches='tight')
print("Saved.")