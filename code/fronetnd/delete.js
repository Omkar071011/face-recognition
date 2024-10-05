document.getElementById('deleteForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const label = document.getElementById('label').value;
    const responseMessage = document.getElementById('responseMessage');

    try {
        const response = await fetch('http://localhost:5000/delete', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ label: label }),
        });

        if (response.ok) {
            const data = await response.json();
            responseMessage.textContent = data.message;
            responseMessage.style.color = 'green';
        } else {
            const errorData = await response.json();
            responseMessage.textContent = `Error: ${errorData.error}`;
            responseMessage.style.color = 'red';
        }
    } catch (error) {
        responseMessage.textContent = `Error: ${error.message}`;
        responseMessage.style.color = 'red';
    }
});