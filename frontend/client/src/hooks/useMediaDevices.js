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

  useEffect(() => {
    if (!micOn) {
      if (micStreamRef.current) {
        micStreamRef.current.getTracks().forEach((t) => t.stop());
        micStreamRef.current = null;
        setStreamsTick((n) => n + 1);
      }
      return;
    }
    let cancelled = false;
    setError(null);
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        if (cancelled) {
          stream.getTracks().forEach((t) => t.stop());
          return;
        }
        micStreamRef.current = stream;
        setStreamsTick((n) => n + 1);
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message || "Microphone access denied");
          setMicOn(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [micOn]);

  useEffect(() => {
    if (!cameraOn) {
      if (cameraStreamRef.current) {
        cameraStreamRef.current.getTracks().forEach((t) => t.stop());
        cameraStreamRef.current = null;
        setStreamsTick((n) => n + 1);
      }
      return;
    }
    let cancelled = false;
    setError(null);
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        if (cancelled) {
          stream.getTracks().forEach((t) => t.stop());
          return;
        }
        cameraStreamRef.current = stream;
        setStreamsTick((n) => n + 1);
      })
      .catch((err) => {
        if (!cancelled) {
          setError(err.message || "Camera access denied");
          setCameraOn(false);
        }
      });
    return () => {
      cancelled = true;
    };
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
