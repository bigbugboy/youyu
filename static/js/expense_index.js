// 基于准备好的dom，初始化echarts实例
function categoryStats(category_data) {
    const myChart = echarts.init(document.getElementById('categoryStats'));
    const option = {
        title: {
            text: '本月支出类型统计'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            bottom: '5%',
            left: 'center'
        },
        series: [
            {
                name: '类型',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: true,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 40,
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: category_data
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function dayStats(day_data) {
    const myChart = echarts.init(document.getElementById('dayStats'));
    const option = {
        title: {
            text: '本月每日支出统计'
        },
        xAxis: {
            type: 'category',
            boundaryGap: false
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '30%']
        },
        visualMap: {
            type: 'piecewise',
            show: false,
            dimension: 0,
            seriesIndex: 0,
            pieces: [
                {
                    gt: 1,
                    lt: 3,
                    color: 'rgba(0, 0, 180, 0.4)'
                },
                {
                    gt: 5,
                    lt: 7,
                    color: 'rgba(0, 0, 180, 0.4)'
                }
            ]
        },
        series: [
            {
                type: 'line',
                smooth: 0.6,
                symbol: 'none',
                lineStyle: {
                    color: '#5470C6',
                    width: 5
                },
                markLine: {
                    symbol: ['none', 'none'],
                    label: { show: false },
                    data: [{ xAxis: 1 }, { xAxis: 3 }, { xAxis: 5 }, { xAxis: 7 }]
                },
                areaStyle: {},
                data: day_data
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


function getStatsDate() {
    fetch('/expense/this_month_data_stats').then((res) => res.json()).then((data) => {
        console.log(data.category_stats)
        console.log(data.day_stats)
        categoryStats(data.category_stats)
        dayStats(data.day_stats)
    })
}


document.onload = getStatsDate()