async function getDataFromUrltime(url){
    const response = await fetch(url,{
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
          "Content-Type": "application/json",
          "time-period": "0d7h"
        })
    }).catch((error) =>{
        alert(error);
    });
    return response.json();
}

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function addData(chart, label, data) {
    chart.data.datasets.push({
        label: label,
        data: data,
        borderColor: getRandomColor()
    })
    chart.update();
}

async function addWeatherChart(output_type, devices){

    var url =  window.location.href+'api';

    var data = await getDataFromUrltime(url);

    time = [];

    var all_devices = [];       // a list of all the de devices
    var selected_devices = [];  // the device-type the user selects

    for (device in data) {
        all_devices.push(device);
    }

    for (i = 0; i < devices.length; i++){
        if (devices === "py_devices") {
            selected_devices = all_devices.filter((data) => data.startsWith("py"));
        }
        if (devices === "lht_devices") {
            selected_devices = all_devices.filter((data) => data.startsWith("lht"));
        }
    }

    // for(i = 0; i < data[selected_devices[0]].entry_hour.length; i++){
    //     time.push(data[selected_devices[0]].entry_hour[i]);
    // }

    //for selecting time-period
    for(i = 0; i < data[selected_devices[0]].entry_date.length; i++){
        time.push(data[selected_devices[0]].entry_date[i]);
    }

    removeElement("div1");
    
    addElement("div1", "canvas", location);

    var ctx = document.getElementById(location);
        
    var chart = new Chart(ctx,{
        type: 'line',
        data:{
            labels: time
        },
        options: {
            legend: { display: false },
            plugins:{
                title: {
                    display: true,
                    text: output_type
                }
            }
        }
    });

    for(var device of selected_devices){
        addData(chart, device, data[device][output_type]);  
    }
}