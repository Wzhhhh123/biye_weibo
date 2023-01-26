
var lineChart = echarts.init(document.getElementById('lines'), 'white', {renderer: 'canvas'});
var radarChart = echarts.init(document.getElementById('radar'), 'white', {renderer: 'canvas'});


$(
function changeCountry(){
    $.ajax({
        type: "GET",
        url: "/changecountry",
        dataType: "json",
        success: function (result) {
            lineChart.setOption(result);
        }
    });
})

$(
    function radar(){
        $.ajax({
            type: "GET",
            url: "/radar",
            dataType: "json",
            success: function (result) {
                radarChart.setOption(result);
            }
        });
    })


