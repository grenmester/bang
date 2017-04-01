platform = {}
player = {}  -- Add this below the platform variable

function love.load()
    -- This is the height and the width of the platform.
	platform.width = love.graphics.getWidth()    -- This makes the platform as wide as the whole game window.
	platform.height = love.graphics.getHeight()  -- This makes the platform as tall as the whole game window.

    -- This is the coordinates where the platform will be rendered.
	platform.x = 0                               -- This starts drawing the platform at the left edge of the game window.
	platform.y = platform.height / 2             -- This starts drawing the platform at the very middle of the game window.

    -- This is the coordinates where the player character will be rendered.
	player.x = love.graphics.getWidth() / 2   -- This sets the player at the middle of the screen based on the width of the game window.
	player.y = love.graphics.getHeight() / 2  -- This sets the player at the middle of the screen based on the height of the game window.

    -- This calls the file named "purple.png" and puts it in the variable called player.img.
	player.img = love.graphics.newImage('assets/purple.png')

    player.speed = 200    -- This is the player's speed. This value can be change based on your liking.

	player.ground = player.y     -- This makes the character land on the plaform.

	player.y_velocity = 0        -- Whenever the character hasn't jumped yet, the Y-Axis velocity is always at 0.

	player.jump_height = -300    -- Whenever the character jumps, he can reach this height.
	player.gravity = -500
end

function love.update(dt)
	if love.keyboard.isDown('d') then
		-- This makes sure that the character doesn't go pass the game window's right edge.
		if player.x < (love.graphics.getWidth() - player.img:getWidth()) then
			player.x = player.x + (player.speed * dt)
		end
	elseif love.keyboard.isDown('a') then
		-- This makes sure that the character doesn't go pass the game window's left edge.
		if player.x > 0 then
			player.x = player.x - (player.speed * dt)
		end
	end

    -- This is in charge of player jumping.
	if love.keyboard.isDown('space') then                     -- Whenever the player presses or holds down the Spacebar:

        -- The game checks if the player is on the ground. Remember that when the player is on the ground, Y-Axis Velocity = 0.
		if player.y_velocity == 0 then
			player.y_velocity = player.jump_height    -- The player's Y-Axis Velocity is set to it's Jump Height.
		end
    end

    -- This is in charge of the jump physics.
    if player.y_velocity ~= 0 then                              -- The game checks if player has "jumped" and left the ground.
		player.y = player.y + player.y_velocity * dt                -- This makes the character ascend/jump.
		player.y_velocity = player.y_velocity - player.gravity * dt -- This applies the gravity to the character.
	end

    -- This is in charge of collision, making sure that the character lands on the ground.
    if player.y > player.ground then    -- The game checks if the player has jumped.
		player.y_velocity = 0       -- The Y-Axis Velocity is set back to 0 meaning the character is on the ground again.
    	player.y = player.ground    -- The Y-Axis Velocity is set back to 0 meaning the character is on the ground again.
    end
end

function love.draw()
	love.graphics.setColor(255, 255, 255)        -- This sets the platform color to white. (The parameters are in RGB Color format).

    -- The platform will now be drawn as a white rectangle while taking in the variables we declared above.
	love.graphics.rectangle('fill', platform.x, platform.y, platform.width, platform.height)
    -- Add this below the love.graphics.rectangle line.

    -- This draws the player.
	love.graphics.draw(player.img, player.x, player.y, 0, 1, 1, 0, 16)
end
