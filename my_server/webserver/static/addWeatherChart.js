async function getDataFromUrl(url){
    const response = await fetch(url,{
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
          "Content-Type": "application/json"
        })
    }).catch((error) =>{
        alert(error);
    });
    return response.json();
}

async function addWeatherChart(output_type, devices){

    var url = window.location.href +'api';

    var data = await getDataFromUrl(url);

    console.log(data)

    time = [];
    temperature_2m = [];

    for(i=0; i< data[devices[0]].entry_hour.length; i++){
        time.push(data[devices[0]]?.entry_hour[i]);
        console.log(data[devices[0]]?.[output_type]);
        temperature_2m.push(data[devices[0]]?.[output_type]?.[i]);
    }

    removeElement("div1");
    
    addElement("div1", "canvas", location);
        
    new Chart(document.getElementById(location),{
        type: 'line',
        data:{
            labels: time,
            datasets: [
                {
                    label: output_type,
                    data: temperature_2m
                }
            ]
        },
        options: {
            legend: { display: false },
            plugins:{
                title: {
                    display: true,
                    text: devices[0]
                }
            }
        }
    });
    
}