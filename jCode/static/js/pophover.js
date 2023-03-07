$(document).ready(function(){
  $('[data-toggle="popover"]').popover({
    trigger: 'hover',
    container: 'body',
    html: true,
    delay: { "show": 0, "hide": 100 } ,
    template: '<div class="popover popover-custom-arrow" role="tooltip"><div class="arrow arrow-custom"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
  });
});

