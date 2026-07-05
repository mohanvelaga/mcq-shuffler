export default function StatusCard({ title, message, selectedFile, uploadedFile, outputFile }) {
  return (
    <div className="mt-6 rounded-2xl bg-slate-50 p-5">
      <div className="flex items-center gap-2 text-green-600">
        <span className="text-xl">✓</span>
        <p className="font-semibold">{title}</p>
      </div>
      <p className="mt-2 text-sm text-slate-600">{message}</p>
      {selectedFile ? <p className="mt-1 text-sm text-slate-600">Selected file: {selectedFile}</p> : null}
      {uploadedFile ? <p className="mt-1 text-sm text-slate-600">Uploaded file: {uploadedFile}</p> : null}
      {outputFile ? <p className="mt-1 text-sm text-slate-600">Output: {outputFile}</p> : null}
    </div>
  );
}
