import type { Template } from "../data/templates";

interface TemplateCardProps {
  template: Template;
  onInfo: (template: Template) => void;
}

const gradients: Record<string, string> = {
  "3D Websites": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  Portfolio: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
  Collections: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
  "Food & Restaurant": "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
  "Cafe & Bakery": "linear-gradient(135deg, #f6d365 0%, #fda085 100%)",
  "Salon & Beauty": "linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)",
  Barber: "linear-gradient(135deg, #2c3e50 0%, #3498db 100%)",
  "Medical & Hospital": "linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)",
  "Real Estate": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
  "Hotel & Travel": "linear-gradient(135deg, #f9d423 0%, #ff4e50 100%)",
  "Fitness & Gym": "linear-gradient(135deg, #f5576c 0%, #ff758c 100%)",
  Photography: "linear-gradient(135deg, #2c3e50 0%, #fd746c 100%)",
  Education: "linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)",
  Legal: "linear-gradient(135deg, #283048 0%, #859398 100%)",
  Accounting: "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)",
  Wedding: "linear-gradient(135deg, #fc5c7d 0%, #6a82fb 100%)",
  Agency: "linear-gradient(135deg, #667db6 0%, #0082c8 100%)",
  Automotive: "linear-gradient(135deg, #3e5151 0%, #dec236 100%)",
  Gaming: "linear-gradient(135deg, #0f0c29 0%, #302b63 100%)",
  "IT Services": "linear-gradient(135deg, #0f0c29 0%, #302b63 100%)",
  Marketing: "linear-gradient(135deg, #f12711 0%, #f5af19 100%)",
  Music: "linear-gradient(135deg, #1f1c2c 0%, #928dab 100%)",
  Startup: "linear-gradient(135deg, #00c6ff 0%, #0072ff 100%)",
  "Mobile Apps": "linear-gradient(135deg, #23074d 0%, #cc5333 100%)",
  "E-commerce": "linear-gradient(135deg, #ff5858 0%, #f09819 100%)",
  Fashion: "linear-gradient(135deg, #cc2b5e 0%, #753a88 100%)",
  Yoga: "linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%)",
  Construction: "linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)",
  Sports: "linear-gradient(135deg, #0c3483 0%, #a2b6df 100%)",
  "Church & Religious": "linear-gradient(135deg, #d38312 0%, #a83279 100%)",
  "Charity & Nonprofit": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
  Other: "linear-gradient(135deg, #757f9a 0%, #d7dde8 100%)",
};

const TemplateCard = ({ template, onInfo }: TemplateCardProps) => {
  const gradient = gradients[template.category] || gradients["Other"];
  const hasUrl = !!template.liveUrl;

  return (
    <div
      className="template-card"
      onClick={() => {
        if (hasUrl) window.open(template.liveUrl, "_blank", "noopener,noreferrer");
        else onInfo(template);
      }}
    >
      <div className="template-card-preview" style={{ background: gradient }}>
        {template.previewImage ? (
          <img src={template.previewImage} alt={template.title} className="template-card-img" loading="lazy" />
        ) : (
          <div className="template-card-preview-content">
            {template.isCollection ? (
              <div className="collection-badge-large">
                <span className="collection-count">{template.templateCount}</span>
                <span className="collection-label">Templates</span>
              </div>
            ) : (
              <div className="template-icon">{template.category.slice(0, 2).toUpperCase()}</div>
            )}
          </div>
        )}
        <div className="template-card-overlay">
          <span className="open-link-text">{hasUrl ? "🌐 Open Website" : "ℹ️ View Details"}</span>
        </div>
        {template.isCollection && (
          <div className="collection-overlay-badge"><span>Collection</span></div>
        )}
      </div>
      <div className="template-card-body">
        <div className="template-card-category">{template.category}</div>
        <h3 className="template-card-title">{template.title}</h3>
        <p className="template-card-desc">{template.description.slice(0, 90)}...</p>
        <div className="template-card-tech">
          {template.techStack.slice(0, 3).map((t) => (
            <span key={t} className="tech-badge">{t}</span>
          ))}
          {template.techStack.length > 3 && <span className="tech-badge tech-badge-more">+{template.techStack.length - 3}</span>}
        </div>
      </div>
    </div>
  );
};

export default TemplateCard;
