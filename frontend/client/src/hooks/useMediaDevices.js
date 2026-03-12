import { useState, useRef } from "react";

export function useMediaDevices({ onEmotionDetected, onBotReply } = {}) {

  const [isRecordingAudio, setIsRecordingAudio] = useState(false);
  const [isRecordingVideo, setIsRecordingVideo] = useState(false);
  const [error, setError] = useState(null);

  const audioRecorderRef = useRef(null);
  const videoRecorderRef = useRef(null);

  const audioStreamRef = useRef(null);
  const videoStreamRef = useRef(null);

  const audioChunksRef = useRef([]);
  const videoChunksRef = useRef([]);

  const videoRef = useRef(null);

  /* ================= AUDIO ================= */

  const toggleAudioRecording = async () => {

    try {

      if (!isRecordingAudio) {

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        audioStreamRef.current = stream;

        const recorder = new MediaRecorder(stream);
        audioRecorderRef.current = recorder;

        audioChunksRef.current = [];

        recorder.ondataavailable = (e) => {
          if (e.data.size > 0) {
            audioChunksRef.current.push(e.data);
          }
        };

        recorder.onstop = async () => {

          const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });

          const formData = new FormData();
          formData.append("audio", blob, "audio.webm");

          try {

            const token = localStorage.getItem("mindcare_token");

            const res = await fetch("http://localhost:8000/api/chat/audio", {
              method: "POST",
              headers: {
                Authorization: `Bearer ${token}`
              },
              body: formData
            });

            const data = await res.json();

            if (onBotReply) {
              onBotReply(data);
            }

            if (onEmotionDetected && data?.emotion) {
              onEmotionDetected(data);
            }

          } catch (err) {
            console.error("Audio upload failed", err);
          }

          if (audioStreamRef.current) {
            audioStreamRef.current.getTracks().forEach(t => t.stop());
            audioStreamRef.current = null;
          }

        };

        recorder.start();
        setIsRecordingAudio(true);

      } else {

        audioRecorderRef.current.stop();
        setIsRecordingAudio(false);

      }

    } catch (err) {
      setError(err.message);
    }

  };

  /* ================= VIDEO ================= */

  const toggleVideoRecording = async () => {

    try {

      if (!isRecordingVideo) {

        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true
        });

        videoStreamRef.current = stream;

        /* attach stream to video element */

        setTimeout(() => {
  if (videoRef.current) {
    videoRef.current.srcObject = stream;
  }
}, 100);

        const recorder = new MediaRecorder(stream);
        videoRecorderRef.current = recorder;

        videoChunksRef.current = [];

        recorder.ondataavailable = (e) => {
          if (e.data.size > 0) {
            videoChunksRef.current.push(e.data);
          }
        };

        recorder.onstop = async () => {

          const blob = new Blob(videoChunksRef.current, {
            type: "video/webm"
          });

          const formData = new FormData();
          formData.append("video", blob, "video.webm");

          try {

            const token = localStorage.getItem("mindcare_token");

            const res = await fetch("http://localhost:8000/api/chat/video", {
              method: "POST",
              headers: {
                Authorization: `Bearer ${token}`
              },
              body: formData
            });

            const data = await res.json();

            if (onBotReply) {
              onBotReply(data);
            }

            if (onEmotionDetected && data?.emotion) {
              onEmotionDetected(data);
            }

          } catch (err) {
            console.error("Video upload failed", err);
          }

          /* stop camera */

          if (videoStreamRef.current) {
            videoStreamRef.current.getTracks().forEach(t => t.stop());
            videoStreamRef.current = null;
          }

        };

        recorder.start();
        setIsRecordingVideo(true);

      } else {

        videoRecorderRef.current.stop();
        setIsRecordingVideo(false);

      }

    } catch (err) {
      setError(err.message);
    }

  };

  /* ================= RETURN ================= */

  return {

    isRecordingAudio,
    isRecordingVideo,

    toggleAudioRecording,
    toggleVideoRecording,

    videoRef,
    error

  };

}