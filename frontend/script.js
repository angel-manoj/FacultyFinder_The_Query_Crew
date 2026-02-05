// No hardcoded localhost — use same domain as frontend
const RELEVANCE_THRESHOLD = 0.5;

let searchBtnText, searchSpinner;
let searchForm, searchInput, searchBtn;
let resultsGrid, errorContainer, errorMessage, noResults;
let heroSubtitle, navBrand;

document.addEventListener('DOMContentLoaded', () => {
  searchBtnText = document.getElementById('searchBtnText');
  searchSpinner = document.getElementById('searchSpinner');
  searchForm = document.getElementById('searchForm');
  searchInput = document.getElementById('searchInput');
  searchBtn = document.getElementById('searchBtn');
  resultsGrid = document.getElementById('resultsGrid');
  errorContainer = document.getElementById('errorContainer');
  errorMessage = document.getElementById('errorMessage');
  noResults = document.getElementById('noResults');
  heroSubtitle = document.getElementById('heroSubtitle');
  navBrand = document.getElementById('navBrand');

  document.getElementById('themeToggle').onclick = () => {
    document.body.classList.toggle('dark');
  };

  searchForm.addEventListener('submit', handleSearch);
  navBrand.addEventListener('click', resetSearch);
});

async function handleSearch(e) {
  e.preventDefault();

  const hero = document.getElementById('heroSection');
  hero.classList.add('hero-compact');
  hero.classList.remove('hero-center');

  const query = searchInput.value.trim();
  if (!query) return;

  heroSubtitle.classList.add('hidden');
  showSkeletons();

  try {
    searchBtn.disabled = true;
    searchBtnText.textContent = 'Searching...';
    searchSpinner.classList.remove('hidden');

    // ✅ Relative API call (works on Render + local)
    const res = await fetch(
      `/faculty/semantic-search?query_str=${encodeURIComponent(query)}`
    );

    if (!res.ok) throw new Error(`API Error: ${res.status}`);

    const data = await res.json();
    hideError();

    if (!data || data.length === 0) {
      showNoResults();
      return;
    }

    displayResults(data);

  } catch (err) {
    showError(err.message || 'Search failed');
  } finally {
    searchBtn.disabled = false;
    searchBtnText.textContent = 'Search';
    searchSpinner.classList.add('hidden');
  }
}

function showSkeletons() {
  resultsGrid.innerHTML = Array(3).fill(0).map(() => `
    <div class="card-hover animate-pulse">
      <div class="h-4 bg-slate-200 rounded w-1/3 mb-2"></div>
      <div class="h-3 bg-slate-200 rounded w-2/3 mb-2"></div>
      <div class="h-3 bg-slate-200 rounded w-full"></div>
    </div>
  `).join('');

  resultsGrid.classList.remove('hidden');
}

function displayResults(results) {
  resultsGrid.innerHTML = '';
  resultsGrid.classList.remove('hidden');
  noResults.classList.add('hidden');

  results.forEach(faculty => {
    resultsGrid.appendChild(createFacultyCard(faculty));
  });
}

function showNoResults() {
  resultsGrid.classList.add('hidden');
  noResults.classList.remove('hidden');
}

function createFacultyCard(faculty) {
  const card = document.createElement('div');
  card.className = 'card-hover p-6 flex flex-col';

  const showBadge = faculty.rerank_score >= RELEVANCE_THRESHOLD;

  card.innerHTML = `
    ${showBadge ? `
      <span class="badge tooltip mb-3">⭐ Most Relevant</span>
    ` : ''}

    <h3 class="text-lg font-bold mb-1">${faculty.name}</h3>
    <p class="text-sm text-gray-600 mb-2">${faculty.education || ''}</p>

    <p class="text-sm text-gray-500 break-all">
      📧 <a href="mailto:${faculty.email}" class="hover:text-indigo-600">
        ${faculty.email}
      </a>
    </p>

    <p class="text-sm text-gray-500 mt-1">
      📞 ${
        faculty.phone
          ? `<a href="tel:${faculty.phone}" class="hover:text-indigo-600">${faculty.phone}</a>`
          : 'Number not available'
      }
    </p>

    ${faculty.profile ? `
      <div class="mt-auto pt-4">
        <a href="${faculty.profile}" target="_blank" class="visit-btn">
          Visit Profile →
        </a>
      </div>
    ` : ''}
  `;

  return card;
}

function showError(msg) {
  errorMessage.textContent = msg;
  errorContainer.classList.remove('hidden');
}

function hideError() {
  errorContainer.classList.add('hidden');
}

function resetSearch() {
  document.getElementById('heroSection').classList.remove('hero-compact');
  document.getElementById('heroSection').classList.add('hero-center');

  searchInput.value = '';
  resultsGrid.classList.add('hidden');
  noResults.classList.add('hidden');
  hideError();
  heroSubtitle.classList.remove('hidden');
}
