## Кэширование

1. Запуск Tarantool из Docker

docker run \
  --name mytarantool \
  -d -p 3301:3301 \
  -v .:/var/lib/tarantool \
  tarantool/tarantool:1

2. Подключиться к экземпляру через стандартный Unix-сокет к Tarantool-серверу, запущенному внутри контейнера, из-под пользователя admin.

docker exec -i -t mytarantool console

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

s:insert{1, 1, 'textpost1'}
s:insert{1, 1, 'textpost2'}

6. Запрос данных

s:select{3}


СТАРОЕ
 https://github.com/tarantool/tarantool/releases/tag/3.0.0-alpha2
   И https://github.com/tarantool/tt
   Или любую старую версию Тарантула

2. Запустить:
  - tarantool --name instance-001 --config config.yaml
  - tarantool --name instance-002 --config config.yaml

  Для старых версий:
  - Раскомментить строчки в example.lua
  - tarantool example.lua

3. Подключиться:
   - tt connect localhost:3301
   - В консоли: get_from_cache(...)

