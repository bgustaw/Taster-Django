// custom form validation rule
const forbiddenChars = ['/', '@', '=', '?', '+', '|', 'admin']
$.fn.form.settings.rules.validChars = function(value) {
    for (let char of forbiddenChars) {
        if (value.includes(char)) {
            return false
        }
    }
    return true
};

$('.ui form')
    .form({
        fields: {
            id_email: {
                identifier: 'id_email',
                errorLimit: 1,
                rules: [
                    {
                        type: 'email',
                        prompt: 'Please enter correct e-mail'
                    }
                ]
            },
            username: {
                identifier: 'id_username',
                errorLimit: 2,
                rules: [
                    {
                        type: 'minLength[3]',
                        prompt: 'Please enter username with at least 3 characters'
                    },
                    {
                        type: 'validChars',
                        prompt: 'Your username cannot contain forbidden special characters'
                    }

                ]
            },
            password2: {
                identifier: 'id_password2',
                errorLimit: 1,
                rules: [
                    {
                        type: 'match[id_password1]',
                        prompt: 'Passwords do not match'
                    }
                ]
            },
            id_country: {
                identifier: 'id_country',
                errorLimit: 1,
                rules: [
                    {
                        type: 'empty',
                        prompt: 'Please choose your country'
                    }
                ]
            }

        }

    });

if ($('#registerForm').form('is valid')) {
    $(this).form('submit')
}
