interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  totalCount: number;
  filteredCount: number;
}

const SearchBar = ({ value, onChange, totalCount, filteredCount }: SearchBarProps) => {
  return (
    <div className="search-bar">
      <div className="search-input-wrapper">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          className="search-input"
          placeholder="Search templates by name, category, or tech stack..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
        {value && (
          <button className="search-clear" onClick={() => onChange("")}>
            ✕
          </button>
        )}
      </div>
      <div className="search-stats">
        Showing <strong>{filteredCount}</strong> of <strong>{totalCount}</strong> templates
      </div>
    </div>
  );
};

export default SearchBar;
