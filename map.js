var nodes = {
  new google.maps.LatLng(40.443393,-79.939046), //n0
  new google.maps.LatLng(40.442308,-79.939905), //n1
  new google.maps.LatLng(40.442498,-79.940475), //n2
  new google.maps.LatLng(40.442880,-79.942732), //n3
  new google.maps.LatLng(40.442228,-79.943787), //n4
}


function initMap() {
  var uluru = {lat: -25.363, lng: 131.044};
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: uluru
  });
  var marker = new google.maps.Marker({
    position: uluru,
    map: map
  });
}
