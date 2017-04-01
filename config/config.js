//this one line of code means calling the require module on config.js will return the object created in either production.json or development.json file 
//When calling require on a json file, Node.js will parse the content to a particular JSON object and return it
module.exports = require('./' + (process.env.NODE_ENV || 'development') + '.json');