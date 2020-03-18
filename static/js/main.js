$(document).ready(function () {
	flashed_messages();



/* Alerts modal */

function flashed_messages() {
	let messages = parseInt($("#messages p").length);
	if (messages) {
		$("#alerts").slideDown(1500);
		setTimeout(() => {
			$("#alerts").slideUp(1500);
		}, 7000);
	}
}


/* Quill */
var toolbarOptions = [['bold', 'italic', 'underline' ], ['link', 'image'], [{ 'list': 'ordered'}, { 'list': 'bullet' }], [{ 'indent': '-1'}, { 'indent': '+1' }], [{ 'header': 3 }, { 'header': 4 }]];
var quill = new Quill('#editor-container', {
  modules: {
    toolbar: toolbarOptions
  },
  placeholder: 'Text...',
  theme: 'snow'
});

var form = document.querySelector('#log_text');
form.onsubmit = function() {
  // Populate hidden form on submit
  var log = document.querySelector('input[name=log_text]');
  log.value = JSON.stringify(quill.getC ontent());
};

/* Collapsible accordion 
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems, options);
  }); */

/* Collapsible Navigation for classes

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(elems, {
      direction: 'left',
      hoverEnabled: false
    });
  });*/

});