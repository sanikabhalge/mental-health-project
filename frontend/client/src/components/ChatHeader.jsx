function ChatHeader({
  isRecordingAudio,
  isRecordingVideo,
  toggleAudioRecording,
  toggleVideoRecording,
  error
}) {

  const statusText =
    isRecordingAudio
      ? "🎤 Recording Audio"
      : isRecordingVideo
      ? "📷 Recording Video"
      : "Ready";

  return (
    <header className="overflow-hidden rounded-b-2xl shadow-lg">

      <div className="relative bg-gradient-to-r from-indigo-600 via-violet-600 to-fuchsia-600 px-6 py-4">

        <div className="relative flex flex-col gap-4">

          <div className="flex justify-between items-center">

            <h2 className="text-xl font-bold text-white tracking-tight">
              MindCare Chat
            </h2>

            <span className="text-sm font-medium text-white/90 bg-white/20 px-3 py-1.5 rounded-full">
              {statusText}
            </span>

          </div>

          {error && (
            <p className="text-sm text-amber-200 bg-amber-900/40 px-3 py-1 rounded-lg">
              {error}
            </p>
          )}

          <div className="flex flex-wrap items-center gap-4">

            <button
              onClick={toggleAudioRecording}
              className={`px-4 py-2 rounded-lg text-white font-medium flex items-center gap-2
              ${isRecordingAudio
                ? "bg-red-500 hover:bg-red-600"
                : "bg-emerald-500 hover:bg-emerald-600"}`}
            >
              {isRecordingAudio ? "⏹ Stop Audio" : "🎤 Record Audio"}
            </button>

            <button
              onClick={toggleVideoRecording}
              className={`px-4 py-2 rounded-lg text-white font-medium flex items-center gap-2
              ${isRecordingVideo
                ? "bg-red-500 hover:bg-red-600"
                : "bg-blue-500 hover:bg-blue-600"}`}
            >
              {isRecordingVideo ? "⏹ Stop Video" : "📷 Record Video"}
            </button>

          </div>

        </div>

      </div>

    </header>
  );
}

export default ChatHeader;