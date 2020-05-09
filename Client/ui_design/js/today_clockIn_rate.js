//var clock_in = 3;
//var total = 40;
var rate = clock_in / total;
var data = [rate, rate*0.8, rate*0.75, rate*0.45];
var option = {
series: [{
    type: 'liquidFill',
    data: data,
    label:{
        formatter: function(param) {
            return '今日出勤率:\n' + clock_in + "/" + total + "\n" + (param.value).toFixed(3) * 100 + "%";
        }
    }
}]
};
var myChart = echarts.init(document.getElementById('main'));
myChart.setOption(option);