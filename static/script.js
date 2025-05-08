const BOARD_SIZE = 10;

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Rozmiar jednej komórki w pikselach
const CELL = canvas.width / BOARD_SIZE;

let gameOver = false;

let currentDirection = 'RIGHT';

// Mapowanie z odwróconą osią Y
const backendDir = {
  UP:    'DOWN',
  DOWN:  'UP',
  LEFT:  'LEFT',
  RIGHT: 'RIGHT'
};

async function initGame() {
  await fetch('/init', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      step: 1,
      board_offset: [0, 0],
      board_size: [BOARD_SIZE, BOARD_SIZE]
    })
  });
  await refreshState();
}

async function refreshState() {
  const res = await fetch('/state');
  const data = await res.json();
  drawBoard({
    snake_body: data.snake_body || data.snake,
    fruits:     data.fruits,
    blocks:     data.blocks
  });
}

async function gameTick() {
  if (gameOver) return;

  // Wysłanie żądania ruchu + tick
  const res = await fetch(`/tick?direction=${backendDir[currentDirection]}`, {
    method: 'PUT'
  });
  const data = await res.json();

  drawBoard({
    snake_body: data.snake,
    fruits:     data.fruits,
    blocks:     data.blocks
  });

  if (data.is_end_game) {
    document.getElementById('message').textContent = 'Game Over!';
    gameOver = true;
  }
}

function drawBoard({ snake_body, fruits, blocks }) {
  // Czyścimy canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Rysujemy siatkę
  ctx.strokeStyle = '#ddd';
  for (let i = 0; i <= BOARD_SIZE; i++) {
    // pionowe linie
    ctx.beginPath();
    ctx.moveTo(i * CELL, 0);
    ctx.lineTo(i * CELL, canvas.height);
    ctx.stroke();
    // poziome linie
    ctx.beginPath();
    ctx.moveTo(0, i * CELL);
    ctx.lineTo(canvas.width, i * CELL);
    ctx.stroke();
  }

  // Rysujemy owoce na czerwono
  ctx.fillStyle = 'red';
  fruits.forEach(([x, y]) => {
    ctx.fillRect(x * CELL, y * CELL, CELL, CELL);
  });

  // Rysujemy bloki na szaro
  ctx.fillStyle = 'gray';
  blocks.forEach(([x, y]) => {
    ctx.fillRect(x * CELL, y * CELL, CELL, CELL);
  });

  // Rysujemy węża na zielono
  ctx.fillStyle = 'green';
  snake_body.forEach(([x, y]) => {
    ctx.fillRect(x * CELL, y * CELL, CELL, CELL);
  });
}

// Tutaj TYLKO zmieniamy kierunek, nie ruszamy węża bo tym się zajmuje tick
window.addEventListener('keydown', e => {
  switch (e.key) {
    case 'ArrowUp':
    case 'w':
      if (currentDirection !== 'DOWN') currentDirection = 'UP';
      break;
    case 'ArrowDown':
    case 's':
      if (currentDirection !== 'UP') currentDirection = 'DOWN';
      break;
    case 'ArrowLeft':
    case 'a':
      if (currentDirection !== 'RIGHT') currentDirection = 'LEFT';
      break;
    case 'ArrowRight':
    case 'd':
      if (currentDirection !== 'LEFT') currentDirection = 'RIGHT';
      break;
  }
});

// inicjalizacja + co 200ms tick
window.addEventListener('load', async () => {
  await initGame();
  setInterval(gameTick, 200);
});
