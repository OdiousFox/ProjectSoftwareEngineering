getData();

async function getDataFromUrl(/*url*/){
    var url = window.location.href+'api';
  
    const response = await fetch(url,{
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
          "Content-Type": "application/json",
          "time-period":"0d7h"
        })
    }).catch((error) =>{
        alert(error);
    });
    return response.json();
  }

async function getData() {
  var data = await getDataFromUrl();

  time = [];
  pressure_py_wierden = [];
  pressure_py_saxion = [];

  for(i = 0; i < data.py_wierden.entry_hour.length; i++){
      time.push(data.py_wierden.entry_hour[i]);
      pressure_py_wierden.push(data.py_wierden.pressure[i]);
      pressure_py_saxion.push(data.py_saxion.pressure[i]);
  }

  // this is used to create the graph
  new Chart(document.getElementById("pressure_py_wierden"),{
    type: 'line',
    data:{
        labels: time,
        datasets: [
            {
                label: "py_wierden",
                data: pressure_py_wierden
            },
            {
                label: "py_saxion",
                data: pressure_py_saxion
            },
        ]
    },
    options: {
        legend: { display: false },
        scales: {
            y: {
                title: {
                    display: 'true',
                    text: 'temp in degrees Celsius'
                }
            },
            x: {
                title: {
                    display: 'true',
                    text: 'time in hours'
                }
            }
        },
        plugins:{
            title: {
                display: true,
                text: 'Temperature',
                padding: {
                    top: 10,
                    bottom: 10
                }
            }
        }
    }
});
}