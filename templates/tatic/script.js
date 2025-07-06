let mediaRecorder;
let audioChunks = [];

async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.start();

  mediaRecorder.addEventListener("dataavailable", event => {
    audioChunks.push(event.data);
  });

  setInterval(() => {
    if (audioChunks.length) {
      const blob = new Blob(audioChunks, { type: 'audio/webm' });
      sendAudio(blob);
      audioChunks = [];
    }
  }, 10000); // co 10 sekund
}

async function sendAudio(blob) {
  const formData = new FormData();
  formData.append("audio", blob, "audio.webm");

  const response = await fetch("/transcribe", {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  document.getElementById("questions").innerText = data.questions;
  document.getElementById("coaching").innerText = data.coaching;
  document.getElementById("transcript").innerText = data.transcript;
}

window.onload = () => {
  startRecording();
};
