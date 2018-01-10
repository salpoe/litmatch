$(document).ready(function() {
  $('.delete_book').click(function() {
    var $this = $(this)
    $.ajax({
      url: '/accounts/recommendation/' + $this.attr('id'),
      type: 'DELETE',
      headers: {
         'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val()
       },
    })
    .done(function(){
      $this.parent().remove()
    })
  });
});
