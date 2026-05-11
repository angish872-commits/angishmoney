import type { Template } from "../data/templates";
import TemplateCard from "./TemplateCard";

interface TemplateGridProps {
  templates: Template[];
  onInfo: (template: Template) => void;
}

const TemplateGrid = ({ templates, onInfo }: TemplateGridProps) => {
  if (templates.length === 0) {
    return (
      <div className="no-results">
        <div className="no-results-icon">🔍</div>
        <h3>No templates found</h3>
        <p>Try a different search or filter category</p>
      </div>
    );
  }

  return (
    <div className="template-grid">
      {templates.map((template) => (
        <TemplateCard key={template.id} template={template} onInfo={onInfo} />
      ))}
    </div>
  );
};

export default TemplateGrid;
