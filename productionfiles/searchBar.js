let pos = $('#rightMenu').children().first().offset().left
let sb = $('#searchBar')
let wid = sb.css('width')
let off = sb.offset().left
let diff = pos - off - (parseFloat(sb.parent().css('padding-right').slice(0, -2))) - 20


$(function () {
    $('#search').parent().css('width', diff)
})


// ajax search request
let csrf_token = $('[name="csrfmiddlewaretoken"]').val()


$('#searchBtn').on('click', function () {
    if ($(this).prev().val() !== '') {
        $('#recipe_body').html('').load(
        '/search-view',
        {
            csrfmiddlewaretoken: csrf_token,
            keyword: $(this).prev().val()
        },
        )

        }
    })



