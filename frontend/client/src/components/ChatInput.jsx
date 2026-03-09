import { useState, useRef, useEffect, useContext } from "react";
import { MediaDevicesContext } from "../context/MediaDevicesContext";

function ChatInput({ onSend }) {
  const [text, setText] = useState("");
  const [isRecordingAudio, setIsRecordingAudio] = useState(false);
  const [isRecordingVideo, setIsRecordingVideo] = useState(false);
  const [recordedAudio, setRecordedAudio] = useState(null);
  const [recordedVideo, setRecordedVideo] = useState(null);
  
  const mediaDevices = useContext(MediaDevicesContext);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const videoChunksRef = useRef([]);
  const streamRef = useRef(null);

  // -------- Audio Recording --------
  const startAudioRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        setRecordedAudio(audioBlob);
        
        // Stop audio stream
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecordingAudio(true);
    } catch (error) {
      console.error("Error starting audio recording:", error);
      alert("Unable to access microphone. Please check permissions.");
    }
  };

  const stopAudioRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecordingAudio(false);
    }
  };

  // -------- Video Recording --------
  const startVideoRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        video: true, 
        audio: true 
      });
      streamRef.current = stream;
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      videoChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        videoChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const videoBlob = new Blob(videoChunksRef.current, { type: "video/webm" });
        setRecordedVideo(videoBlob);
        
        // Stop video stream
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start();
      setIsRecordingVideo(true);
    } catch (error) {
      console.error("Error starting video recording:", error);
      alert("Unable to access camera. Please check permissions.");
    }
  };

  const stopVideoRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecordingVideo(false);
    }
  };

  // -------- Send Message --------
  const handleSend = async () => {
    if (!text.trim() && !recordedAudio && !recordedVideo) {
      alert("Please enter text or record audio/video");
      return;
    }

    // Call onSend with all data together
    onSend({
      text: text.trim() || null,
      audio_blob: recordedAudio || null,
      video_blob: recordedVideo || null,
    });

    setText("");
    setRecordedAudio(null);
    setRecordedVideo(null);
  };

  const clearRecordings = () => {
    setRecordedAudio(null);
    setRecordedVideo(null);
  };

  return (
    <div className="flex flex-col gap-3 p-4 bg-white/95 backdrop-blur border-t border-gray-200/80 shadow-inner">
      {/* Display recorded status */}
      {(recordedAudio || recordedVideo) && (
        <div className="flex items-center gap-2 px-3 py-2 bg-green-50 border border-green-200 rounded-lg text-sm">
          {recordedAudio && <span>🎤 Audio recorded</span>}
          {recordedVideo && <span>📹 Video recorded</span>}
          <button
            onClick={clearRecordings}
            className="ml-auto text-xs px-2 py-1 bg-red-200 hover:bg-red-300 rounded"
          >
            Clear
          </button>
        </div>
      )}

      {/* Text Input */}
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
        placeholder="Type a message or use audio/video..."
        className="flex-1 p-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent bg-gray-50/80"
      />

      {/* Controls */}
      <div className="flex gap-2 flex-wrap items-center">
        {/* Audio Recording Button */}
        <button
          type="button"
          onClick={isRecordingAudio ? stopAudioRecording : startAudioRecording}
          className={`px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-all ${
            isRecordingAudio
              ? "bg-red-500 hover:bg-red-600 text-white"
              : "bg-blue-100 hover:bg-blue-200 text-blue-700"
          }`}
        >
          {isRecordingAudio ? "⏹ Stop Audio" : "🎤 Record Audio"}
        </button>

        {/* Video Recording Button */}
        <button
          type="button"
          onClick={isRecordingVideo ? stopVideoRecording : startVideoRecording}
          className={`px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-all ${
            isRecordingVideo
              ? "bg-red-500 hover:bg-red-600 text-white"
              : "bg-purple-100 hover:bg-purple-200 text-purple-700"
          }`}
        >
          {isRecordingVideo ? "⏹ Stop Video" : "📹 Record Video"}
        </button>

        {/* Send Button */}
        <button
          type="button"
          onClick={handleSend}
          className="px-6 py-2 rounded-lg bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-medium hover:from-indigo-700 hover:to-violet-700 shadow-md hover:shadow transition-all ml-auto"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatInput;
