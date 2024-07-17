document.getElementById('classifyButton').addEventListener('click', function() {
    const fileInput = document.getElementById('imageUpload');
    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('https://gym-classifier-76781534fd77.herokuapp.com/classify', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.description);  // Log the description for debugging

            // Hard-code a test string with new lines for debugging
            const testDescription = `**Equipment: Bench Press**\n\n**To-Do List:**\n\n1. **How it's used and what muscles it targets:**\n - **Usage:** Lie down flat on the bench with your feet firmly on the floor. Grip the barbell with both hands slightly wider than shoulder-width. Lower the bar to your mid-chest, then push it back up to the starting position.\n - **Targeted Muscles:** Primarily targets the pectoral muscles (chest). Secondary muscles worked include the triceps, shoulders, and to a lesser extent, the lats and forearms.\n\n2. **Tips for proper form or common mistakes to avoid:**\n - **Proper Form:** Keep your feet flat on the floor throughout the exercise. Your back should have a natural arch, with your upper back and buttocks in contact with the bench. Lower the bar to your mid-chest (avoid bouncing it off your chest). Fully extend your arms at the top of the movement but avoid locking your elbows.\n - **Common Mistakes to Avoid:** Avoid lifting your feet off the ground or moving them during the lift. Do not flare your elbows outward excessively; keep a slight inward angle. Ensure you’re not using weights too heavy to maintain proper form. Avoid bouncing the bar off your chest, which can lead to injury.`;

            document.getElementById('description').innerHTML = testDescription.replace(/\n/g, '<br>');
            document.getElementById('videoLink').innerHTML = `<a href="${data.video_link}" target="_blank">Watch Tutorial Video</a>`;
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please select an image file.');
    }
});
