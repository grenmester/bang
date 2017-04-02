'use strict'
let express = require('express');
let path = require('path');
let config = require('./config/config.js');
let net = require('net');
let app = express();
let loveSocket;
let numPlayers = 0;
let playerToSocket = {};
let socketToPlayer = {};

//In this case we're running the app from Users/Documents/Programming/Node Starter, so that's the value of __dirname
//Now we tell the app to append /views to that path
app.set('views', path.join(__dirname, 'views'));

//hogan templating engine allows us to keep HTML files with extension .html
app.engine('html', require('hogan-express'));
app.set('view engine', 'html');

//app.use mounts the middleware function to that path
//app.use with no path specified will default to '/' and will get executed at every request
//Therefore, at every request, we want to serve the static files (images, CSS, JavaScript)
app.use(express.static(path.join(__dirname, 'public')));
//create our name-value pairs
app.set('port', process.env.PORT || 3000);
app.set('host', config.host);

//calling require on a file returns the module object generated by that file
//module = module.exports = {}
//In javascript, it is perfectly valid return a value, in this case - an object, but not initialize it
require('./routes/routes.js')(express, app);

//node is a server side app, so we need to now create a server using our app
let server = require('http').createServer(app);
let loveServer = net.createServer(function(socket) {
    loveSocket = socket;
    loveSocket.on("connect", function () {
        // not appearing
        console.log("Connected to LOVE2D");
    });

    loveSocket.on("data", function (d) {
        d = d.toString()
        if(d == "exit\0") {
            console.log("exit");
            loveSocket.end();
            server.close();
        }
        else if (d[0] == "3"){
            let ammoLeft = d.slice(1, d.length)
            playerToSocket[1].emit('ammo', {ammoLeft: ammoLeft})
        }

    });
});


let io = require('socket.io')(server);

//set our app listen on the port we specify
server.listen(app.get('port'), function(){
    //app.get('name') just gets name-value pair
    console.log('Project XXX working on port: ' + app.get('port'));
})

loveServer.listen(5000, 'localhost')

//bang, zap, boom, jump
io.on('connection', function (socket) {
  numPlayers++;
  playerToSocket[numPlayers] = socket;
  socketToPlayer[socket] = numPlayers;
  //TODO: get all players to join rooms
  socket.join('playerRoom');
  console.log('client socket connected')
  socket.on('sent word', function(data){
    // TODO: still have to check if word is a command
    console.log(data)
  })
});
