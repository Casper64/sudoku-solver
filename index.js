const { spawn } = require('child_process');
const express = require("express");
const path = require('path');
const multer = require("multer")
const sharp = require("sharp")
const bodyParser = require("body-parser");
let PythonShellLibrary = require('python-shell');
let {PythonShell} = PythonShellLibrary;

const app = express();

app.use(
    express.static(__dirname + '/assets'),
);
app.use(bodyParser.json());

app.use(bodyParser.urlencoded({ extended: false }));


const pythonScanner = (img) => {
    let shell = new PythonShell('./sudoku_scanner.py', {
        // The '-u' tells Python to flush every time
        pythonOptions: ['-u'],
        args: [img]
    });
    shell.on('message', function(message){
        sendEventsToAll(message)
    })
};

const pythonGenerator = () => {
    let shell = new PythonShell('./sudoku_generator.py', {
        // The '-u' tells Python to flush every time
        pythonOptions: ['-u'],
    });
    shell.on('message', function(message){
        console.log(message)
        sendEventsToAll(message)
    })
};

const pythonSolver = (grid) => {
    let shell = new PythonShell('./sudoku_solver.py', {
        pythonOptions: ['-u'],
        args: [JSON.stringify(grid)]
    });
    shell.on('message', function(message){
        sendEventsToAll(message)
    })
    shell.on('error', (message) => {
        sendEventsToAll(message)
    })
    shell.on('pythonError', (message) => {
        sendEventsToAll(message)
    })
}

let clients = [];

function eventsHandler(request, response, next) {
    const headers = {
      'Content-Type': 'text/event-stream',
      'Connection': 'keep-alive',
      'Cache-Control': 'no-cache'
    };
    response.writeHead(200, headers);
  
    const clientId = Date.now();
  
    const newClient = {
      id: clientId,
      response
    };
  
    clients.push(newClient);
  
    request.on('close', () => {
      console.log(`${clientId} Connection closed`);
      clients = clients.filter(client => client.id !== clientId);
    });
}
app.get('/events', eventsHandler);

function sendEventsToAll(string) {
    clients.forEach(client => client.response.write(`data: ${string}\n\n`))
}
  

const upload = multer().single("image")
app.post("/script", (req, res) => {
    upload(req, res, async (error) => {
        const image = await sharp(req.file.buffer)
            .jpeg({
                quality: 40
            })
            .toFile("./images/image.jpeg")
            .catch( err => { console.log('error: ', err) })

        pythonScanner("./images/image.jpeg");
    })
});

app.post("/solve", (req, res) => {
    pythonSolver(req.body);
})

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "/index.html"))
})

app.get("/generate", (req, res) => {
    pythonGenerator();
    res.send("Well Hello there")
})


app.listen(5000, () => console.log("App is running port 5000"));