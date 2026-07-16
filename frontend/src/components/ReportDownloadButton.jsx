import { useState } from "react";
import { downloadReportPdf } from "../api/reports";
import { toast } from "react-hot-toast";
import { FileText } from "lucide-react";

export default function ReportDownloadButton({ scanId, findings, score }) {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    if (!scanId) {
      toast.error("Please run a security scan first to generate a report.");
      return;
    }

    setDownloading(true);
    const toastId = toast.loading("Generating PDF Report...");

    try {
      const result = await downloadReportPdf(scanId, findings, score);
      if (result.success) {
        if (result.fallback) {
          toast.success("PDF Report downloaded (Client-side Fallback)", {
            id: toastId,
            duration: 4000,
          });
        } else {
          toast.success("PDF Report downloaded successfully!", {
            id: toastId,
            duration: 3000,
          });
        }
      }
    } catch (error) {
      console.error(error);
      toast.error("Failed to generate PDF report.", {
        id: toastId,
      });
    } finally {
      setDownloading(false);
    }
  };

  return (
    <button
      className="inline-flex items-center gap-2 rounded-lg border border-cyan-500/30 bg-cyan-500/10 px-4 py-2 text-sm font-semibold uppercase tracking-wide text-cyan-200 transition hover:bg-cyan-500/20 active:scale-95 disabled:cursor-not-allowed disabled:opacity-50"
      disabled={downloading || !scanId}
      onClick={handleDownload}
      type="button"
    >
      {downloading ? (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-cyan-200 border-t-transparent" />
      ) : (
        <FileText className="h-4 w-4" />
      )}
      <span>{downloading ? "Downloading..." : "Download PDF"}</span>
    </button>
  );
}
