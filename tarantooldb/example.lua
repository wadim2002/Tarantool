-- box.cfg{} -- start tarantool

-- box.schema.user.grant('guest', 'super', nil, nil, {if_not_exists = true}) -- grant super to guest

box.schema.space.create('cache', {if_not_exists = true}) -- create space

box.space.cache:format({ -- set space format
    {name = 'key', type = 'string'},
    {name = 'value', type = 'any'},
    {name = 'created_at', type = 'number'},
})

box.space.cache:create_index('primary', {parts = {'key'}, if_not_exists = true}) -- create primary index

box.space.cache:create_index('ttl_index', {parts = {'created_at'}, if_not_exists = true}) -- create secondary index

local fiber = require'fiber' -- load fiber module

local CHECK_INTERVAL = 10 -- check interval
local TTL = 30 -- time to live


fiber.create(function()
    while true do
        fiber.sleep(CHECK_INTERVAL) -- sleep 10 seconds

        box.space.cache.index.ttl_index:pairs(fiber.time() - TTL, {iterator = "LE"})
            :each(function(tuple)
                box.space.cache:delete(tuple.key)
            end) -- select expired tuples
    end
end)

function get_from_cache(key)
    local tuple = box.space.cache:get(key) -- get tuple by key
    if tuple == nil then
        -- connect to postgres
        return box.space.cache:insert{key, math.random(), fiber.time()} -- insert new tuple
    end
    return tuple
end

-- require'console'.start() -- start console
