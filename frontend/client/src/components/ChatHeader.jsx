import { useContext } from "react";
import { MediaDevicesContext } from "../context/MediaDevicesContext";

function ChatHeader() {
  const media = useContext(MediaDevicesContext);
  const {
    micOn,
    cameraOn,
    speakerOn,
    toggleMic,
    toggleCamera,
    toggleSpeaker,
    error,
  } = media ?? {};

  const activeDevices = [
    micOn && "Mic",
    cameraOn && "Camera",
    speakerOn && "Speaker",
  ].filter(Boolean);

  const statusText = activeDevices.length > 0
    ? `${activeDevices.join(" • ")} on`
    : "All devices off";

  return (
    <header className="overflow-hidden rounded-b-2xl shadow-lg">
      {/* Attractive gradient strip */}
      <div className="relative bg-gradient-to-r from-indigo-600 via-violet-600 to-fuchsia-600 px-6 py-4">
        {/* Subtle pattern overlay */}
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='1' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 20V40H20L40 20z'/%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />
        <div className="relative flex flex-col gap-4">
          {/* Title row */}
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold text-white tracking-tight drop-shadow-sm">
              MindCare Chat
            </h2>
            <span className="text-sm font-medium text-white/90 bg-white/20 backdrop-blur-sm px-3 py-1.5 rounded-full">
              {statusText}
            </span>
          </div>
          {error && (
            <p className="text-sm text-amber-200 bg-amber-900/40 px-3 py-1 rounded-lg" role="alert">
              {error}
            </p>
          )}

          {/* Toggle switches row */}
          <div className="flex flex-wrap items-center gap-6">
            {/* Mic toggle */}
            <div className="flex items-center gap-2">
              <span className="text-white/95 text-sm font-medium flex items-center gap-1.5">
                <span className="text-lg" aria-hidden>🎤</span>
                Mic
              </span>
              <button
                type="button"
                role="switch"
                aria-checked={micOn}
                aria-label={`Microphone ${micOn ? "on" : "off"}`}
                onClick={toggleMic}
                className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-transparent ${
                  micOn ? "bg-emerald-400" : "bg-white/30"
                }`}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    micOn ? "translate-x-5" : "translate-x-0.5"
                  }`}
                />
              </button>
            </div>

            {/* Camera toggle */}
            <div className="flex items-center gap-2">
              <span className="text-white/95 text-sm font-medium flex items-center gap-1.5">
                <span className="text-lg" aria-hidden>📷</span>
                Camera
              </span>
              <button
                type="button"
                role="switch"
                aria-checked={cameraOn}
                aria-label={`Camera ${cameraOn ? "on" : "off"}`}
                onClick={toggleCamera}
                className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-transparent ${
                  cameraOn ? "bg-emerald-400" : "bg-white/30"
                }`}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    cameraOn ? "translate-x-5" : "translate-x-0.5"
                  }`}
                />
              </button>
            </div>

            {/* Speaker toggle */}
            <div className="flex items-center gap-2">
              <span className="text-white/95 text-sm font-medium flex items-center gap-1.5">
                <span className="text-lg" aria-hidden>🔊</span>
                Speaker
              </span>
              <button
                type="button"
                role="switch"
                aria-checked={speakerOn}
                aria-label={`Speaker ${speakerOn ? "on" : "off"}`}
                onClick={toggleSpeaker}
                className={`relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-transparent ${
                  speakerOn ? "bg-emerald-400" : "bg-white/30"
                }`}
              >
                <span
                  className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${
                    speakerOn ? "translate-x-5" : "translate-x-0.5"
                  }`}
                />
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

export default ChatHeader;
