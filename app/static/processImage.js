$(document).ready(function () {

    var scripts = document.getElementById('makeGraph');
    var image_source = scripts.getAttribute('img');
    console.log(image_source);
    makeGraph(image_source);
});

function calculateHistogram(imageData) {
    let histogramData = Array(256).fill(0);

    for (let i = 0; i < imageData.data.length; i += 4) {
        let brightness = Math.round((imageData.data[i] + imageData.data[i + 1] + imageData.data[i + 2]) / 3);
        histogramData[brightness]++;
    }

    return histogramData;
}

function makeGraph(results) {
    console.log(results);
    var img_Src = results;
    console.log(img_Src);

    // Supponiamo che tu abbia già l'elemento canvas nel tuo HTML con l'id "classificationOutput"
    var ctx = document.getElementById("imageHistogram").getContext('2d');

    // Caricamento dell'immagine
    var image = new Image();
    image.src = img_Src;

    image.onload = function () {
        // Creazione del canvas
        ctx.canvas.width = image.width;
        ctx.canvas.height = image.height;
        ctx.drawImage(image, 0, 0, image.width, image.height);

        // Calcolo dell'istogramma
        let imageData = ctx.getImageData(0, 0, image.width, image.height);
        let histogramData = calculateHistogram(imageData);

        // Creazione del grafico con Chart.js
        var histogramChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Array.from({ length: 256 }, (_, i) => i),
                datasets: [{
                    label: 'Istogramma',
                    data: histogramData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom'
                    },
                    y: {
                        type: 'linear',
                        position: 'left'
                    }
                }
            }
        });
    };
}
