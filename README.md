## Кэширование

1. Запуск Tarantool из Docker

docker-compose up

2. Подключиться к экземпляру через стандартный Unix-сокет к Tarantool-серверу, запущенному внутри контейнера, из-под пользователя admin.

docker exec -i -t <ID-контейнера> console

 3. Создание БД

 s = box.schema.space.create('posts')
 
 3. Создание полей в БД

 s:format({
{name = 'id', type = 'unsigned'},
{name = 'userid', type = 'unsigned'},
{name = 'text', type = 'string'},
})
 
 4. Создание индекса

s:create_index('primary', {
type = 'hash',
parts = {'userid'}
})
 
 5. Вставка данных

Копирование данных из Postrges в Tarantool реализована через функцию 
http://localhost:8000/post/copy

6. Запрос данных

box.space['posts']:select()