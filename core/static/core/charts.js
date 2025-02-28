document.addEventListener("DOMContentLoaded", function () {
    var ctx = document.getElementById('expenseChart').getContext('2d');
    
    var chartLabels = JSON.parse(document.getElementById('chartLabels').textContent);
    var chartValues = JSON.parse(document.getElementById('chartValues').textContent);
    
    var expenseChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Expenses by Category',
                data: chartValues,
                backgroundColor: [
                    'tomato', 'royalblue', 'gold', 'mediumseagreen',
                    'mediumpurple', 'darkorange', 'lightgrey',
                    'steelblue', 'orangered', 'teal'
                ],
                borderColor: 'white',
                borderWidth: 2
            }]
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var ctxBar = document.getElementById('monthlyExpenseChart').getContext('2d');

    var chartLabelsBar = JSON.parse(document.getElementById('chartLabelsBar').textContent);
    var chartValuesBar = JSON.parse(document.getElementById('chartValuesBar').textContent);

    var expenseChartBar = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: chartLabelsBar,
            datasets: [{
                label: 'Total Spending per Month',
                data: chartValuesBar,
                backgroundColor: 'rgba(54, 162, 235, 0.6)', // Blue bars
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    var ctxLine = document.getElementById('spendingTrendChart').getContext('2d');

    var chartLabelsLine = JSON.parse(document.getElementById('chartLabelsLine').textContent);
    var chartValuesLine = JSON.parse(document.getElementById('chartValuesLine').textContent);

    var trendChart = new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: chartLabelsLine,
            datasets: [{
                label: 'Spending Trend Over Time',
                data: chartValuesLine,
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green fill
                borderColor: 'rgba(75, 192, 192, 1)', // Green line
                borderWidth: 2,
                tension: 0.2, // Slight curve for smooth visualization
                pointRadius: 4, // Points on the line
                pointBackgroundColor: 'rgba(75, 192, 192, 1)',
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
