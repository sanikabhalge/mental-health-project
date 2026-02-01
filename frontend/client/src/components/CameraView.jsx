import { useRef, useEffect } from "react";

const FLOATING_SIZE = { width: 280, height: 210 };

function CameraView({
  stream,
  mode,
  onModeToggle,
  position,
  onDragStart,
  onDragMove,
  onDragEnd,
  isDragging,
}) {
  const videoRef = useRef(null);

  useEffect(() => {
    if (!videoRef.current || !stream) return;
    videoRef.current.srcObject = stream;
    return () => {
      if (videoRef.current) videoRef.current.srcObject = null;
    };
  }, [stream]);

  if (!stream) return null;

  const isFloating = mode === "floating";

  if (isFloating) {
    return (
      <div
        className="fixed z-50 flex flex-col rounded-xl overflow-hidden shadow-2xl border-2 border-white/30 bg-gray-900"
        style={{
          width: FLOATING_SIZE.width,
          height: FLOATING_SIZE.height,
          left: position.x,
          top: position.y,
        }}
      >
        <div
          className="flex items-center justify-between px-2 py-1.5 bg-indigo-600 text-white text-sm cursor-grab active:cursor-grabbing select-none"
          onMouseDown={onDragStart}
          onTouchStart={(e) => {
            const t = e.touches[0];
            onDragStart({ clientX: t.clientX, clientY: t.clientY });
          }}
        >
          <span className="font-medium">Camera</span>
          <div className="flex gap-1">
            <button
              type="button"
              onClick={onModeToggle}
              className="p-1 rounded hover:bg-white/20"
              title="Expand to full size"
              aria-label="Expand to full size"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v5a1 1 0 001 1h2a1 1 0 001-1v-5a1 1 0 00-1-1h-2z" />
              </svg>
            </button>
          </div>
        </div>
        <div className="flex-1 min-h-0 relative bg-black">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-full object-cover"
          />
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 min-h-0 flex flex-col rounded-xl overflow-hidden bg-gray-900 shadow-inner">
      <div className="flex items-center justify-between px-3 py-2 bg-indigo-600 text-white text-sm">
        <span className="font-medium">Camera (full size)</span>
        <button
          type="button"
          onClick={onModeToggle}
          className="px-2 py-1 rounded-lg bg-white/20 hover:bg-white/30 text-xs font-medium"
          title="Minimize to floating window"
        >
          Floating window
        </button>
      </div>
      <div className="flex-1 min-h-0 relative">
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="absolute inset-0 w-full h-full object-contain"
        />
      </div>
    </div>
  );
}

export default CameraView;
