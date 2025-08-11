let mediaRecorder;
let audioChunks = [];
let recording = false;

const recordButton = document.getElementById('recordButton');
const recordingText = document.getElementById('recordingText');
const recordingSpinner = document.getElementById('recordingSpinner');
const transcriptContainer = document.getElementById('transcriptContainer');
const transcriptText = document.getElementById('transcriptText');

recordButton.addEventListener('click', async () => {
    if (!recording) {
        try {
            // Request microphone access
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                // Create audio blob
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                audioChunks = [];

                // Create form data
                const formData = new FormData();
                formData.append('audio', audioBlob, 'recording.webm');

                // Show spinner while processing
                recordingSpinner.classList.remove('d-none');
                recordingText.textContent = 'Processing audio...';

                try {
                    // Send to server
                    const response = await fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();

                    if (result.ok) {
                        transcriptText.textContent = result.transcript;
                        transcriptContainer.style.display = 'block';
                        flashMessage('Transcription completed successfully!', 'success');
                    } else {
                        throw new Error('Transcription failed');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    flashMessage('Transcription failed. Please try again.', 'danger');
                } finally {
                    recordingSpinner.classList.add('d-none');
                    recordingText.textContent = 'Ready to record';
                }

                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            };

            // Start recording
            mediaRecorder.start();
            recording = true;
            recordButton.classList.add('recording');
            recordingText.textContent = 'Recording...';
            recordButton.innerHTML = '<i class="bi bi-stop-fill" style="font-size: 2rem;"></i>';
        } catch (err) {
            console.error('Error accessing microphone:', err);
            flashMessage('Microphone access denied. Please enable microphone permissions.', 'danger');
        }
    } else {
        // Stop recording
        mediaRecorder.stop();
        recording = false;
        recordButton.classList.remove('recording');
        recordButton.innerHTML = '<i class="bi bi-mic" style="font-size: 2rem;"></i>';
    }
});

function flashMessage(message, type) {
    // Create flash message
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    // Prepend to flash container
    document.querySelector('.container.mt-3').prepend(alert);
}
