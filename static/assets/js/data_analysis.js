

const update_counters = (url) => {
// FETCH PERSONAL DEVELOPMENT DATA AGGREGATE
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
        },
    })
        .then(response => response.json())
        .then((data) => {

            document.querySelector('#counter_passages').textContent = data['counter_passages'];
            document.querySelector('#counter_prayers').textContent = data['counter_prayers'];
            document.querySelector('#counter_church_works').textContent = data['counter_church_works'];
            document.querySelector('#counter_evangelism').textContent = data['counter_evangelism'];

            document.querySelector('#circle-progress-passages').dataset.value = data['counter_passages'];
            document.querySelector('#circle-progress-prayers').dataset.value = data['counter_prayers'];
            document.querySelector('#circle-progress-church-work').dataset.value = data['counter_church_works'];
            document.querySelector('#circle-progress-evangelism').dataset.value = data['counter_evangelism'];

            const progressBar = document.getElementsByClassName('circle-progress')
            if(typeof progressBar !== typeof undefined) {
              Array.from(progressBar, (elem) => {
                const minValue = elem.getAttribute('data-min-value')
                const maxValue = elem.getAttribute('data-max-value')
                const value = elem.getAttribute('data-value')
                const  type = elem.getAttribute('data-type')
                if (elem.getAttribute('id') !== '' && elem.getAttribute('id') !== null) {
                  new CircleProgress('#'+elem.getAttribute('id'), {
                    min: minValue,
                    max: maxValue,
                    value: value,
                    textFormat: type,
                  });
                }
              })
            }

            if (window.counterUp !== undefined) {
              const counterUp = window.counterUp["default"];
              const counterUp2 = document.querySelectorAll( '.counter' )
              Array.from(counterUp2, (el) => {
                if (typeof Waypoint !== typeof undefined) {
                  const waypoint = new Waypoint({
                    element: el,
                    handler: function () {
                      counterUp(el, {
                        duration: 1000,
                        delay: 10,
                      });
                      this.destroy();
                    },
                    offset: "bottom-in-view",
                  });
                }
              })
            }



        })
        .catch((error) => {
            console.error(error, 'error')
        })

}

const update_charts = (url) => {
// FETCH PERSONAL DEVELOPMENT DATA AGGREGATE
    fetch(url, {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'Accept': 'application/json',
        },

    })
        .then(response => response.json())
        .then((values) => {
            category = values['category']

            let id_name = "";
            let drop_menu = "";
            let tool_tip = "";

            if (category === 'Bible Reading') {
                id_name = "d-activity-bible-reading";
                drop_menu = 'dropdownMenuButton1';
                tool_tip = "passages"
            }
            else if (category === 'Prayer Marathon') {
                id_name = "d-activity-prayer-marathon";
                drop_menu = "dropdownMenuButton2";
                tool_tip = "prayers"
            }
            else if (category === 'Church Work') {
                id_name = 'd-activity-church-work';
                drop_menu = "dropdownMenuButton3";
                tool_tip = "church work"
            }
            else if (category === 'Evangelism') {

                const val = values['unique_counts'];
                const raw = values['raw_values']

                document.getElementById("people_prayed").textContent = raw[0];
                document.getElementById("led_to_christ").textContent = raw[1];
                document.getElementById("follow_up").textContent = raw[2];
                document.getElementById("baptism").textContent = raw[3];

                if (document.querySelectorAll('#myChart').length) {
                  const options = {
                    series: val,
                    chart: {
                    height: 390,
                    type: 'radialBar',
                  },
                  colors: ["#4bc7d2", "#3a57e8", "#Aa57e8", "#a47132"],
                  plotOptions: {
                    radialBar: {
                      hollow: {
                          margin: 10,
                          size: "50%",
                      },
                      track: {
                          margin: 10,
                          strokeWidth: '50%',
                      },
                      dataLabels: {
                          show: false,
                      }
                    }
                  },
                  labels: ['Apples', 'Oranges', 'Pineapples'],
                  };
                  if(ApexCharts !== undefined) {
                    const chart = new ApexCharts(document.querySelector("#myChart"), options);
                    chart.render();
                    document.addEventListener('ColorChange', (e) => {
                        const newOpt = {colors: [e.detail.detail2, e.detail.detail1],}
                        chart.updateOptions(newOpt)

                    })
                  }
                }

                return;
            }

            document.getElementById(id_name).innerHTML = ""
            document.getElementById(drop_menu).textContent = values['mode'].substring(0, 1).toUpperCase() + values['mode'].substring(1)
            if (document.querySelectorAll(`#${id_name}`).length) {
                const options = {
                  series: [{
                    name: category,
                    data: values['unique_counts']
                  }],
                  chart: {
                    type: 'bar',
                    height: 230,
                    stacked: true,
                    toolbar: {
                        show:true
                      }
                  },
                  colors: ["#3a57e8", "#4bc7d2"],
                  plotOptions: {
                    bar: {
                      horizontal: false,
                      columnWidth: '28%',
                      endingShape: 'rounded',
                      borderRadius: 5,
                    },
                  },
                  legend: {
                    show: false
                  },
                  dataLabels: {
                    enabled: false
                  },
                  stroke: {
                    show: true,
                    width: 2,
                    colors: ['transparent']
                  },
                  xaxis: {
                    categories: values['distinct_values'],
                    labels: {
                      minHeight:20,
                      maxHeight:20,
                      style: {
                        colors: "#8A92A6",
                      },
                    }
                  },
                  yaxis: {
                    title: {
                      text: ''
                    },
                    labels: {
                        minWidth: 19,
                        maxWidth: 19,
                        style: {
                          colors: "#8A92A6",
                        },
                    }
                  },
                  fill: {
                    opacity: 1
                  },
                  tooltip: {
                    y: {
                      formatter: function (val) {
                        return val + ` ${tool_tip}`
                      }
                    }
                  }
                };

                const chart = new ApexCharts(document.querySelector(`#${id_name}`), options);
                chart.render();
                document.addEventListener('ColorChange', (e) => {
                    const newOpt = {colors: [e.detail.detail1, e.detail.detail2],}
                    chart.updateOptions(newOpt)
                })
            }

        })
        .catch(error => {
            console.error(error)
        })
}


