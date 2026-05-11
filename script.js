document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('projectGrid');
    const searchInput = document.getElementById('searchInput');
    const categorySelect = document.getElementById('categorySelect');
    const loadMoreBtn = document.getElementById('loadMoreBtn');

    let displayedCount = 0;
    const ITEMS_PER_PAGE = 50;
    let filteredProjects = [...projectsData]; // from projects_data.js

    // Initialize Categories
    function initCategories() {
        const categories = new Set(projectsData.map(p => p.category));
        const sortedCategories = Array.from(categories).sort();
        
        sortedCategories.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            categorySelect.appendChild(option);
        });
    }

    // Render Cards
    function renderCards(append = false) {
        if (!append) {
            grid.innerHTML = '';
            displayedCount = 0;
        }

        const toDisplay = filteredProjects.slice(displayedCount, displayedCount + ITEMS_PER_PAGE);
        
        toDisplay.forEach(project => {
            const cardLink = document.createElement('a');
            cardLink.href = project.url;
            cardLink.target = '_blank';
            cardLink.className = 'card-link';
            cardLink.innerHTML = `
                <div class="project-card" data-tilt data-tilt-max="15" data-tilt-speed="400" data-tilt-glare="true" data-tilt-max-glare="0.2">
                    <div class="card-img-wrapper">
                        <!-- We use lazy loading for performance -->
                        <img src="${project.image}" alt="${project.name}" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div>
                            <h3 class="card-title">${project.name}</h3>
                            <span class="card-category">${project.category}</span>
                        </div>
                        <div class="card-footer">
                            View Project <span>→</span>
                        </div>
                    </div>
                </div>
            `;
            grid.appendChild(cardLink);
        });

        displayedCount += toDisplay.length;

        // Initialize VanillaTilt for new cards
        const newCards = grid.querySelectorAll('.project-card:not(.tilt-initialized)');
        if (typeof VanillaTilt !== 'undefined') {
            VanillaTilt.init(newCards);
            newCards.forEach(card => card.classList.add('tilt-initialized'));
        }

        // Mouse hover glow effect
        newCards.forEach(card => {
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });

        // Toggle Load More button
        if (displayedCount >= filteredProjects.length) {
            loadMoreBtn.classList.add('hidden');
        } else {
            loadMoreBtn.classList.remove('hidden');
        }
    }

    // Filter Logic
    function applyFilters() {
        const searchTerm = searchInput.value.toLowerCase();
        const category = categorySelect.value;

        filteredProjects = projectsData.filter(project => {
            const matchesSearch = project.name.toLowerCase().includes(searchTerm) || 
                                  project.category.toLowerCase().includes(searchTerm);
            const matchesCategory = category === 'All' || project.category === category;
            
            return matchesSearch && matchesCategory;
        });

        renderCards(false);
    }

    // Event Listeners
    searchInput.addEventListener('input', applyFilters);
    categorySelect.addEventListener('change', applyFilters);
    loadMoreBtn.addEventListener('click', () => renderCards(true));

    // Initial setup
    initCategories();
    renderCards();
});
