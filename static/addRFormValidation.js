// validate data
$('#addRecipeForm')
    .form({
        fields: {
            mealName: {
                identifier: 'mealName',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter your meal name'
                    }
                ]
            },
            portions: {
                identifier: 'portions',
                rules: [
                    {
                        type: 'integer[1..20]',
                        prompt: 'Please select portions amount'
                    }
                ]
            },
            prepTimeDelta: {
                identifier: 'prepTimeDelta',
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please enter preparation time'
                    }
                ]
            },
            imgValidate: {
                identifier: 'imgValidate',
                rules: [
                    {
                        type: 'integer[3...10]',
                        prompt: 'Please add at least 2 photos'
                    }
                ]
            },
            ingredients: {
                identifier: 'ingredients',
                errorLimit: 1,
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please add ingredient'
                    },
                ]
            },
            step: {
                identifier: 'step',
                rules: [
                    {
                        type: 'minLength[10]',
                        prompt: 'Please add steps'
                    }
                ]
            }
        }
    });

