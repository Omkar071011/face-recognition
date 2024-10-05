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

document.getElementById('file-input2').addEventListener('change', function () {
    updatePlaceholderBackground(this, 'placeholder2');
});

document.getElementById('file-input3').addEventListener('change', function () {
    updatePlaceholderBackground(this, 'placeholder3');
});

document.getElementById('file-input4').addEventListener('change', function () {
    updatePlaceholderBackground(this, 'placeholder4');
});

document.getElementById('file-input5').addEventListener('change', function () {
    updatePlaceholderBackground(this, 'placeholder5');
});

document.getElementById('train-button').addEventListener('click', async () => {
    const label = document.getElementById('label').value;
    if (!label) {
        alert('Please enter a label');
        return;
    }

    const formData = new FormData();
    formData.append('label', label);

    for (let i = 1; i <= 5; i++) {
        const fileInput = document.getElementById(`file-input${i}`);
        if (fileInput.files.length > 0) {
            formData.append(`image${i}`, fileInput.files[0]);
        } else {
            alert(`Please select an image for Image ${i}`);
            return;
        }
    }

    try {
        const response = await fetch('http://localhost:5000/train', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const result = await response.json();
            alert('Training successful: ' + JSON.stringify(result));
        } else {
            const errorText = await response.text();
            alert('Training failed: ' + errorText);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred: ' + error.message);
    }
});
