document.addEventListener('DOMContentLoaded', function() {
    const dataDropdown = document.getElementById('data-dropdown');
    const plotlyVisualization = document.getElementById('plotly-visualization');
    const exportButton = document.getElementById('export-csv');

    dataDropdown.addEventListener('change', function() {
        // You can load your data here based on the selected option and create Plotly visualizations.
        // For simplicity, let's create a placeholder plot.
        const selectedData = dataDropdown.value;

        // Replace this with your actual data and visualization logic.
        const trace = {
            x: [1, 2, 3, 4, 5],
            y: selectedData === 'data1' ? [10, 11, 12, 13, 14] : [15, 16, 17, 18, 19],
            type: 'scatter',
        };
        const layout = {
            title: `Plotly Visualization for ${selectedData}`,
        };

        Plotly.newPlot(plotlyVisualization, [trace], layout);
    });

//    exportButton.addEventListener('click', function() {
        // You can implement the CSV export logic here.
        // For simplicity, we'll export dummy data to the browser's console.
//        const selectedData = dataDropdown.value;
//        const dataToExport = selectedData === 'data1' ? [10, 11, 12, 13, 14] : [15, 16, 17, 18, 19];

        // Log the data to the browser's console.
 //       console.log('Exporting data to CSV:');
//        console.log(dataToExport);
//    });
    exportButton.addEventListener('click', function() {
        const selectedData = dataDropdown.value;

    // Send the data to the Python backend for CSV export.
    fetch('/export_csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(selectedData === 'data1' ? [10, 11, 12, 13, 14] : [15, 16, 17, 18, 19]),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error exporting CSV:', error);
    });
});


});
