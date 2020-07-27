# -*- coding: utf8 -*-
import recobj


#########
#
# Определение языка по тексту
#
#########


jp_text = '昨日、私は猫を見て、森の中にたくさんのキノコがあります！ 太陽は明るく輝いている。'

sp_text = '''
En el trabajo, los personajes se encuentran en una situación difícil en la vida. 
El jefe de familia se quedó sin trabajo, sus hijos están enfermos y lo peor es que su hija menor murió. 
El padre de la familia tiene un pensamiento.'''

ru_text = '''
Жители Казани гордятся своими известными и прославленными земляками: Николаем Лобачевским и 
Федором Шаляпиным, Гавриилом Державиным и Фешиным. 
Источник: Сочинение на тему г. Казань - мой любимый город, https://ya.ru'''

ru_translit = '''
Zhiteli Kazani gordyatsa svoimi izvestnymi i proslavlennymi zemlyakami: Nikolaem Lobachevskim i 
Fedorom Shalyapinym, Gavriilom Derzhavinym i Feshinym. 
Istochnik: Sochineniye na temu g. Kazan - moj lyubimyj gorod, https://ya.ru'''


# Определяем язык по тексту
print(recobj.detect_language(jp_text))
# Можно задать точность (доля слов из частотного словаря в тексте, по-умолчанию 0.2)
print(recobj.detect_language(sp_text, accuracy=0.2))
# И словари для буквеных языков (base) и иероглифических (speshal)
test_dict = [
    (set(['Жители', 'Казани', 'гордятся', 'своими', 'известными', 'и', 'прославленными', 'земляками']), 'ru'),
    (set(['a', 'b', 'c']), '??')
]
print(recobj.detect_language(ru_text, base_dict=test_dict, spechal_dict=None))


# Если язык не опознан
print(recobj.detect_language(ru_translit))
if recobj.detect_language(ru_translit) == 'un':
    # Пытаемся интерпретировать его как транслитерацию
    # Можно задавать кастомные словари (подстановка будет произведена по лучшему совпадению)
    custom_dicts = [
        {
            'r': 'р', 'R': 'Р'
        },
        {  # Многобуквенные сокращения должны стоять реньше
            'shh': 'щ', 'Shh': 'Щ',
            'ya': 'я', 'Ya': 'Я',
            'r': 'р', 'R': 'Р'
        }
    ]
    print(recobj.translit_into_ru(ru_translit, translit_dicts=custom_dicts))
    # И точность (по-умолчанию 0.1)
    tmp = recobj.translit_into_ru(ru_translit, accuracy=0.1)
    # Если нашли транлитерацию с необходимым уровнем совпадения, то сохраняем результат
    if tmp is not None:
        ru_translit = tmp
print(ru_translit)

# Словари по-умолчанию:
# Частотные
recobj.base_dictionary
# Частотные для иероглифов
recobj.spechal_dictionary
# Транслитерации
recobj.default_translit_dictionaries


#########
#
# Выделение сущностей из текста
#
#########


# Необходимо совершить предобработку
tmp = recobj.preprocess(ru_translit)
# Интерпретацию граматики
tmp = recobj.interpretate(tmp)
# И пост-обработку
print(recobj.postprocess(tmp))

# Или все сразу
facts = recobj.parse(ru_text)
print(facts)


#########
#
# Обработка фактов
#
#########


# Определение тематики сайта
# Подгружаем базу
handler = recobj.UrlHandler()
# Ищем сайт в базе
print(handler.find(facts['url_fact'][0]['text']))


# Нормализация слова
# Подгружаем базу
norm = recobj.Normalizer()
# Время от времени следует обновлять словари pymorphy2
# Нормализуем
norm_name = norm.norm(facts['fio_fact'][0]['name'])
norm_surname = norm.norm(facts['fio_fact'][0]['surname'])
print(norm_name, norm_surname)
# Также нормальную форму можно достать из факта непосредственно
print(facts['fio_fact'][0]['normal_name'], facts['fio_fact'][0]['normal_surname'])
print(facts['geo_fact'][0]['normal'])


# Определение данных по ФИО
# Подгружаем базу
ident = recobj.Identifer()
# Ищем в базе
print(ident.detect(fio=facts['fio_fact'][0]['normal_name'] + ' ' + facts['fio_fact'][0]['normal_surname']))
# Или так
print(ident.detect(name=norm_name, surname=norm_surname, middle_name=None))
# Можно не только на русском
print(ident.detect(fio='Trevisan Mazzanti'))
# Если национальность имени и фамилии отличается, то сначала идет национальность по имени, а потом по фамилии
print(ident.detect(name='АБУ АЛ ХАЫР', surname='طاهرنژاد'))