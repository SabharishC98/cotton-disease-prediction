function predict() {
    const fileInput = document.getElementById('uploadInput');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = `Predicted Disease: ${data.disease}, Solution: ${data.solution}`;
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please select an image.');
    }
}