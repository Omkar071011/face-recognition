const updatePlaceholderBackground = (input, placeholderId) => {
    const file = input.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById(placeholderId).style.backgroundImage = `url(${e.target.result})`;
        };
        reader.readAsDataURL(file);
    }
};

document.getElementById('file-input1').addEventListener('change', function () {
    updatePlaceholderBackground(this, 'placeholder1');
});

document.getElementById('identify-button').addEventListener('click', async () => {
    const formData = new FormData();

    const fileInput = document.getElementById('file-input1');
    if (fileInput.files.length > 0) {
        formData.append('image', fileInput.files[0]);
    } else {
        alert('Please select an image');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/identify', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById('output').textContent = JSON.stringify(result, null, 2);
        } else {
            const errorText = await response.text();
            document.getElementById('output').textContent = 'Identification failed: ' + errorText;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('output').textContent = 'An error occurred: ' + error.message;
    }
});