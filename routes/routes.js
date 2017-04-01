'use strict'
//Since we are using function constructors to set the properties of the module.exports object, the function constructor itself is also getting invoked (from javascript course!), therefore this setup is synonymous to just running the following code in the app.js file 
module.exports = function(express, app){
    
    //Configure some routes 
    let router = express.Router();

    //app.get(path, callback) routes HTTP GET requests to the specified path with the specified callback function 
    router.get('/', function(req, res){
        //terminate the connection with the server with a res.render method 
        res.render('index', {});
    })

    app.use('/', router);
    
}
