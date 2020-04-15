var rate = clock_in / total;
var data = [rate, rate-0.1, rate-0.15, rate-0.25];
var option = {
series: [{
    type: 'liquidFill',
    data: data,
    label:{
        formatter: function(param) {
            return '今日出勤率:\n' + clock_in + "/" + total + "\n" + param.value * 100 + "%";
        }
    }
}]
};
var myChart = echarts.init(document.getElementById('main'));
myChart.setOption(option);