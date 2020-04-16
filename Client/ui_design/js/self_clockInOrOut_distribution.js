//var data_clockin = [[0, 0, 5],[0, 2, 5],[0, 3, 5],[0, 13, 5], [6, 1, 6]];
//var data_clockout = [[0, 12, 5],[1, 14, 5],[2, 16, 5],[0, 11, 5], [6, 16, 6]];
var hours = ['00', '01', '02', '03', '04', '05', '06',
    '07', '08', '09','10','11',
    '12', '13', '14', '15', '16', '17',
    '18', '19', '20', '21', '22', '23'];
var days = ['Monday', 'Tuesday','Wednesday',
    'Thursday', 'Friday', 'Saturday', 'Sunday'];

option = {
title: {
    text: '本周出勤/离岗时间点'
},
legend: {
    data: ['出勤','离岗'],
    left: 'right'
},
polar: {},
tooltip: {
    formatter: function (params) {
        return ' clocked in/out at ' + hours[params.value[1]] + ' on ' + days[params.value[0]];
    }
},
angleAxis: {
    type: 'category',
    data: hours,
    boundaryGap: false,
    splitLine: {
        show: true,
        lineStyle: {
            color: '#999',
            type: 'dashed'
        }
    },
    axisLine: {
        show: false
    }
},
radiusAxis: {
    type: 'category',
    data: days,
    axisLine: {
        show: true
    },
    axisLabel: {
        rotate: 35
    }
},
series: [{
    name: '出勤',
    type: 'scatter',
    color: 'green',
    coordinateSystem: 'polar',
    symbolSize: function (val) {
        return val[2] * 2;
    },
    data: data_clockin,
    animationDelay: function (idx) {
        return idx * 5;
    }
},{
    name: '离岗',
    type: 'scatter',
    coordinateSystem: 'polar',
    symbolSize: function (val) {
        return val[2] * 2;
    },
    data: data_clockout,
    animationDelay: function (idx) {
        return idx * 5;
    }
}
]
};
var myChart = echarts.init(document.getElementById('main'));
myChart.setOption(option);