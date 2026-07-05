import UploadForm from '../components/UploadForm';

function HomePage() {
  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>MCQ Shuffler</h1>
      <p>Upload a question file and prepare it for shuffling.</p>
      <UploadForm />
    </main>
  );
}

export default HomePage;
