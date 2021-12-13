

function load() {
    const container = document.getElementById("grid");
    for (let i = 0; i < 9; i++) {
        let bigSquare = document.createElement("div");
        bigSquare.classList.add("big-square");
        bigSquare.id = "b"+i;
        container.insertAdjacentElement("beforeend", bigSquare);
        for (let j = 0; j < 9; j++) {
            let smallSquare = document.createElement("div");
            smallSquare.classList.add("small-square");
            smallSquare.id= `${Math.floor(j / 3) + Math.floor(i / 3) * 3}:${j % 3 + (i % 3 )* 3}`
            smallSquare.setAttribute("contenteditable", "true");
            bigSquare.insertAdjacentElement("beforeend", smallSquare);
        }
    }

    document.getElementById("img-upload").addEventListener("change", handleUpload);

    var eventSource = new EventSource('/events');
    eventSource.onmessage = handleScriptMessage;
}

let end = false;
let grid = Array(9).fill(Array(9).fill(0));
function handleScriptMessage(e) {
    let text = e.data;
    if (text.includes("/")) {
        let [current, total] = text.split("/");
        let progress = Math.ceil(Number(current) / Number(total)* 100);
        document.getElementById("progress").style.width = progress + "%"
    }
    else if (text.match("Array")) {
        document.getElementById("popup").style.display = "none";
        document.getElementById("backdrop").style.display = "none";
        end = true;
        grid = [];
    }
    else if (text.match("End")) {
        end = false;
        fillGrid();
        if (solving) {
            document.getElementById("success-text").style.display = "block";
            solving = false;
        }
    }
    else if (end) {
        let array = text.match(/\d/g);
        grid.push(array)
    }
    else if (text.match("FAIL")) {
        document.getElementById("error-text").style.display = "block";
    }
    else {
        console.log(text);
    }
}

function fillGrid() {
    grid.forEach((row, r) => {
        row.forEach((col, c) => {
            if (col == 0) {
                document.getElementById(`${r}:${c}`).innerHTML = "";
            }
            else {
                document.getElementById(`${r}:${c}`).innerHTML = col;
            }
        })
    })
}

let solving = false;
function solve() {
    solving = true;
    document.getElementById("error-text").style.display = "none";
    document.getElementById("success-text").style.display = "none";
    
    grid = [];
    for (let i = 0; i < 9; i++) {
        let row = [];
        for (let j = 0; j < 9; j++) {
            let value = document.getElementById(`${i}:${j}`).innerText;
            if (!value) {
                value = 0;
            }
            else {
                value = Number(value);
            }
            row.push(value)
        }
        grid.push(row)
    }
    let data = JSON.stringify(grid);
    var xhttp = new XMLHttpRequest(); // create new AJAX request

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { // sucess from server
            console.log('sent'+this.responseText+ xhttp.status);
        }else{ // errors occured
            console.log(xhttp.status );
        }
    }
    xhttp.open("POST", "solve", true)
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(data);
}

function handleUpload(event) {
    document.getElementById("error-text").style.display = "none";
    document.getElementById("success-text").style.display = "none";

    var xhttp = new XMLHttpRequest(); // create new AJAX request

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { // sucess from server
            console.log('sent'+this.responseText+ xhttp.status);
        } else{ // errors occured
            // console.log(xhttp.status );
        }
    }

    xhttp.open("POST", "script")
    var formData = new FormData()
    formData.append('image', document.getElementById('img-upload').files[0]) // since inputs allow multi files submission, therefore files are in array
    xhttp.send(formData)
    document.getElementById("popup").style.display = "grid";
    document.getElementById("backdrop").style.display = "block";
}

function clearGrid() {
    document.getElementById("error-text").style.display = "none";
    document.getElementById("success-text").style.display = "none";
    grid = Array(9).fill(Array(9).fill(0));
    fillGrid(); 
}

function generate() {
    clearGrid();
    var xhttp = new XMLHttpRequest(); // create new AJAX request

    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) { // sucess from server
            console.log('sent '+this.responseText+ " " + xhttp.status );
        }else{ // errors occured
            console.log(xhttp.status );
        }
    }
    xhttp.open("GET", "generate", true)
    xhttp.send();
}