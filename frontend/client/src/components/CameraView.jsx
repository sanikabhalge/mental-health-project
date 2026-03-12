import React from "react";

const FLOATING_SIZE = { width: 280, height: 210 };

function CameraView({
  videoRef,
  cameraOn,
  mode = "floating",
  onModeToggle,
  position = { x: 24, y: 24 },
  onDragStart
}) {

  if (!cameraOn) return null;

  const isFloating = mode === "floating";

  /* ---------- Floating Camera ---------- */

  if (isFloating) {
    return (
      <div
        className="fixed z-50 flex flex-col rounded-xl overflow-hidden shadow-2xl border border-white/30 bg-gray-900"
        style={{
          width: FLOATING_SIZE.width,
          height: FLOATING_SIZE.height,
          left: position.x,
          top: position.y
        }}
      >

        {/* Header */}
        <div
          className="flex items-center justify-between px-2 py-1.5 bg-indigo-600 text-white text-sm cursor-grab active:cursor-grabbing select-none"
          onMouseDown={onDragStart}
        >
          <span className="font-medium">Camera</span>

          <button
            onClick={onModeToggle}
            className="p-1 rounded hover:bg-white/20"
          >
            ⛶
          </button>
        </div>

        {/* Video Preview */}
        <div className="flex-1 bg-black">

          <video
            ref={videoRef}
            autoPlay
            muted
            playsInline
            className="w-full h-full object-cover"
          />

        </div>

      </div>
    );
  }

  /* ---------- Full Screen Camera ---------- */

  return (
    <div className="flex-1 min-h-0 flex flex-col rounded-xl overflow-hidden bg-gray-900 shadow-inner">

      <div className="flex items-center justify-between px-3 py-2 bg-indigo-600 text-white text-sm">

        <span className="font-medium">Camera</span>

        <button
          onClick={onModeToggle}
          className="px-2 py-1 rounded-lg bg-white/20 hover:bg-white/30 text-xs font-medium"
        >
          Floating window
        </button>

      </div>

      <div className="flex-1 relative bg-black">

        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          className="absolute inset-0 w-full h-full object-contain"
        />

      </div>

    </div>
  );
}

export default CameraView;