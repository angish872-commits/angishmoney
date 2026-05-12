document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('projectGrid');
    const searchInput = document.getElementById('searchInput');
    const categorySelect = document.getElementById('categorySelect');
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    const scrollTopBtn = document.getElementById('scrollTopBtn');

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
        
        toDisplay.forEach((project, index) => {
            const cardLink = document.createElement('a');
            cardLink.href = project.url;
            cardLink.target = '_blank';
            cardLink.className = 'card-link';
            cardLink.style.setProperty('--delay', index);
            cardLink.innerHTML = `
                <div class="project-card" data-tilt data-tilt-max="15" data-tilt-speed="400" data-tilt-glare="true" data-tilt-max-glare="0.2">
                    <div class="card-img-wrapper">
                        <img src="${project.image}" alt="${project.name}" loading="lazy" onerror="this.style.display='none';this.parentElement.classList.add('img-failed')">
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

        // Initialize VanillaTilt for new cards (skip on mobile)
        const isMobile = window.innerWidth < 768;
        const newCards = grid.querySelectorAll('.project-card:not(.tilt-initialized)');
        if (typeof VanillaTilt !== 'undefined' && !isMobile) {
            VanillaTilt.init(newCards);
            newCards.forEach(card => card.classList.add('tilt-initialized'));
        } else if (isMobile) {
            newCards.forEach(card => {
                card.removeAttribute('data-tilt');
                card.classList.add('tilt-initialized');
            });
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

        // Observe new cards for scroll animation
        observeCards(toDisplay.length);

        // Toggle Load More button
        if (displayedCount >= filteredProjects.length) {
            loadMoreBtn.classList.add('hidden');
        } else {
            loadMoreBtn.classList.remove('hidden');
        }
    }

    // Intersection Observer for card scroll animations
    let cardObserver = null;
    function observeCards() {
        if (!cardObserver) {
            cardObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        cardObserver.unobserve(entry.target);
                    }
                });
            }, { rootMargin: '0px 0px -100px 0px' });
        }
        document.querySelectorAll('.card-link:not(.observed)').forEach(el => {
            el.classList.add('observed');
            cardObserver.observe(el);
        });
    }

    // Animated counter for stats
    function animateCounters() {
        const counters = document.querySelectorAll('.stat-number');
        const statsSection = document.getElementById('statsBar');
        if (!counters.length || !statsSection) return;

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    counters.forEach(counter => {
                        const target = parseInt(counter.dataset.target);
                        const duration = 2000;
                        const start = performance.now();

                        function update(currentTime) {
                            const elapsed = currentTime - start;
                            const progress = Math.min(elapsed / duration, 1);
                            const eased = 1 - Math.pow(1 - progress, 3);
                            counter.textContent = Math.floor(eased * target);
                            if (progress < 1) {
                                requestAnimationFrame(update);
                            } else {
                                counter.textContent = target + '+';
                            }
                        }
                        requestAnimationFrame(update);
                    });
                    counterObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counterObserver.observe(statsSection);
    }

    // Scroll to top button visibility
    function initScrollToTop() {
        if (!scrollTopBtn) return;
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        });
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
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
        // Smooth scroll to top of grid on filter
        grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Event Listeners
    searchInput.addEventListener('input', applyFilters);
    categorySelect.addEventListener('change', applyFilters);
    loadMoreBtn.addEventListener('click', () => renderCards(true));

    // Initial setup
    initCategories();
    renderCards();
    animateCounters();
    initScrollToTop();
});
