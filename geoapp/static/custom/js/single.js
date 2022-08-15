
// map class initialize 
var map = L.map('map').setView([27.5142, 90.4336], 9);
map.zoomControl.setPosition('topright');


//Adding marker in the center of map

var selected = null;
var selectedLayerName = null;
var dzoId = sessionStorage.getItem('dzongkhagId');



// adding osm tilelayer 
var Carto = L.tileLayer('https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png').addTo(map);

var Imagery = L.tileLayer('http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}');
var Hybrid = L.tileLayer('http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}');

var BaseLayers = {
    'Carto Map': Carto,
    'Satellite Imagery': Imagery,
    'Hybrid Imagery': Hybrid,
}


var controlLayers = L.control.layers(BaseLayers, null, { collapsed: false, position: 'topleft' }).addTo(map);
//add map scale
L.control.scale().addTo(map);

//Map coordinate display
map.on('mousemove', function (e) {
    $('.coordinate').html(`Lat: ${e.latlng.lat} Lng: ${e.latlng.lng}`)
});

$.getJSON(`http://127.0.0.1:8000/dzongkhag/${dzoId}`, function (data) {
    var dzongkahg = L.geoJSON(data, {
        style: function (feature) {
            return {
                color: "#FFF",
                opacity: 2,
            };
        },
        onEachFeature(feature, layer) {
        }
    });

});

$.getJSON(`http://127.0.0.1:8000/boundary`, function (data) {
    var boundray = L.geoJSON(data, {
        style: function (feature) {
            return {
                color: "#0C0A09",
                fillColor: "#FFF",
                opacity: 0.7,
            };
        },
        onEachFeature(feature, layer) {
            var layerBoundray = layer.getBounds()
            map.fitBounds(layerBoundray)
        }
    })
    controlLayers.addOverlay(boundray, 'Boundray');

});

$.getJSON(`http://127.0.0.1:8000/precient`, function (data) {
    var precient = L.geoJSON(data, {
        style: function (feature) {
            return {
                color: feature.properties.color,
                fillColor: feature.properties.color,
            };
        },
        onEachFeature(feature, layer) {

            layer.bindTooltip(feature.properties.precinct, { permanent: false, opacity: 0.7, direction: 'center' });
            var popup = L.popup()
                    .setContent(` 
                    
                    <strong> Name: </strong> ${feature.properties.precinct}  

                    <br />
                    
                    <strong> Area: </strong> ${feature.properties.area} Acres

                    <br />

                    <strong> Description: </strong> ${feature.properties.details}
                    ` )
                    .openOn(layer);

            layer.bindPopup(popup).openPopup();
            layer.on({
                'click': function (e) {
                    highlight(e.target);
                    select(e.target);
                }
            });


        }

        
    });
    function highlight(layer) {
        layer.setStyle({
            weight: 2,
            color: "#0C0A09",
            fillColor: "#FF5733",
            opacity: 0.6,
        });
        if (!L.Browser.ie && !L.Browser.opera) {
            layer.bringToFront();
        }
    }

    function dehighlight(layer) {
        if (selected === null || selected._leaflet_id !== layer._leaflet_id) {
            precient.resetStyle(layer);
        }
    }

    function select(layer) {
        if (selected !== null) {
            var previous = selected;
        }
        map.fitBounds(layer.getBounds());
        selected = layer;
        if (previous) {
            dehighlight(previous);
        }
    }
    
    precient.addTo(map);
    controlLayers.addOverlay(precient, 'Precient');

});

$.getJSON(`http://127.0.0.1:8000/plot`, function (data) {
    var plot = L.geoJSON(data, {
        style: function (feature) {
            return {
                color: "#7F968C",
                fillColor: "#7F968C",
                width: 0.2,
            };
        },
        onEachFeature(feature, layer) {
            layer.bindTooltip(feature.properties.plot_id, { permanent: false, opacity: 0.7, direction: 'center' });
        }

    });
    controlLayers.addOverlay(plot, 'Plot');

});


