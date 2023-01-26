function bodyScale() {
    var devicewidth = document.documentElement.clientWidth;
    var scale = devicewidth / 1440;  // 分母——设计稿的尺寸
    document.body.style.zoom = scale;
}
window.onload = window.onresize = function () {
    bodyScale();
};