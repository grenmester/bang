canvas = {}
platforms = {}
player = {}

function love.load()
    -- canvas settings
    canvas.width = love.graphics.getWidth()
    canvas.height = love.graphics.getHeight()
    canvas.x = 0
    canvas.y = canvas.height * 0.75

    -- player settings
	player.x = love.graphics.getWidth() * 0.5   -- This sets the player at the middle of the screen based on the width of the game window.
	player.y = love.graphics.getHeight() * 0.75  -- This sets the player at the middle of the screen based on the height of the game window.
    player.img = love.graphics.newImage('assets/purple.png')

    player.speed = 200
    player.y_velocity = 0
    player.jump_height = -300
    player.gravity = -500

    platforms.ground = canvas.height * 0.75
end

function love.update(dt)
    -- movement
	if love.keyboard.isDown('d') and not love.keyboard.isDown('a') then
		player.x = (player.x + (player.speed * dt)) % canvas.width
    elseif love.keyboard.isDown('a') and not love.keyboard.isDown('d') then
	    player.x = (player.x - (player.speed * dt)) % canvas.width
	end

	if love.keyboard.isDown('w') then
		if player.y_velocity == 0 then  -- if the player is on the ground
			player.y_velocity = player.jump_height
        end
    end

    -- gravity
    if player.y_velocity ~= 0 then
		player.y = player.y + player.y_velocity * dt
        player.y_velocity = player.y_velocity - player.gravity * dt
	end

    -- ground collision detection
    if player.y > platforms.ground then
		player.y_velocity = 0
    	player.y = platforms.ground
    end
end

function love.draw()
	love.graphics.setColor(255, 255, 255)
	love.graphics.rectangle('fill', canvas.x, canvas.y, canvas.width, canvas.height)
	love.graphics.draw(player.img, player.x, player.y, 0, 1, 1, 0, 16)
end
