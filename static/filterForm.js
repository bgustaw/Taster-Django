document.getElementById("submit").addEventListener("click", function () {

    // send information about selected filters
    // 1 or str = do filter by // 0 do not filter by

    let cont = $('#continent-f');
    let continent;
    if (cont.val() !== '') {
        continent = cont.val()
    } else {
        continent = 0
    }

    let countryF = $('#country-f');
    let country;
    if (countryF.val() !== '') {
        country = countryF.val()
    } else {
        country = 0
    }

    if (country !== 0) {
        continent = 0
    }

    let mostLiked;
    if ($('#most-liked-f').checkbox('is checked')) {
        mostLiked = 1
    } else {
        mostLiked = 0
    }

    let bool;
    for (bool of ($('[data-toggle-name="uploaded"]'))) {
        if ($(bool).checkbox('is checked')) {
            $(bool).val('1')
        } else {
            $(bool).val('0')
        }
    }


    let rangeSlider = $('#slider-range-portions')
    let portions1 = $(rangeSlider).slider('get thumbValue', 'first')
    let portions2 = $(rangeSlider).slider('get thumbValue', 'second')
    let portions;
    if (portions1 === 1 && portions2 === 20) {
        portions = 0
    } else {
        portions = portions1.toString() + '|' + portions2.toString()
    }


    let diet;
    let diets = ''
    for (diet of ($('[data-model-name="diet-filter"]'))) {
        if ($(diet).checkbox('is checked')) {
            diets += $(diet).attr('id')+'|'
    }}
    if (diets === '') {
        diets = 0
    }

    let fullTime1 = ($('#slider-full-h').slider('get value', 'first')).toString() + 'H '
    let fullTime2 = $('#slider-full-min').slider('get value', 'second').toString() + 'MIN'
    let fullTimeDelta = fullTime1 + fullTime2
    if (fullTimeDelta === "24H 55MIN") {
        fullTimeDelta = 0
    }

    // send AJAX request, loads new data in html
    let csrf_token = $('[ name="csrfmiddlewaretoken"]').val()

    $('#recipe_body').html('').load(
        '/filter-view',
        {
            csrfmiddlewaretoken: csrf_token,
            continent: continent,
            country: country,
            most_liked: mostLiked,
            newest: $('#newest-f').val(),
            oldest: $('#oldest-f').val(),
            portions: portions,
            diets: diets,
            full_time_delta: fullTimeDelta,
        },)


        })

$('#reset').on('click', function () {
    $('#country-f').parent().dropdown('clear')
    $('#continent-f').parent().dropdown('clear')
    $('#slider-range-portions').slider('set rangeValue', '1', '20')
    $('[data-model-name="min"]').slider('set value', '55')
    $('[data-model-name="h"]').slider('set value', '24')
})

$('#slider-range-portions')
        .slider({
                restrictedLabels: [1, 20],
                min: 1,
                max: 20,
                start: 1,
                end: 20,
                step: 1,
                showThumbTooltip: true,
                tooltipConfig: {
                    position: 'top center',
                    variation: 'small blue'
                }
            },
        )
    ;
    $('[data-model-name="min"]')
        .slider({
                restrictedLabels: [0, 55],
                min: 0,
                max: 55,
                start: 55,
                step: 5,
                showThumbTooltip: true,
                tooltipConfig: {
                    position: 'top center',
                    variation: 'small blue'
                }
            },
        )
    ;
    $('[data-model-name="h"]')
        .slider({
                restrictedLabels: [0, 24],
                min: 0,
                max: 24,
                start: 24,
                step: 1,
                showThumbTooltip: true,
                tooltipConfig: {
                    position: 'top center',
                    variation: 'small blue'
                }
            },
        )
    ;