const ctx = document.getElementById('SalesByMonth');
const ctxPie = document.getElementById('SalesByItem');

      
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['January', 'February', 'March', 'April', 'May', 'June','July','August', 'September','October','November', 'December'],
    datasets: [{
      label: 'Earnings in ₱',
      data: [1065, 2259, 480, 1081, 1856, 1855, 2340,1232,2322,1123,2344,1122],
      backgroundColor: [
        'rgba(255, 99, 132, 0.9)',
        'rgba(54, 162, 235, 0.9)',
        'rgba(255, 205, 86, 0.9)',
        'rgba(75, 192, 192, 0.9)',
        'rgba(153, 102, 255, 0.9)',
        'rgba(255, 159, 64, 0.9)',
        'rgba(201, 203, 207, 0.9)',
        'rgba(255, 99, 132, 0.9)',
        'rgba(54, 162, 235, 0.9)',
        'rgba(255, 205, 86, 0.9)',
        'rgba(75, 192, 192, 0.9)',
        'rgba(153, 102, 255, 0.9)',
        ],
        borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 205, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgb(201, 203, 207)',
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 205, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        ],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        responsive: true,
      }
    },
    plugins: {
        title: {
            display: true,
            text: 'Sales by Month',
        }
    }
  }
});

new Chart(ctxPie, {
    type: 'doughnut',
    data: {
        labels: [
            'Casual Shoes',
            'Apple Watch',
            'Denim Shirts'
        ],
        datasets: [{
            label: 'Top Sales',
            data: [300, 50, 100],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)'
            ],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Top Sales by ...',
            }
        }
    }
  });