"use strict";

// @see: https://en.wikipedia.org/wiki/Superformula
var canvas = document.querySelector("canvas"),
    context = canvas.getContext("2d");

var SCALE = 150;
var VALUES = [];
for (var index = 0; index < 30; index++) {
    VALUES.push(Math.random() * 20000 + 100);
}

function superformula(phi, a, b, m, n1, n2, n3) {
    return Math.pow(Math.pow(Math.abs(Math.cos(m * phi / 4) / a), n2) + Math.pow(Math.abs(Math.sin(m * phi / 4) / b), n3), -1 / n1);
}

function renderFormula(now, t1, t2, t3, i) {
    var s1 = now / t1;
    var s2 = now / t2;
    var s3 = now / t3;

    var a = Math.abs(Math.sin(s1));
    var b = Math.abs(Math.sin(s1));

    var m = Math.abs(Math.sin(s2) * 50);
    var n1 = Math.abs(Math.sin(s3) * 50);
    var n2 = Math.abs(Math.sin(s2) * 50);
    var n3 = Math.abs(Math.sin(s1) * 50);

    context.beginPath();
    for (var index = 0; index < 360; index++) {
        var radius = superformula(index / 360 * Math.PI * 2, a, b, m, n1, n2, n3);
        var x = Math.cos(index / 360 * Math.PI * 2) * radius * SCALE;
        var y = Math.sin(index / 360 * Math.PI * 2) * radius * SCALE;
        if (index === 0) {
            context.moveTo(x, y);
        } else {
            context.lineTo(x, y);
        }
    }
    context.closePath();

    context.globalCompositeOperation = "lighten";

    context.shadowColor = "#0cf";
    context.shadowBlur = 32;

    context.lineWidth = i;
    context.strokeStyle = "#fff";
    context.stroke();
}

function update() {}

function render(now) {
    var s1 = now / 1000;
    var s2 = now / 250;
    var s3 = now / 500;

    var a = Math.abs(Math.sin(s1));
    var b = Math.abs(Math.sin(s1));

    var m = Math.abs(Math.sin(s2) * 50);
    var n1 = Math.abs(Math.sin(s3) * 50);
    var n2 = Math.abs(Math.sin(s2) * 50);
    var n3 = Math.abs(Math.sin(s1) * 50);

    context.clearRect(0, 0, canvas.width, canvas.height);
    context.save();
    context.translate(canvas.width * 0.5, canvas.height * 0.5);
    for (var index = 0; index < VALUES.length; index += 3) {
        renderFormula(now, VALUES[index], VALUES[index + 1], VALUES[index + 2], index + 1);
    }
    context.restore();
}

function frame(now) {
    update();
    render(now);
    window.requestAnimationFrame(frame);
}

function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.requestAnimationFrame(frame);
window.addEventListener("resize", resize);
window.dispatchEvent(new Event("resize"));
window.dispatchEvent(new Event("resize"));