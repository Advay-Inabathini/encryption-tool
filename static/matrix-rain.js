// matrix-rain.js
// Matrix rain animation code

function initMatrixRain(canvasId) {
    var canvas = document.getElementById(canvasId),
        ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    var fontSize = 15, // Adjust font size
        columns = canvas.width / fontSize,
        drops = [];

    for (var i = 0; i < columns; i++) {
        drops[i] = 1;
    }

    function draw() {
        ctx.fillStyle = 'rgba(0, 0, 0, .1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        for (var i = 0; i < drops.length; i++) {
            var text = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
            text = text.split('');
            ctx.fillStyle = '#0f0';
            ctx.fillText(text[Math.floor(Math.random() * text.length)], i * fontSize, drops[i] * fontSize);
            drops[i]++;
            if (drops[i] * fontSize > canvas.height && Math.random() > .95) {
                drops[i] = 0;
            }
        }
    }

    setInterval(draw, 44);
}

var MatrixRain = {
    init: initMatrixRain,
};
