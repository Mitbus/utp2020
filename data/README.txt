Для обновления баз данных необходимо:
1. Добавить новые url адреса в url_bd.xlsx
2. Добавить новые значение имен и фамилий в names_db.xlsx
3. Произвести филтрацию ячеек по фамилии (имени) и url адресу, чтобы остались только уникальные значения
4. Убрать старые базы данных url.db и names.db из текущей дикертории
5. Создать новые .db файлы при помощи скрипта create_db.py (Интерфейс запуска: python3 create_db.py)
6. Дождитесь конца выполнения. Это может занять некоторое время