async function getDataFromUrl(url){
    const response = await fetch(url,{
        method: "get",
        headers: new Headers({
          "ngrok-skip-browser-warning": "69420",
          "Content-Type": "application/json",
        //   "time-period": "0d7h"
        })
    }).catch((error) =>{
        alert(error);
    });
    return response.json();
}

async function generateTable() {
    var url = "https://99b4-2001-1c06-180b-b600-c6dd-83ad-209c-52e5.eu.ngrok.io/webserver/api/";

    var data = await getDataFromUrl(url);

    var all_devices = [];       // a list of all the de devices
    var meta_data = [];

    for (device in data) {
        all_devices.push(device);
    }

    for (var i = 0; i < 1; i++) {
        meta_data.push(data[all_devices[0]].meta_data);
    }

    // creates a <table> element and a <tbody> element
    const tbl = document.createElement("table");
    const tblBody = document.createElement("tbody");

    const tblHead = document.createElement("thead");
    for (var i = 0; i < 1; i++) {
        const row = document.createElement("tr");
        const cell = document.createElement("th");
        const cell1 = document.createElement("th");
        const cell2 = document.createElement("th");
        const cell3 = document.createElement("th");
        const cell4 = document.createElement("th");
        const cell5 = document.createElement("th");
        const cell6 = document.createElement("th");

        const cellText = document.createTextNode("Device");
        const cellText1 = document.createTextNode("Air time");
        const cellText2 = document.createTextNode("Gateway id");
        const cellText3 = document.createTextNode("Latitude");
        const cellText4 = document.createTextNode("Longitude");
        const cellText5 = document.createTextNode("Rssi");
        const cellText6 = document.createTextNode("Snr");

        cell.appendChild(cellText);
        cell1.appendChild(cellText1);
        cell2.appendChild(cellText2);
        cell3.appendChild(cellText3);
        cell4.appendChild(cellText4);
        cell5.appendChild(cellText5);
        cell6.appendChild(cellText6);

        row.appendChild(cell);
        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);
        row.appendChild(cell5);
        row.appendChild(cell6);

        tblHead.appendChild(row);
    }

    for (var i = 0; i < all_devices.length; i++){
        console.log("length of all devices: " + all_devices.length);

        const row = document.createElement("tr");

        const cell = document.createElement("td");
        const cellText = document.createTextNode(all_devices[i]);
        cell.appendChild(cellText);
        row.append(cell);

        const cell1 = document.createElement("td");
        const cell2 = document.createElement("td");
        const cell3 = document.createElement("td");
        const cell4 = document.createElement("td");
        const cell5 = document.createElement("td");
        const cell6 = document.createElement("td");

        const cellText1 = document.createTextNode(data[all_devices[i]].meta_data.airtime);
        const cellText2 = document.createTextNode(data[all_devices[i]].meta_data.gateway_id);
        const cellText3 = document.createTextNode(data[all_devices[i]].meta_data.latitude);
        const cellText4 = document.createTextNode(data[all_devices[i]].meta_data.longitude);
        const cellText5 = document.createTextNode(data[all_devices[i]].meta_data.rssi);
        const cellText6 = document.createTextNode(data[all_devices[i]].meta_data.snr);

        cell1.appendChild(cellText1);
        cell2.appendChild(cellText2);
        cell3.appendChild(cellText3);
        cell4.appendChild(cellText4);
        cell5.appendChild(cellText5);
        cell6.appendChild(cellText6);

        row.appendChild(cell1);
        row.appendChild(cell2);
        row.appendChild(cell3);
        row.appendChild(cell4);
        row.appendChild(cell5);
        row.appendChild(cell6);

        tblBody.appendChild(row);
    }

    tbl.appendChild(tblHead);
    // put the <tbody> in the <table>
    tbl.appendChild(tblBody);
    // appends <table> into <body>
    document.head.appendChild(tbl);
    document.body.appendChild(tbl);
    // sets the border attribute of tbl to '2'
    tbl.setAttribute("border", "1");
}
  