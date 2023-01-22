async function getDataFromUrl(url, hours, days){
    const response = await fetch(url,{
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
          "Content-Type": "application/json",
          "time-period":`${days}d${hours}h`
        })
    }).catch((error) =>{
        alert(error);
    });
    return response.json();
}

function getRandomString(){
    var characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var result = '';
    for (var i = 0; i < 6; i++) {
        result += characters[Math.floor(Math.random() * characters.length)];
    }
    return result;
}

function stringToHexColor(labelName){
    switch(labelName){
        case "py_wierden":
            return "#FF0000";
            break;
        case "py_saxion":
            return "#00FF00";
            break;
        case "py_group3":
            return "#0000FF";
            break;
        case "lht_saxion":
            return "#00FFFF";
            break;
        case "lht_wierden":
            return "#FF00FF";
            break;
        case "lht_gronau":
            return "#FFFF00";
            break;
    }
}

function addData(chart, label, data) {
    chart.data.datasets.push({
        label: label,
        data: data,
        borderColor: stringToHexColor(label)
    })
    chart.update();
}

function yLabel(output_type) {
    var y_label;
    if (output_type === "Outside Temperature" || output_type === "Inside Temperature") {
        y_label = "Temperature [°C]"  
    }
    else if (output_type === "Pressure") {
        y_label = "Pressure [hPa]"
    }
    else if (output_type === "Light Intensity") {
        y_label = "Light intensity [Lux]"
    }
    else if (output_type === "Humidity") {
        y_label = "Humidity [rH%]"
    }
    else{
        y_label = ""
    }

    return y_label;
}

function outputType(output_type) {
    var type_output;
    if (output_type === "Outside Temperature") {
        type_output = "Outside_Temperature"  
    }
    else if (output_type === "Inside Temperature") {
        type_output = "Inside_Temperature"  
    }
    else if (output_type === "Pressure") {
        type_output = "pressure"
    }
    else if (output_type === "Light Intensity") {
        type_output = "light_intensity"
    }
    else if (output_type === "Humidity") {
        type_output = "Humidity"
    }
    else{
        type_output = ""
    }

    return type_output;
}

async function addWeatherChart(output_type, devices, hours, days, topDiv){

    var url = "https://a533-2001-1c06-180b-b600-c6dd-83ad-209c-52e5.eu.ngrok.io/webserver/api/";

    var data = await getDataFromUrl(url, hours, days);

    console.log(data);

    time = [];

    for(i=0; i< data[devices[0]].entry_date.length; i++){
        time.push(data[devices[0]].entry_date[i]);
    }

    var chartDivId = getRandomString();
    var chartDiv = addElementToParent(topDiv, "div", "chart-grid-item", chartDivId);

    var canvasId = getRandomString();
    var canvasElement = addElementToParent(chartDiv, "canvas", "canvasClass", canvasId);

    addRemoveButton(chartDiv);
      
    var chart = new Chart(canvasElement,{
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
            },
            scales: {
                x: {
                    title: {
                        display: 'true',
                        text: 'time'
                    }
                },
                y: {
                    title: {
                        display: 'true',
                        text: yLabel(output_type)
                    }
                }
            }
        }
    });

    for(var device of devices){
        addData(chart, device, data[device][outputType(output_type)]);  
    }
}