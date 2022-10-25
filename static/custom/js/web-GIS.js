//Full screen map view
var mapId = document.getElementById('map');


//Leaflet browser print function
L.control.browserPrint({ position: 'topright' }).addTo(map);


//Leaflet measure
L.control.measure({
    primaryLengthUnit: 'kilometers',
    secondaryLengthUnit: 'meter',
    primaryAreaUnit: 'sqmeters',
    secondaryAreaUnit: 'sqkilometers'
}).addTo(map);

//zoom to layer
$('.zoom-to-layer').click(function () {
    map.setView([38.8610, 71.2761], 7)
})