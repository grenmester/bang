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
    direction = 1,
    speed = 150,
    jump_height = -5,
    gravity = 9.8,
    isGrounded = false,
    bullet = {
        w = 8,
        h = 8,
        direction = 1,
        speed = 450,
        exists = false
    }
}

local blocks = {}

local function drawBox(box, r, g, b)
  love.graphics.setColor(r, g, b, 100)
  love.graphics.rectangle("fill", box.x, box.y, box.w, box.h)
end

--------------------------------------------------
-- Bullets
--------------------------------------------------

local function fireBullet()
    player.bullet["x"] = player.x + player.direction * 48
    player.bullet["y"] = player.y + 16 - 4
    player.bullet.direction = player.bullet.direction or player.direction
    player.bullet.exists = true
    world:add(player.bullet, player.bullet.x, player.bullet.y, player.bullet.w, player.bullet.h)
end

local function updateBullet(dt)
    player.bullet.dx = player.bullet.speed * player.bullet.direction * dt
    player.bullet.x, player.bullet.y, cols, len = world:move(player.bullet, (player.bullet.x + player.bullet.dx) % canvas.width, player.bullet.y)
end

local function drawBullet()
    -- replace with tiles later
    drawBox(player.bullet, 0, 255, 255)
end

--------------------------------------------------
-- Players
--------------------------------------------------

local function playerCollision(player,collision)
  if (player.x + player.dx) > canvas.width or (player.x + player.dx) < 0 then
    oob = 'out of bounds'
  else
    oob = ''
  end
  print(string.format('Player collided at (%d,%d) with %s %s', player.x + player.dx, player.y + player.dy, collision.name, oob))
  print(string.format('Player y = %d, dy = %d',player.y,player.dy))
  -- update later to check collisions between different kinds of objects
  -- always collide with the ground
  if collision.name == 'ground' then
    return 'slide'
  elseif collision.name == 'platform1' then
    -- if the player is off the screen, ignore platform collisions
    if (player.x + player.dx) > canvas.width or (player.x + player.dx) < 0 then
      return false
    -- only collide if you're above the platform
    elseif player.dy < 0 then
      return false
    else
      return 'slide'
    end
  -- return slide by default
  else
    return 'slide'
  end
end

local function updatePlayer(dt)
    -- debug
    if love.keyboard.isDown('d') then
        print(string.format("player.dx,player.dy = (%d,%d)",player.dx,player.dy))
        if player.isGrounded then
            print("player.isGrounded: true")
        else
            print("player.isGrounded: false")
        end
    end

    -- fires bullet
    if love.keyboard.isDown('s') and not player.bullet.exists then
        fireBullet()
    end

    -- x direction movement
    if love.keyboard.isDown('right') then
        player.dx = player.speed * dt
        player.direction = 1
    elseif love.keyboard.isDown('left') then
        player.dx = -player.speed * dt
        player.direction = -1
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
        --try to move (test for collision)
        player.x, player.y, cols, len = world:move(player, (player.x + player.dx), (player.y + player.dy),playerCollision)
        -- wrap the player around if the player went offscreen
        player.x = player.x % canvas.width
        world:update(player, player.x,player.y)
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

--------------------------------------------------
-- Blocks
--------------------------------------------------

local function addBlock(x, y, w, h, name)
    local block = {x = x, y = y, w = w, h = h, name = name}
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
    addBlock(-20, canvas.height * 0.75, canvas.width + 40, canvas.height * 0.25, 'ground')
    addBlock(128, canvas.height * 0.65, 128, 8, 'platform1')
end

function love.update(dt)
    updatePlayer(dt)
    if player.bullet.exists then
        updateBullet(dt)
    end
end

function love.draw()
    drawBlocks()
    drawPlayer()
    if player.bullet.exists then
        drawBullet()
    end
end
