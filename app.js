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
let commandSet = new Set(['jump', 'shoot', 'turn', 'drop'])
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

let loveServer = net.createServer(function(socket) {
    loveSocket = socket;
    loveSocket.on("connect", function () {
        // not appearing
        console.log("Connected to LOVE2D");
    });

        //bang, zap, boom, jump

    loveSocket.on("data", function (d) {
        d = d.toString()
        console.log(d)
        let split = d.split(" ")
        loveSocket.write('hi to python from node')
        loveSocket.pipe(loveSocket)
        if(split[0] == "end") {
            console.log("exit");
            loveSocket.end();
            server.close();
        }
        else if (split[0] == 'ammo'){
            let id = split[1]
            let ammoLeft = split[2]
            // TODO: identify player numbers
            playerToSocket[id].emit('ammo', {ammoLeft: ammoLeft})
        }
        else if (split[0] == "health"){
            let id = split[1]
            let healthLeft = split[2]
            // TODO: identify player numbers
            playerToSocket[id].emit('health', {healthLeft: healthLeft})
        } else if (split[0] == "color"){
            let id = split[1]
            let color = split[2]
            playerToSocket[id].emit('color', {color: color})
        }

    });
});
loveServer.listen(5000, 'localhost')

let socket2;
let server2 = require('http').createServer(app);
let io2 = require('socket.io')(server2)
io2.on('connection', function(socket){
  socket2 = socket
  socket.on('color', function(data){
    console.log(data)
  })
  socket.on('health', function(data){
    playerToSocket[data['id']].emit('health', {'healthLeft': data['health']})
  })
  socket.on('ammo', function(data){
    playerToSocket[data['id'].emit('ammo,', {'ammo': data['ammo']})]
  })
  socket.on("connected", function(data){
    console.log(data["data"])
  })
})
server2.listen('5001', function(){
  console.log('server 2 listening on port 5001')
})

//node is a server side app, so we need to now create a server using our app
let server = require('http').createServer(app);
let io = require('socket.io')(server);

//set our app listen on the port we specify
server.listen(app.get('port'), function(){
    //app.get('name') just gets name-value pair
    console.log('Project XXX working on port: ' + app.get('port'));
})


io.on('connection', function (socket) {
  numPlayers++;
  console.log(Object.keys(playerToSocket))
  socket2.emit("add-player", {'id': numPlayers})
  playerToSocket[numPlayers] = socket;
  socketToPlayer[socket] = numPlayers;
  //TODO: get all players to join rooms
  //socket.join('playerRoom');

  socket.on('sent word', function(data){
    // TODO: still have to check if word is a command and send it to game engine
    let words = data['word'].split(' ')
    let id = socketToPlayer[socket]
    let commands = [];
    for(let i = 0; i<words.length; i++){
      if(commandSet.has(words[i])){
        commands.push(words[i])
      }
    }
    console.log("commands " + commands)
    if (commands.length > 0){
      socket2.emit("command", {'id':id, 'commands': commands})
    }

  })
});
