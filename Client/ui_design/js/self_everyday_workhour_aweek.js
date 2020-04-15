//var data = [0, 0, 0.7, 0, 0,0,0];
option = {
angleAxis: {
    max: 12,
    startAngle: 45,
    splitLine: {
        show: false
    }
},
radiusAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    z: 10
},
polar: {
},
series: [{
    type: 'bar',
    data: data,
    coordinateSystem: 'polar',
    name: '一周每天在岗时长',
    roundCap: true,
    color: 'rgba(255, 164, 0, 0.5)',
    itemStyle: {
        borderColor: 'orange',
        borderWidth: 2
    }
}],
legend: {
    show: true,
    data: ['一周每天在岗时长']
}
};
var myChart = echarts.init(document.getElementById('main'));
myChart.setOption(option);