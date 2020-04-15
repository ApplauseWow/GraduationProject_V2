//var data = [[0,0,5],[0,1,1],[0,2,0],[0,3,0],[0,4,0],[0,5,0]];
var hours = ['00', '01', '02', '03', '04', '05', '06',
    '07', '08', '09','10','11',
    '12', '13', '14', '15', '16', '17',
    '18', '19', '20', '21', '22', '23'];
var days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

data = data.map(function (item) {
return [item[1], item[0], item[2] || '-'];
});

option = {
tooltip: {
    position: 'top'
},
animation: false,
grid: {
    height: '50%',
    top: '10%'
},
xAxis: {
    type: 'category',
    data: hours,
    splitArea: {
        show: true
    }
},
yAxis: {
    type: 'category',
    data: days,
    splitArea: {
        show: true
    }
},
visualMap: {
    min: 0,
    max: 15,
    calculable: true,
    orient: 'horizontal',
    left: 'center',
    bottom: '15%'
},
series: [{
    name: '出勤人数',
    type: 'heatmap',
    data: data,
    label: {
        show: true
    },
    emphasis: {
        itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
    }
}]
};
var myChart = echarts.init(document.getElementById('main'));
myChart.setOption(option);