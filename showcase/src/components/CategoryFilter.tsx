import { allCategories } from "../data/templates";

interface CategoryFilterProps {
  selected: string;
  onSelect: (category: string) => void;
}

const CategoryFilter = ({ selected, onSelect }: CategoryFilterProps) => {
  return (
    <div className="category-filter">
      <div className="category-filter-scroll">
        {allCategories.map((category) => (
          <button
            key={category}
            className={`category-btn ${selected === category ? "category-btn-active" : ""}`}
            onClick={() => onSelect(category)}
          >
            {category}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CategoryFilter;
