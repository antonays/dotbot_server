var update = function() {
  $("#update-btn").text("updating...");
  $.get( "/api/v1.0/bin/update", function( data ) {
    location.reload();
  });
}

var set_hostname = function() {
  console.log("test");
  $.get( "/api/v1.0/bin/hostname/"+$("#hostname_text").val(), function( data ) {
    console.log(data);
  });
}
