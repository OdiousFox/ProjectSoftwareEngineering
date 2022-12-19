async function getData(location){
    if(location == "Doha"){
        latitude = 25.3;
        longitude = 51.5;
    }if(location == "Winnipeg"){
        latitude = 49.9;
        longitude = -97.1;
    }
    var url = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&hourly=temperature_2m`;

    const response = await fetch(url);
    const data = await response.json();

    time = [];
    temperature_2m = [];

    for(i=0; i< 24; i++){
        time.push(data.hourly.time[i]);
        temperature_2m.push(data.hourly.temperature_2m[i]);
    }

    alert(time);
    alert(temperature_2m);

    removeElement("div1");
    
    addElement("div1", "canvas", location);
    
    new Chart(document.getElementById(location),{
        type: 'line',
        data:{
            labels: time,
            datasets: [
                {
                    label: "Temperature",
                    data: temperature_2m
                }
            ]
        },
        options: {
            legend: { display: false },
            plugins:{
                title: {
                    display: true,
                    text: "TestLocation"
                }
            }
        }
    });
}

