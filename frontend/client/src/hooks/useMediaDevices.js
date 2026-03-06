import { useState, useRef, useEffect, useCallback } from "react";

export function useMediaDevices() {
  const [micOn, setMicOn] = useState(false);
  const [cameraOn, setCameraOn] = useState(false);
  const [speakerOn, setSpeakerOn] = useState(true);
  const [error, setError] = useState(null);

  const micStreamRef = useRef(null);
  const cameraStreamRef = useRef(null);
  const audioContextRef = useRef(null);
  const gainNodeRef = useRef(null);
  const [, setStreamsTick] = useState(0);

  const toggleMic = useCallback(() => {
    setError(null);
    setMicOn((prev) => !prev);
  }, []);

  const toggleCamera = useCallback(() => {
    setError(null);
    setCameraOn((prev) => !prev);
  }, []);

  const toggleSpeaker = useCallback(() => {
    setSpeakerOn((prev) => !prev);
  }, []);

  const recorderRef = useRef(null);

  useEffect(() => {
    if (!micOn) {
      if (recorderRef.current) {
        recorderRef.current.stop();
        recorderRef.current = null;
      }
      return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
      micStreamRef.current = stream;

      const recorder = new MediaRecorder(stream);
      recorderRef.current = recorder;

      recorder.ondataavailable = async (event) => {
        const blob = event.data;

        const formData = new FormData();
        formData.append("audio", blob);

        await fetch("http://localhost:8000/api/emotion/audio", {
          method: "POST",
          body: formData
        });
      };

      recorder.start(3000); // send audio every 3 seconds
    });

  }, [micOn]);

  const videoRef = useRef(null);

  useEffect(() => {
    if (!cameraOn) return;

    const interval = setInterval(() => {
      const video = videoRef.current;
      if (!video) return;

      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);

      canvas.toBlob(async (blob) => {
        const formData = new FormData();
        formData.append("image", blob);

        await fetch("http://localhost:8000/api/emotion/video", {
          method: "POST",
          body: formData
        });
      });

    }, 4000); // every 4 seconds

    return () => clearInterval(interval);

  }, [cameraOn]);

  useEffect(() => {
    if (gainNodeRef.current) {
      gainNodeRef.current.gain.value = speakerOn ? 1 : 0;
    }
  }, [speakerOn]);

  const initSpeakerContext = useCallback(() => {
    if (!audioContextRef.current) {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const gain = ctx.createGain();
      gain.gain.value = speakerOn ? 1 : 0;
      gain.connect(ctx.destination);
      audioContextRef.current = ctx;
      gainNodeRef.current = gain;
    }
    if (gainNodeRef.current) gainNodeRef.current.gain.value = speakerOn ? 1 : 0;
    return audioContextRef.current;
  }, [speakerOn]);

  return {
    micOn,
    cameraOn,
    speakerOn,
    toggleMic,
    toggleCamera,
    toggleSpeaker,
    getMicStream: () => micStreamRef.current,
    getCameraStream: () => cameraStreamRef.current,
    getSpeakerGainNode: () => gainNodeRef.current,
    initSpeakerContext,
    error,
  };
}
