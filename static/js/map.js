var gmap = {};
gmap.markers = [];

gmap.placeCursor = function(e){
  if (gmap.cursor) {
    gmap.cursor.setMap(null);
  }

  gmap.cursor = new google.maps.Marker(
    {
      position: e.latLng,
      map: gmap.map,
      title: 'here'
    }
  );
  $.ajax(
    '/ig_get_locations',
    {
      'data':{
        'lat':e.latLng.lat(),
        'lng':e.latLng.lng()},
      'dataType':'json',
      'success':function(data){
        gmap.plotLocations(data);
      },
      'error':function(){alert('oops');},
      'type':'post'
    }

  );
};

gmap.plotLocations = function(data){
  var i;
  for( i=0; i < gmap.markers.length; i++ ){
    gmap.markers[i].setMap(null);
  }
  gmap.markers = [];
  for( i=0; i < data['data'].length; i++ ){
    var d = data['data'][i];
    var marker = new google.maps.Marker(
      {
        position: new google.maps.LatLng(
          d.latitude,
          d.longitude),
        map: gmap.map,
        title: d.name
      }
    );

    google.maps.event.addListener(
      marker,
      "click",
      function(_id,_m){return function() {
        gmap.loadPictures(_id, _m);
      };}(d.id, marker)
    );
    gmap.markers[gmap.markers.length] = marker;
  }
  // Zoom and center the map to fit the markers
  // This logic could be conbined with the marker creation.
  // Just keeping it separate for code clarity.
  var bounds = new google.maps.LatLngBounds();
  for (var j=0; j < gmap.markers.length; j++) {
    var marker = gmap.markers[j];
    bounds.extend(marker.getPosition());
  }
  if (gmap.markers.length) {
    gmap.map.fitBounds(bounds);
  }
};

gmap.loadPictures = function(location_id, marker){
  $.ajax(
    '/ig_pictures_for_location',
    {
      'data':{
        'location':location_id},
      'dataType':'json',
      'success':function(data){
        gmap.onLoadPictures(data, marker);
      },
      'error':function(){alert('oops');},
      'type':'post'
    }

  );
};

gmap.onLoadPictures = function(data, marker){
  if (gmap.infowindow) {
    gmap.infowindow.close();
  }
  var height = 100 + 150 * ((data['data'].length / 3)+1);
  var width = 50 + 150 * Math.min(data['data'].length, 3);
  var rootNode = $("<div style='height:"+height+"px; width:"+width+"px;'></div>");
  rootNode.append($("<h2>"+marker.getTitle()+"</h2>"));
  var rootTable = $("<table></table>");
  rootNode.append(rootTable);
  var curRow = $("<tr></tr>");
  for(var i=0; i < 9; i++){
    var curCell = $("<td></td>");
    if (data['data'].length > i) {
      var d = data['data'][i];
      curCell.append(
        $("<span>"+d.created_time_str+"</span>").css(
          {'position':'absolute',
          'background-color':'white',
          'font-family':'monospace',
          'font-size':'11px'})).append(
	$("<img src='"+d.images['thumbnail']['url']+"'/>").click(
	  function(_d){ return function(e){igview.showPicture(_d);}; }(d)
        )
      );
    }
    curRow.append(curCell);
    if( (i+1) % 3 == 0){
      rootTable.append(curRow);
      curRow = $("<tr></tr>");
    }
  }
  rootNode.append(rootTable);
  gmap.infowindow = new google.maps.InfoWindow(
    {
      content: rootNode[0]
    });
  gmap.infowindow.open(gmap.map, marker);
};

function initialize() {
  // Create the map
  // No need to specify zoom and center as we fit the map further down.
  gmap.map = new google.maps.Map(
              document.getElementById("map_canvas"), {
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                streetViewControl: false,
                center: new google.maps.LatLng(37.7593835169, -122.4271774291),
                zoom: 13
              }
  );

  // Create the shared infowindow with two DIV placeholders
  // One for a text string, the other for the StreetView panorama.
  var content = document.createElement("DIV");
  var title = document.createElement("DIV");
  content.appendChild(title);
  var streetview = document.createElement("DIV");
  streetview.style.width = "200px";
  streetview.style.height = "200px";
  content.appendChild(streetview);
  var infowindow = new google.maps.InfoWindow(
    {
      content: content
    });

  google.maps.event.addListener(
    gmap.map,
    "click",
    gmap.placeCursor
  );


function addMarker(data) {
    var marker = new google.maps.Marker(
      {
        position: new google.maps.LatLng(data.lat, data.lng),
        map: gmap.map,
        title: data.name
      }
    );
    google.maps.event.addListener(
      marker,
      "click",
      function() {
        openInfoWindow(marker);
      }
    );



  // Handle the DOM ready event to create the StreetView panorama
  // as it can only be created once the DIV inside the infowindow is loaded in the DOM.
  var panorama = null;
  var pin = new google.maps.MVCObject();
  google.maps.event.addListenerOnce(
    infowindow,
    "domready",
    function() {
      panorama = new google.maps.StreetViewPanorama(
        streetview,
        {
          navigationControl: false,
          enableCloseButton: false,
          addressControl: false,
          linksControl: false,
          visible: true
        });
        panorama.bindTo("position", pin);
    });

  // Set the infowindow content and display it on marker click.
  // Use a 'pin' MVCObject as the order of the domready and marker click events is not garanteed.
  function openInfoWindow(marker) {
    title.innerHTML = marker.getTitle();
    pin.set("position", marker.getPosition());
    infowindow.open(gmap.map, marker);
  }
}
}