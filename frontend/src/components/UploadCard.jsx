import { UploadCloud } from 'lucide-react';

export default function UploadCard({ file, onFileChange }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-slate-50 p-6 shadow-sm">
      <div className="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center">
        <UploadCloud className="mb-3 h-10 w-10 text-blue-600" />
        <p className="text-lg font-semibold text-slate-800">Drag & drop your DOCX or PDF here</p>
        <p className="mt-2 text-sm text-slate-500">or browse files from your device</p>
        <label className="mt-5 cursor-pointer rounded-xl bg-blue-600 px-5 py-3 font-medium text-white transition hover:bg-blue-700">
          {file ? file.name : 'Choose File'}
          <input type="file" className="hidden" accept=".docx,.pdf" onChange={onFileChange} />
        </label>
      </div>
    </div>
  );
}
