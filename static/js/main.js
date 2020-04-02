$(document).ready(function () {

  // Initialize Materialize Navigation 
  $('.sidenav').sidenav();

  // Initialize Materialize Collapsible
  $(document).ready(function () {
    $('.collapsible').collapsible();
  });

  // Initialize Materialize Floating Action Button
  $(document).ready(function () {
    $('.fixed-action-btn').floatingActionButton();

  });

  // Initializing Materialize Tooltips
  document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(elems, {
      isOpen: true
    });
  });


  $(document).ready(function () {
    $('.tooltipped').tooltip();
  });

  // Materialize Collapsible 
  // Class Elements Header - toggle the background color / class elements
  $('.collapsible.collapsible-elem').on('click', '.level-4', function (e) {
    if ($(this).hasClass('collapsible-opened-4')) {
      $(this).removeClass('collapsible-opened-4');
    } else {
      $('.level-4').removeClass('collapsible-opened-4');
      $(this).addClass('collapsible-opened-4');
    }
  });

  // Exercises Headers - toggle the background color / exercises
  $('.collapsible.collapsible-main').on('click', '.level-1', function (e) {
    if ($(this).hasClass('collapsible-opened-1')) {
      $(this).removeClass('collapsible-opened-1');
    } else {
      $('.level-1').removeClass('collapsible-opened-1');
      $(this).addClass('collapsible-opened-1');
    }
  });
  // Exercises content headers - toggle the background color / exercises content
  $('.collapsible.collapsible-sub').on('click', '.level-2', function (e) {
    $(this).toggleClass('collapsible-opened-2');
  });

  
  // Logs headers - toggle the background color / logs
  $('.collapsible.collapsible-log').on('click', '.level-3', function (e) {
    if ($(this).hasClass('collapsible-opened-3')) {
      $(this).removeClass('collapsible-opened-3');
    } else {
      $('.level-3').removeClass('collapsible-opened-3');
      $(this).addClass('collapsible-opened-3');
    }
  });

  // Initializing Materialize Modal
  $('.modal').modal();

  // Initializing Materialize Date Picker

  var elems = document.querySelector('.datepicker');
  M.Datepicker.init(elems, {
    // selectMonths: true, // Creates a dropdown to control month
    // selectYears: 15, // Creates a dropdown of 15 years to control year,
    closeOnSelect: false, // Close upon selecting a date,
    close: 'Ok',
    showClearBtn: true,
    container: null // ex. 'body' will append picker to body
  });

  $('.datepicker').on('mousedown', function(e) {
    e.preventDefault();
  });


  // Materialize initialize form select element
  $('select').formSelect();


  flashed_messages();
  /* Alerts modal */
  function flashed_messages() {
    let messages = parseInt($("#messages p").length);
    if (messages) {
      $("#alerts").slideDown(500);
      setTimeout(() => {
        $("#alerts").slideUp(500);
      }, 4000);
    }
  }

  /* SUMMERNOTE EDITOR */

  var toolbar = [
    ['style', ['style']],
    ['font', ['bold', 'italic', 'underline']],
    ['undo', ['undo', 'redo']],
    ['para', ['ul', 'ol']],
    ['insert', ['emoji']],
    ['misc', ['fullscreen']]
  ];

  $('.summernote').summernote({
    placeholder: 'Text..',
    tabsize: 1.5,
    height: 100,
    toolbar: toolbar,
    styleTags: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
    tooltip: false
  });

  /* RE-STYLING SUMMER NOTE ELEMENTS TO GO WITH MATERIALIZE */
  $('.note-btn').css({
    'background-color': 'rgb(176, 224, 230)',
    'height': '2rem',
    'width': '2.2rem',
    'padding': '0',
    'margin': '0 1px',
    'color': 'rgb(3, 109, 138)',
    'line-height': '0'
  }).removeAttr('tooltip');

  $('.note-btn').mouseover(function () {
    $(this).addClass('note-hover');
  });
  $('.note-btn').mouseout(function () {
    $(this).removeClass('note-hover');
  });

  $('button.note-btn i').css({
    'font-size': '1rem',
    'margin': 'auto'
  });
  $('.note-dropdown-menu a').css({
    'color': 'rgb(3, 109, 138)',
    'line-height': '80%'
  });

  $('.editor ul>li').css({
    'list-style-type': 'initial',
    'margin-left': '2rem'
  });
});