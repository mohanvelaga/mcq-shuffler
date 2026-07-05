import { useState } from 'react';
import Header from './components/Header';
import UploadCard from './components/UploadCard';
import StatusCard from './components/StatusCard';
import UploadForm from './components/UploadForm';

export default function App() {
  const [file, setFile] = useState(null);
  const [uploadedFile, setUploadedFile] = useState('');
  const [outputFile, setOutputFile] = useState('');
  const [statusTitle, setStatusTitle] = useState('Ready');
  const [statusMessage, setStatusMessage] = useState('Choose a file to begin.');

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center p-4 sm:p-8">
      <div className="w-full max-w-3xl rounded-3xl bg-white p-6 shadow-2xl sm:p-8">
        <Header />
        <UploadCard
          file={file}
          onFileChange={(event) => {
            const selectedFile = event.target.files?.[0] || null;
            setFile(selectedFile);
            setStatusTitle('File selected');
            setStatusMessage(selectedFile ? `Selected ${selectedFile.name}` : 'Choose a file to begin.');
          }}
        />
        <div className="mt-6">
          <UploadForm
            file={file}
            uploadedFile={uploadedFile}
            outputFile={outputFile}
            onUploadSuccess={(filename, message) => {
              setUploadedFile(filename);
              setStatusTitle('Upload complete');
              setStatusMessage(message);
            }}
            onProcessSuccess={(filename, message) => {
              setOutputFile(filename);
              setStatusTitle('Process complete');
              setStatusMessage(message);
            }}
            onDownloadSuccess={(message) => {
              setStatusTitle('Download ready');
              setStatusMessage(message);
            }}
            onStatusChange={(title, message) => {
              setStatusTitle(title);
              setStatusMessage(message);
            }}
          />
        </div>
        <StatusCard
          title={statusTitle}
          message={statusMessage}
          selectedFile={file?.name || ''}
          uploadedFile={uploadedFile}
          outputFile={outputFile}
        />
      </div>
    </div>
  );
}