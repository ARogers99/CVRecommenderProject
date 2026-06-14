import { CheckCircle2, FileText, Loader2, Upload } from "lucide-react"

function CvUploader({ cvData, file, onSelectCv, status }) {
  return (
    <section className="panel-section" aria-labelledby="cv-upload-title">
      <div className="section-title">
        <FileText aria-hidden="true" />
        <h2 id="cv-upload-title">CV</h2>
      </div>

      <label className="file-drop">
        <input
          accept="application/pdf"
          disabled={status === "uploading"}
          type="file"
          onChange={(event) => {
            const selected = event.target.files?.[0] || null
            onSelectCv(selected)
            event.target.value = ""
          }}
        />
        {status === "uploading" ? (
          <Loader2 className="spin" aria-hidden="true" />
        ) : (
          <Upload aria-hidden="true" />
        )}
        <strong>{status === "uploading" ? "Uploading CV" : file?.name || "Select PDF"}</strong>
        <span>{file ? `${Math.max(1, Math.round(file.size / 1024))} KB` : "PDF only"}</span>
      </label>

      {cvData?.raw_text ? (
        <div className="cv-ready" role="status">
          <CheckCircle2 aria-hidden="true" />
          <span>{cvData.raw_text.length.toLocaleString()} characters parsed</span>
        </div>
      ) : null}
    </section>
  )
}

export default CvUploader
