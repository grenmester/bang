local bump = require 'lib.bump'

local world = bump.newWorld(32)

local canvas = {
    width = love.graphics.getWidth(),
    height = love.graphics.getHeight(),
}

local player = {
    x = 375,
    y = 250,
    w = 32,
    h = 32,
    dx = 0,
    dy = 0,
    speed = 150,
    jump_height = -5,
    gravity = 9.8,
    isGrounded = false
}

local blocks = {}

local function drawBox(box, r,g,b)
  love.graphics.setColor(r, g, b, 100)
  love.graphics.rectangle("fill", box.x, box.y, box.w, box.h)
end

local function updatePlayer(dt)
    -- debug
    if love.keyboard.isDown('d') then
        print("player.dx: "..player.dx)
        print("player.dy: "..player.dy)
        if player.isGrounded then
            print("player.isGrounded: true")
        else
            print("player.isGrounded: false")
        end
    end

    -- x direction movement
    if love.keyboard.isDown('right') then
        player.dx = player.speed * dt
    elseif love.keyboard.isDown('left') then
        player.dx = -player.speed * dt
    elseif not love.keyboard.isDown('left') and not love.keyboard.isDown('right') then
        player.dx = 0
    end

    -- y direction movement
    if love.keyboard.isDown('up') and player.isGrounded then
        player.isGrounded = false
        player.dy = player.jump_height
    end

    -- gravity
    if player.isGrounded then
        player.dy = 0
    else
        player.dy = player.dy + (player.gravity * dt)
    end

    -- movement
    if player.dx ~= 0 or player.dy ~= 0 then
        local cols
        player.x, player.y, cols, len = world:move(player, (player.x + player.dx) % canvas.width, (player.y + player.dy) % canvas.width)
        if len <= 0 then
            player.isGrounded = false
        else
            for i = 1, len do
                local col = cols[i]
                if col.normal.x == 0 and col.normal.y == -1 then
                    player.isGrounded = true
                end
            end
        end
    end
end

local function drawPlayer()
    -- replace with tiles later
    drawBox(player, 0, 255, 0)
end

local function addBlock(x, y, w, h)
    local block = {x = x, y = y, w = w, h = h}
    blocks[#blocks+1] = block
    world:add(block, x, y, w, h)
end

local function drawBlocks()
    for _,block in ipairs(blocks) do
        -- replace with tiles later
        drawBox(block, 255, 0, 0)
    end
end

function love.load()
    world:add(player, player.x, player.y, player.w, player.h)
    addBlock(0, canvas.height * 0.75, canvas.width, canvas.height * 0.25)
    addBlock(128, canvas.height * 0.65, 128, 8)
end

function love.update(dt)
    updatePlayer(dt)
end

function love.draw()
    drawBlocks()
    drawPlayer()
end
