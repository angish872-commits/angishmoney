import { useState, useMemo } from "react";
import { templates, allCategories, type Template } from "./data/templates";
import TemplateGrid from "./components/TemplateGrid";
import CategoryFilter from "./components/CategoryFilter";
import SearchBar from "./components/SearchBar";
import PreviewModal from "./components/PreviewModal";
import "./App.css";

function App() {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [infoTemplate, setInfoTemplate] = useState<Template | null>(null);

  const filteredTemplates = useMemo(() => {
    return templates.filter((t) => {
      const catMatch = selectedCategory === "All" || t.category === selectedCategory;
      const searchMatch = !searchQuery ||
        t.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.techStack.some((s) => s.toLowerCase().includes(searchQuery.toLowerCase()));
      return catMatch && searchMatch;
    });
  }, [selectedCategory, searchQuery]);

  const stats = useMemo(() => {
    const cols = templates.filter((t) => t.isCollection);
    return {
      collections: cols.length,
      totalSub: cols.reduce((s, c) => s + (c.templateCount || 0), 0),
    };
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1><span className="header-emoji">🎨</span> Template Showcase</h1>
          <p className="header-subtitle">Click any template card to open the live website — 36 templates with live demos ready</p>
          <div className="header-stats">
            <div className="stat-card"><span className="stat-number">{templates.length}</span><span className="stat-label">Template Groups</span></div>
            <div className="stat-card"><span className="stat-number">{stats.collections}</span><span className="stat-label">Collections</span></div>
            <div className="stat-card"><span className="stat-number">{stats.totalSub}+</span><span className="stat-label">Total Templates</span></div>
            <div className="stat-card"><span className="stat-number">{allCategories.length - 1}</span><span className="stat-label">Categories</span></div>
          </div>
        </div>
      </header>
      <main className="app-main">
        <SearchBar value={searchQuery} onChange={setSearchQuery} totalCount={templates.length} filteredCount={filteredTemplates.length} />
        <CategoryFilter selected={selectedCategory} onSelect={setSelectedCategory} />
        <div className="app-results">
          <div className="results-header"><h2>{selectedCategory === "All" ? "All Templates" : selectedCategory} <span className="results-count">({filteredTemplates.length})</span></h2></div>
          <TemplateGrid templates={filteredTemplates} onInfo={setInfoTemplate} />
        </div>
      </main>
      <footer className="app-footer">
        <p>Template Showcase &copy; {new Date().getFullYear()} — <strong>{templates.length}</strong> groups, <strong>{stats.totalSub}+</strong> total templates</p>
      </footer>
      <PreviewModal template={infoTemplate} onClose={() => setInfoTemplate(null)} />
    </div>
  );
}

export default App;
