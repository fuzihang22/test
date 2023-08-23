$(document).ready(function() {
    var map = L.map('map').setView([-31.950527, 115.860457], 13);
    var streetLayer = L.tileLayer.provider('OpenStreetMap.Mapnik');
    var satelliteLayer = L.tileLayer.provider('Stamen.TonerLite');
    
    var baseLayers = {
        "Street": streetLayer,
        "Satellite": satelliteLayer
    };
    
    streetLayer.addTo(map);
    L.control.layers(baseLayers).addTo(map);
    locations.forEach(location => {
        var details = `
        <a href="#${location.buisness}"><strong>${location.buisness}</strong></a><br>
        <p>${location.address}</p>
        `;
        L.marker([location.lat, location.lng])
        .bindPopup(details)
        .addTo(map);
    });
});