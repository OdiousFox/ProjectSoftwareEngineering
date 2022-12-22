// this is to get the information from py_wierden and put it into a graph

var url = '/* insert our url here */';

getData();

async function getData() {
  const response = await fetch(url);
  console.log(response);
  const data = await response.json();
  console.log(data);
  length = data.py_wierden.entry_date.length;
  console.log(length);

  time = [];
  temperature = [];

  for (i = 0; i < length; i++) {
    time.push(data.py_wierden.entry_date[i]);
    temperature.push(data.py_wierden.temperature[i]);
  }

  // this is used to create the graph
  new Chart(document.getElementById("test_json"),{
    type: 'line',
    data: {
      labels: time,
      datasets: [
      {
        label: "Temperature",
        data: temperature,
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
