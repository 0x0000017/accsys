const prdBreak = document.getElementById('prodBreakdown');
const prdBreak1 = document.getElementById('prodBreakdown1');
const prdBreak2 = document.getElementById('prodBreakdown2');

      

new Chart(prdBreak, {
  type: 'doughnut',
  data: {
    labels: [
      'Electronics',
      'Furniture',
      'Bags and Packages',
      'Accessories'
    ],
    datasets: [{
      label: 'Sales Breakdown by Product',
      data: [300, 100, 60, 30, 10],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(0,88,255)'
      ],
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Sales Breakdown by Product',
      }
    }
  }
});
new Chart(prdBreak1, {
  type: 'doughnut',
  data: {
    labels: [
      'Electronics',
      'Furniture',
      'Bags and Packages',
      'Accessories'
    ],
    datasets: [{
      label: 'Sales Breakdown by Product',
      data: [300, 100, 60, 30, 10],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(0,88,255)'
      ],
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Sales Breakdown by Product',
      }
    }
  }
});
new Chart(prdBreak2, {
  type: 'doughnut',
  data: {
    labels: [
      'Electronics',
      'Furniture',
      'Bags and Packages',
      'Accessories'
    ],
    datasets: [{
      label: 'Sales Breakdown by Product',
      data: [300, 100, 60, 30, 10],
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(0,88,255)'
      ],
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Sales Breakdown by Product',
      }
    }
  }
});