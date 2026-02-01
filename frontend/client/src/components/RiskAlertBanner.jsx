function RiskAlertBanner({ onDismiss }) {
  return (
    <div
      className="bg-red-600 text-white px-4 py-3 rounded-lg shadow-lg flex flex-col gap-2"
      role="alert"
    >
      <div className="flex items-start justify-between gap-2">
        <div>
          <p className="font-semibold">We’re here for you</p>
          <p className="text-sm text-red-100 mt-0.5">
            If you’re in crisis, please reach out to someone now. You’re not alone.
          </p>
        </div>
        {onDismiss && (
          <button
            type="button"
            onClick={onDismiss}
            className="text-white/90 hover:text-white p-1 rounded"
            aria-label="Dismiss"
          >
            ✕
          </button>
        )}
      </div>
      <div className="text-sm border-t border-red-500/50 pt-2 mt-1">
        <p className="font-medium mb-1">Helplines:</p>
        <ul className="space-y-0.5 text-red-100">
          <li><strong>India:</strong> 91-22-27546669 (Aasra)</li>
          <li><strong>USA:</strong> 1-800-273-8255 (NSPL)</li>
          <li><strong>International:</strong> <a href="https://findahelpline.com" className="underline" target="_blank" rel="noopener noreferrer">findahelpline.com</a></li>
        </ul>
      </div>
    </div>
  );
}

export default RiskAlertBanner;
