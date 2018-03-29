const canvas = document.getElementById("tetris");
const context = canvas.getContext('2d');
var gameOVer = false;
context.scale(20, 20)
    
function arenaSweep() {
    let rowCount = 1;
    outer: for (let y = arena.length - 1; y > 0; y--) {
        for (let x = 0; x < arena[y].length; x++) {
            if (arena[y][x] == 0) {
                continue outer;
            }
        }
        const row = arena.splice(y, 1)[0].fill(0);
        arena.unshift(row);
        y++;

        player.score += rowCount * 100;
        rowCount *= 2;
        dropInterval *= 0.8;
    }
}

function collide(arena, player) {
    const m = player.matrix;
    const o = player.position;
    for (let y = 0; y < m.length; y++) {
        for (let x = 0; x < m[y].length; x++) {
            if (m[y][x] !== 0 &&
                (arena[y + o.y] &&
                    arena[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;
};

function createMatrix(w, h) {
    const matrix = [];
    while (h--) {
        matrix.push(new Array(w).fill(0))
    }
    return matrix;

};

function createPiece (type) {
    if (type == 'T') {
        return [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0],
        ];
    } else if (type == 'O') {
        return [
            [2, 2],
            [2, 2],
        ];
    } else if (type == 'I') {
        return [
            [0, 3, 0, 0],
            [0, 3, 0, 0],
            [0, 3, 0, 0],
            [0, 3, 0, 0]
        ];
    } else if (type == 'S') {
        return [
            [0, 0, 0],
            [0, 4, 4],
            [4, 4, 0],
        ];
    } else if (type == 'Z') {
        return [
            [0, 0, 0],
            [5, 5, 0],
            [0, 5, 5],
        ];
    } else if (type == 'L') {
        return [
            [0, 6, 0],
            [0, 6, 0],
            [0, 6, 6],
        ];
    } else if (type == 'J') {
        return [
            [0, 7, 0],
            [0, 7, 0],
            [7, 7, 0],
        ];
    }
}   

function draw() {
    //draw canvas
    context.fillStyle = "#FFF";
    context.fillRect(0, 0, canvas.width, canvas.height);
    //draw piece
    drawMatrix(arena, {
        x: 0,
        y: 0
    })
    drawMatrix(player.matrix, player.position);


}

function drawMatrix(matrix, offset) { //offset allows the piece to move
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                context.strokeStyle = "black";
                context.lineWidth = .05;
                context.fillStyle = colors[value];
                context.fillRect(x + offset.x, y + offset.y, 1, 1);
                context.strokeRect(x + offset.x, y + offset.y, 1, 1);
            }
        });
    });
}

function merge(arena, player) {
    player.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                arena[y + player.position.y][x + player.position.x] = value;
            }
        })
    })
}

function rotate(matrix, dir) {
    for (let y = 0; y < matrix.length; y++) {
        for (let x = 0; x < y; x++) {
            [
                matrix[x][y],
                matrix[y][x]
            ] = [
                matrix[y][x],
                matrix[x][y]
            ];
        }
    }
    if (dir > 0) {
        matrix.forEach(row => row.reverse());
    } else {
        matrix.reverse();
    }
}

function playerDrop() {
    player.position.y++;
    if (collide(arena, player)) {
        player.position.y--;
        merge(arena, player);
        playerReset();
        arenaSweep();
        updateScore();
        }
    dropCounter = 0;
}

function playerMove(offset) {
    player.position.x += offset;
    if (collide(arena, player)) {
        player.position.x -= offset;
    }

}

function playerReset() { // <---- GAME OVER CONDITION HERE
    const pieces = "ILJOTSZ"
    player.matrix = createPiece(pieces[pieces.length * Math.random() | 0]);
    player.position.y = 0;
    player.position.x = (arena[0].length / 2 | 0) -
                        (player.matrix[0].length / 2 | 0);
    if (collide(arena, player)) {
        arena.forEach(row => row.fill(0));
        alert("Game over!")
        sendScore();
        player.score = 0;
        updateScore();
    }
}

function playerRotate(dir) {
    const pos = player.position.x;
    let offset = 1;
    rotate(player.matrix, dir);
    while (collide(arena, player)) {
        player.position.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > player.matrix[0].length) {
            rotate(player.matrix, -dir);
            player.position.x = pos;
            return;
        }
    }
}

let dropCounter = 0;
let dropInterval = 1000;

let lastTime = 0;

function update(time = 0) {
    const dTime = time - lastTime;
    dropCounter += dTime;
    if (dropCounter > dropInterval) {
        playerDrop();
    }
    lastTime = time;
    draw();
    requestAnimationFrame(update);
}

function updateScore() {
    document.getElementById('score').innerText = player.score
}

function sendScore() {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
    $.ajax({
        url: "/games/receiver",
        data: playerScore,                
        type: 'POST',
        success: function (response) {
            console.log("This is a test of the emergency broadcast system.");
        }
    },
    );
};

const colors = [
    null,
    'red',
    'orange',
    'yellow',
    'green',
    'blue',
    'purple',
    'teal'
]

const arena = createMatrix(12, 25);
const player = {
    position: {
        x: 0,
        y: 0
    },
    matrix: null,
    score: 0,
}

//event listeners
document.addEventListener("keydown", event => {
    if (event.keyCode == 37) {
        // player.position.x--;
        playerMove(-1);
    } else if (event.keyCode == 39) {
        // player.position.x++;
        playerMove(1);
    } else if (event.keyCode == 40) {
        playerDrop();
        // playerMove(1);
    } else if (event.keyCode == 38) {
        playerRotate(-1)
    }

});

//up is 38
//down is 30
//space is 32 <-- in order to pause or start

playerReset();
updateScore();
update();