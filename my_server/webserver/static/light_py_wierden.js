
var url = window.location.href+"api";

getData();

async function getData() {
  const response = await fetch(url);
  console.log(response);
  const data = await response.json();
  console.log(data);
  length = data.py_wierden.entry_date.length;
  console.log(length);

  time = [];
  light = [];

  for (i = 0; i < length; i++) {
    time.push(data.py_wierden.entry_date[i]);
    light.push(data.py_wierden.light[i]);
  }

  // this is used to create the graph
  new Chart(document.getElementById("light_py_wierden"),{
    type: 'line',
    data: {
      labels: time,
      datasets: [
      {
        label: "Light",
        data: light,
      },
      ],
    },
    options: {
      legend: { display: false },
      scales: { 
        y: {
          title: {
            display: 'true',
            text: 'light level'
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
          text: 'Light py-Wierden',
          padding: {
            top: 10,
            bottom: 10
          }
        }
      }
    }
  }); 
}