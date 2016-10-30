/* Author: Wilson Xu */

function hide_flask_message_container() {
    $('#flash_message_container').slideUp('fast');
}

var myIP_global;

function connectToBot(response, target, address){
	includeIP={};
	$.extend(includeIP, response, {"ip":address});
	$.ajax({
           url: target,
           data: includeIP,
           error: function(error) {
              console.log("connect to bot failed" + error);
           },
           success: function(data) {
              toastr["success"]("connected to bot");

           },
           type: 'POST',
        });
}
function execute_discovery(element, elementid, target, selector){
  var added=false;
  var done=false;
  exclude = myIP_global.split(".")[3];
  var my_address = myIP_global.split(".").slice(0, 3).join('.');
  $("#"+elementid).empty();
  $("#"+elementid).append('<li><center><a onclick="execute_discovery('+element+','+elementid+','+target+')">Search</a></center></li>');
  $("#"+elementid).append('<li class="divider"></li>');
  for (i=2; i<256; i++) {
    if (i==exclude) {continue;}
    var target_address = "http://"+ my_address + "."+i + ":5000/discovery";
    (function(target_address, i) {
        $.getJSON(target_address, function( data ) {timeout:100} )
        .done(function(response){
        	cut_address = target_address.split(':').slice(0,2).join(':')+'/';
          $("#"+elementid).append('<li>'+
          	'<center><button type="button" class="btn" id="btn'+i+'">'+cut_address+'</button></center></li>');
          
          $("#btn"+i).click(function(){
          	(function (){
          		connectToBot(response, target, cut_address);	
          		
          	})();
          	if (selector){
          		//
          		//
          		//
          		//
          		//
          		setTimeout(function(){window.location.href = consoleTarget[1];}, 2000);
          		 // buggy
						};
			    });
          console.log('== Tried '+target_address.split(':').slice(0,2).join(':')+'/, Success');
          added=true;
        })
        .fail(function() { 
          console.log('-- Tried '+target_address.split(':').slice(0,2).join(':')+'/, Refused');  
        })
        .always(function(){
          if (i==255){
            if (!added) { 
              $("#"+elementid).append('<li"> <center>Not Found</center> </li>'); 
              $("#"+elementid).append('<li class="divider"></li>');
            }
          }
        });
    })(target_address, i);
  }
}

$( document ).ready(function() {
    // obtain IP and save it to global variable
    window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;   //compatibility for firefox and chrome
    var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};      
    pc.createDataChannel("");    //create a bogus data channel
    pc.createOffer(pc.setLocalDescription.bind(pc), noop);    // create offer and set local description
    pc.onicecandidate = function(ice){  //listen for candidate events
    if(!ice || !ice.candidate || !ice.candidate.candidate)  return;
      var myIP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1];
      console.log('my IP: ', myIP);   
      pc.onicecandidate = noop;
      myIP_global = myIP ;
    };
});

