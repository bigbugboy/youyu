
function s1(title, data) {
    const myChart = echarts.init(document.getElementById('s1'));
    const option = {
        title: {
            text: title
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
                data: data
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function s2(title, data) {
    const myChart = echarts.init(document.getElementById('s2'));
    const option = {
        title: {
            text: title
        },
        xAxis: {
            type: 'category',
            data: data.captions
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: data.values,
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                }
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function s3(title, data) {
    const myChart = echarts.init(document.getElementById('s3'));
    const option = {
        title: {
            text: title
        },
        xAxis: {
            type: 'category',
            data: data.captions,
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                data: data.values,
                type: 'bar'
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

function s4(title, data) {
    const myChart = echarts.init(document.getElementById('s4'));
    const option = {
        title: {
            text: title
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['今年', '去年'],
            right: '10%'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: data.month,
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '今年',
                type: 'line',
                data: data.this_year_values,
                smooth: true
            },
            {
                name: '去年',
                type: 'line',
                data: data.last_year_values,
                smooth: true
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


function getStatsDate() {
    const currentDate = new Date();
    const thisYear = currentDate.getFullYear()

    fetch('/expense/expense-s1').then((res) => res.json()).then((data) => {
        s1('支出类型【今年】', data)
    })

    fetch('/expense/expense-s2').then((res) => res.json()).then((data) => {
        s2('支出类型【今年】', data)
    })

    fetch('/expense/expense-s3').then((res) => res.json()).then((data) => {
        values = data.values
        mvi = data.max_value_index
        values[mvi] = {
            value: values[mvi],
            itemStyle: { color: '#a90000' }
        }
        newData = {
            captions: data.captions,
            values: values
        }
        s3('每月支出【今年】', newData)
    })
    
    fetch(`/expense/expense-s4/${thisYear}`).then((res) => res.json()).then((data) => {
        let s4_data = {}
        s4_data.month = data.captions;
        s4_data.this_year_values = data.values;
        fetch(`/expense/expense-s4/${thisYear - 1}`).then((res) => res.json()).then((data) => {
            s4_data.last_year_values = data.values;
            console.log(s4_data);
            s4('年度累计支出', s4_data)

        })
    })
}

document.onload = getStatsDate()