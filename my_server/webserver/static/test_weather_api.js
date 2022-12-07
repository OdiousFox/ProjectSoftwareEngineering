var url = 'https://api.open-meteo.com/v1/forecast?latitude=52.2&longitude=8.9&hourly=temperature_2m';

getData();

async function getData(){
    const response = await fetch(url);
    console.log(response);
    const data = await response.json();
    console.log(data);
    length = data.hourly.time.length;
    console.log(length);

    time = [];
    temperature_2m = [];

    for(i=0; i< length; i++){
        time.push(data.hourly.time[i]);
        temperature_2m.push(data.hourly.temperature_2m[i]);
    }

    new Chart(document.getElementById("weather-chart"),{
        type: 'line',
        data: {
            labels: time,
            datasets: [
                {
                    label: "Temperature",
                    data: temperature_2m,
                },
            ],
        },
        options: {
            legend: { display: false },
            scales: { 
                y: {
                    title: {
                        display: 'true',
                        text: 'yTitle'
                    }
                },
                x: {
                    title: {
                        display: 'true',
                        text: 'xTitle'
                    }
                }
            },
            plugins: {
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
