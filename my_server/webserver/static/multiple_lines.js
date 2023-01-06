getData();

async function getDataFromUrl(/*url*/){
    var url = window.location.href+'api';
  
    const response = await fetch(url,{
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
          "Content-Type": "application/json",
          "time-period":"0d7h",
        })
    }).catch((error) =>{
        alert(error);
    });
    return response.json();
  }

async function getData(){
    var data = await getDataFromUrl();

    time = [];
    temp_py_wierden = [];
    temp_py_saxion = [];

    for(i = 0; i < data.py_wierden.entry_hour.length; i++){
        time.push(data.py_wierden.entry_hour[i]);
        temp_py_wierden.push(data.py_wierden.temperature[i]);
        temp_py_saxion.push(data.py_saxion.temperature[i]);
    }

    console.log(time);
    console.log(temp_py_wierden);

    new Chart(document.getElementById("line-chart"),{
        type: 'line',
        data:{
            labels: time,
            datasets: [
                {
                    label: "py_wierden",
                    data: temp_py_wierden
                },
                {
                    label: "py_saxion",
                    data: temp_py_saxion
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