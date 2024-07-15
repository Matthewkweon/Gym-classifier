document.getElementById('classifyButton').addEventListener('click', function() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        // Update this line with your Heroku app URL
        fetch('https://gym-classifier-76781534fd77.herokuapp.com/classify', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('description').textContent = data.description;
            document.getElementById('videoLink').innerHTML = `<a href="${data.video_link}" target="_blank">Watch Tutorial Video</a>`;
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please select an image file.');
    }
});