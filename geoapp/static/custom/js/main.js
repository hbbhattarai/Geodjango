// Api

var Api = 'http://127.0.0.1:8000'


// map class initialize 
var map = L.map('map').setView([27.5142, 90.4336], 9);
map.zoomControl.setPosition('topright');

//functions for leaflet
function highlight(layer) {
    layer.setStyle({
        weight: 2,
        color: '#FF5733'
    });
    if (!L.Browser.ie && !L.Browser.opera) {
        layer.bringToFront();
    }
}

function dehighlight(layer) {
    if (selected === null || selected._leaflet_id !== layer._leaflet_id) {
        dzongkhags.resetStyle(layer);
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

// adding osm tilelayer 
var Carto = L.tileLayer('https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png');

var Imagery = L.tileLayer('http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}').addTo(map);
var Hybrid = L.tileLayer('http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}');
var dzongkhags = L.geoJSON(null,{
        style: function (feature) {
            return {
                color: "#E2DFD2",
                fillColor: feature.properties.color,
                fillOpacity:0.5,
            };
        },
        onEachFeature(feature, layer) {
            layer.bindTooltip(feature.properties.name, { permanent: true, opacity: 0.7 ,direction: 'center' });
            layer.on({
                'mouseover': function (e) {
                    highlight(e.target);
                },
                'mouseout': function (e) {
                    dehighlight(e.target);
                },
                'click': function (e) {
                    select(e.target);
                }
            });
            layer.on('click', function(e) {
                var dzoId = feature.properties.dzoId
                sessionStorage['dzongkhagId'] = dzoId
                location.href = `${Api}/plans/${dzoId}`
            });
        }

    }).addTo(map);
var chiwogs = L.geoJSON(null,{
        style: function (feature) {
            return {
                color: "#E2DFD2",
                fillOpacity:0,
            };
        },
        onEachFeature(feature, layer) {
            layer.bindTooltip(feature.properties.chiwog, { opacity: 0.7 ,direction: 'center' });
        }
    });

//Adding marker in the center of map



var selected = null;
var selectedLayerName = null;

$.getJSON(`${Api}/chiwogs`, function (data) {
    chiwogs.addData(data );
});

$.getJSON(`${Api}/dzongkhags`, function (data) {
    dzongkhags.addData(data );
});



//add map scale
L.control.scale().addTo(map);

//Map coordinate display
map.on('mousemove', function (e) {
    $('.coordinate').html(`Lat: ${e.latlng.lat} Lng: ${e.latlng.lng}`)
})


//Leaflet layer control
var baseMaps = {
    'Satellite Map': Imagery,
    'Carto Map': Carto,
    'Hybrid Map': Hybrid,
}

var overlayMaps = {
    'Dzongkhags':dzongkhags,
    'Chiwogs':chiwogs,
}

L.control.layers(baseMaps, overlayMaps, { collapsed: false, position: 'topleft' }).addTo(map);
