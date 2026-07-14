import { useState } from "react";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

export default function Layout({ children, backendStatus }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Sidebar for Desktop & Mobile */}
      <Sidebar isOpen={mobileMenuOpen} onClose={() => setMobileMenuOpen(false)} />

      {/* Main content wrapper */}
      <div className="md:ml-56 flex flex-col min-h-screen">
        <Navbar 
          backendStatus={backendStatus} 
          onMenuToggle={() => setMobileMenuOpen(!mobileMenuOpen)} 
        />
        <main className="flex-grow px-4 py-6 md:px-8 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
