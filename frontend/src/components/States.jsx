export function Loading({ label = "Loading..." }) {
  return (
    <div className="state state-loading">
      <div className="spinner" />
      <p>{label}</p>
    </div>
  );
}

export function ErrorState({ message = "Unable to load data.", onRetry }) {
  return (
    <div className="state state-error">
      <p>{message}</p>
      {onRetry && (
        <button className="btn btn-secondary" onClick={onRetry}>
          Retry
        </button>
      )}
    </div>
  );
}

export function EmptyState({ message = "Nothing here yet." }) {
  return (
    <div className="state state-empty">
      <p>{message}</p>
    </div>
  );
}

export function NotAvailable({ endpoint, note }) {
  return (
    <div className="state state-unavailable">
      <p>This section isn't available yet.</p>
      <p className="state-sub">
        The backend doesn't currently expose <code>{endpoint}</code>.
        {note ? ` ${note}` : ""}
      </p>
    </div>
  );
}
