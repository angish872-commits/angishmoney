import type { Template } from "../data/templates";

interface PreviewModalProps {
  template: Template | null;
  onClose: () => void;
}

const colors: Record<string, string> = {
  Collections: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
  "Food & Restaurant": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
  "Medical & Hospital": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)",
  "Real Estate": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
};
const def = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)";

const PreviewModal = ({ template, onClose }: PreviewModalProps) => {
  if (!template) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>
        <div className="modal-header" style={{ background: colors[template.category] || def }}>
          <div className="modal-header-text">
            <span className="modal-category">{template.category}</span>
            {template.isCollection && <span className="modal-collection-badge">Collection</span>}
            <h2>{template.title}</h2>
          </div>
        </div>
        <div className="modal-body">
          <p className="modal-description">{template.description}</p>
          <div className="modal-details">
            <div className="modal-section">
              <h4>Tech Stack</h4>
              <div className="modal-tech-list">
                {template.techStack.map((t) => (
                  <span key={t} className="tech-badge tech-badge-lg">{t}</span>
                ))}
              </div>
            </div>
            {template.isCollection && template.templateCount && (
              <div className="modal-section">
                <h4>Collection</h4>
                <p><strong>{template.templateCount}</strong> sub-templates</p>
              </div>
            )}
          </div>
          <div className="modal-actions">
            <button className="btn btn-secondary" onClick={onClose}>Close</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PreviewModal;
