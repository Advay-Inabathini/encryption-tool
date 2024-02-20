$(document).ready(function () {
    $('#encryptionForm').submit(function (e) {
        e.preventDefault();
        console.log('Form submitted');

        var text = $('#text').val();
        var password = $('#password').val();
        var algorithm = $('#algorithm').val();
        var operation = $('#operation').val();

        console.log('Text:', text);
        console.log('Password:', password);
        console.log('Algorithm:', algorithm);
        console.log('Operation:', operation);

        $.ajax({
            type: 'POST',
            url: '/',
            data: {
                text: text,
                password: password,
                algorithm: algorithm,
                operation: operation
            },
            success: function (response) {
                console.log('Success:', response);
                if (algorithm === 'RSA' && operation === 'encrypt') {
                    alert('Encrypted text:\n' + response.result + '\n\nPrivate key:\n' + response.private_key);
                } else {
                    alert('Result:\n' + response.result);
                }
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });
});
