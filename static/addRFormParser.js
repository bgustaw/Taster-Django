// parse data before sending to server
document.getElementById("addRecipeForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting immediately
    
    // parse prepare and cooking time delta
    let prepTimeDelta = ''
    document.getElementsByName('prepTimeDelta').forEach(function (prepTime, number) {
        let v1;
        if (number === 0) {
            v1 = prepTime.value + 'H '
        } else {
            v1 = prepTime.value + 'MIN'
        }
        prepTimeDelta += v1
    })
    document.getElementById('parsedPrepTimeDelta').value = prepTimeDelta

    let cookTimeDelta = ''
    document.getElementsByName('cookTimeDelta').forEach(function (cookTime, number) {
        let v2;
        if (number === 0) {
            v2 = cookTime.value + 'H '
        } else {
            v2 = cookTime.value + 'MIN'
        }
        cookTimeDelta += v2
    })
    document.getElementById('parsedCookTimeDelta').value = cookTimeDelta



    //if nutrition - validate number and parse its data
    let parsedNutritionData;
    let flag = $('#nutrFlag')
    if (flag.attr('value')) {
        parsedNutritionData = flag.attr('value')         // changed from #nutrFlag
        document.getElementsByName('nutrition').forEach(function (data) {
            let value = data.value
            if (value === '') {
                value = ' | ' + '-'
                parsedNutritionData += value
                return
            } else {
                value = ' | ' + parseFloat(value).toString()
                parsedNutritionData += value
            }
        })
        document.getElementById('parsedNutritionData').value = parsedNutritionData
    }

    // parse ingredients
    let parsedIngredients = ''
    document.getElementsByName('ingredients').forEach(function (ingredient) {
        let value = ingredient.value
        if (parsedIngredients.length === 0) {
            parsedIngredients += value
        } else {
            parsedIngredients += ' | ' + value
        }
    })
    document.getElementById('parsedIngredients').value = parsedIngredients
    
    // parse steps
    let parsedSteps = ''
    document.getElementsByName('step').forEach(function (step) {
        let value = step.value + '&'
        parsedSteps += value
    })
    document.getElementById('parsedSteps').value = parsedSteps

    $('#addRecipeForm').form('submit')

});