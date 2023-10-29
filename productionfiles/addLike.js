$('.spanIcon').on('click', function (){
    $(this).toggleClass('liked')
    let likeCounter = $(this).prev()
    let likedPostID = $(this).attr('data-id')
    let csrf_token = $('[ name="csrfmiddlewaretoken"]').val()
    $.ajax(
        {
            type: 'POST',
            url: '/like-post',
            headers: {'X-CSRFToken': csrf_token},
            data:{
                recipe_id: likedPostID
            },
            success: function ( data ) {
                likeCounter.text(data);
            }

        }
    )
})