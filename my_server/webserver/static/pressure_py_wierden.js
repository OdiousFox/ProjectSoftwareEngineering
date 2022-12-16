
var url = window.location.href+'api';

getData();

async function getData() {
  const response = await fetch(url);
  console.log(response);
  const data = await response.json();
  console.log(data);
  length = data.py_wierden.entry_date.length;
  console.log(length);

  time = [];
  pressure = [];

  for (i = 0; i < length; i++) {
    time.push(data.py_wierden.entry_date[i]);
    pressure.push(data.py_wierden.pressure[i]);
  }

  // this is used to create the graph
  new Chart(document.getElementById("pressure_py_wierden"),{
    type: 'line',
    data: {
      labels: time,
      datasets: [
      {
        label: "Pressure",
        data: pressure,
      },
      ],
    },
    options: {
      legend: { display: false },
      scales: { 
        y: {
          title: {
            display: 'true',
            text: 'pressure [pHa]'
          }
        },
        x: {
          title: {
            display: 'true',
            text: 'time'
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Pressure py_wierden',
          padding: {
            top: 10,
            bottom: 10
          }
        }
      }
    }
  }); 
}