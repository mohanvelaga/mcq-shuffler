export default function ActionButtons() {
  return (
    <div className="mt-6 grid gap-3 sm:grid-cols-3">
      <button className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700">
        Upload
      </button>
      <button className="rounded-xl bg-green-600 px-4 py-3 font-semibold text-white transition hover:bg-green-700">
        Process
      </button>
      <button className="rounded-xl bg-purple-600 px-4 py-3 font-semibold text-white transition hover:bg-purple-700">
        Download
      </button>
    </div>
  );
}
