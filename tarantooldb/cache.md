## Кэширование

1. Установить https://github.com/tarantool/tarantool/releases/tag/3.0.0-alpha2
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

