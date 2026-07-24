// ====================================================================
// PARCEL PAAS - MINIMAL FRONTEND LOGIC (PLAIN JAVASCRIPT)
// ====================================================================

// --------------------------------------------------------------------
// STEP 1: Find HTML elements on the page so JavaScript can update them
// --------------------------------------------------------------------
const loginSection = document.getElementById('login-section');
const loginButton = document.getElementById('login-button');
const loadingSection = document.getElementById('loading-section');
const dashboardSection = document.getElementById('dashboard-section');
const logoutButton = document.getElementById('logout-button');
const repoList = document.getElementById('repo-list');

// --------------------------------------------------------------------
// STEP 2: Login Button - When clicked, redirect user to GitHub login
// --------------------------------------------------------------------
loginButton.addEventListener('click', function () {
  // Redirect browser to backend endpoint which handles GitHub login
  window.location.href = '/api/auth/github/login';
});

// --------------------------------------------------------------------
// STEP 3: Logout Button - When clicked, reset page back to login
// --------------------------------------------------------------------
logoutButton.addEventListener('click', function () {
  dashboardSection.style.display = 'none';
  loginSection.style.display = 'block';
  repoList.innerHTML = '';
});

// --------------------------------------------------------------------
// STEP 4: Check if user just returned from GitHub login callback
// --------------------------------------------------------------------
// Read URL query parameters from browser address bar (e.g. ?code=123&state=abc)
const urlParams = new URLSearchParams(window.location.search);
const code = urlParams.get('code');
const state = urlParams.get('state');

// If 'code' and 'state' exist in URL, complete authentication with backend
if (code && state) {
  // Remove ?code=...&state=... from address bar so page URL stays clean
  window.history.replaceState({}, document.title, window.location.pathname);

  // Show loading section, hide login section
  loginSection.style.display = 'none';
  loadingSection.style.display = 'block';

  // Call backend to exchange code for list of repositories
  fetchRepositories(code, state);
}

// --------------------------------------------------------------------
// STEP 5: Function to call backend API and get repositories list
// --------------------------------------------------------------------
async function fetchRepositories(codeParam, stateParam) {
  try {
    // Send HTTP GET request to backend callback endpoint
    const response = await fetch(`/api/auth/github/callback?code=${codeParam}&state=${stateParam}`);
    
    if (!response.ok) {
      throw new Error(`Server returned status ${response.status}`);
    }

    // Convert server response into JavaScript object
    const data = await response.json();

    // Hide loading section and show dashboard section
    loadingSection.style.display = 'none';
    dashboardSection.style.display = 'block';

    // Render repository items into HTML
    renderRepositories(data.repositories || []);

  } catch (error) {
    loadingSection.style.display = 'none';
    loginSection.style.display = 'block';
    alert('Failed to load repositories: ' + error.message);
  }
}

// --------------------------------------------------------------------
// STEP 6: Function to render repositories list onto the screen
// --------------------------------------------------------------------
function renderRepositories(repositories) {
  // Clear any existing list items
  repoList.innerHTML = '';

  // Loop over each repository received from backend
  for (let i = 0; i < repositories.length; i++) {
    const repo = repositories[i];

    // Create a new <li> element
    const li = document.createElement('li');
    li.className = 'repo-item';

    // Set inside HTML content for repo info and Deploy button
    li.innerHTML = `
      <div>
        <h3 class="repo-name">${escapeHtml(repo.owner)} / ${escapeHtml(repo.name)}</h3>
        <div class="repo-branch">Branch: <code>${escapeHtml(repo.default_branch)}</code></div>
      </div>
      <button class="btn-deploy" id="deploy-btn-${repo.id}">Deploy</button>
    `;

    // Append <li> to the repository list container
    repoList.appendChild(li);

    // Attach click event to Deploy button
    const deployBtn = document.getElementById(`deploy-btn-${repo.id}`);
    deployBtn.addEventListener('click', function () {
      handleDeploy(deployBtn, repo.owner, repo.name, repo.default_branch);
    });
  }
}

// --------------------------------------------------------------------
// STEP 7: Placeholder function for Deploy button clicks
// --------------------------------------------------------------------
function handleDeploy(button, owner, repoName, branch) {
  // Update button text to show deployment started
  button.innerText = 'Deploying...';
  button.disabled = true;

  /* 
   * FUTURE BACKEND CALL:
   * fetch('/api/deploy', {
   *   method: 'POST',
   *   headers: { 'Content-Type': 'application/json' },
   *   body: JSON.stringify({ owner, repo: repoName, branch })
   * });
   */

  // Simulate deployment completion after 1.5 seconds
  setTimeout(function () {
    button.innerText = 'Active';
    button.className = 'btn-deploy active';
    button.disabled = false;
  }, 1500);
}

// Helper function to safely escape text before inserting into HTML
function escapeHtml(text) {
  const div = document.createElement('div');
  div.innerText = text;
  return div.innerHTML;
}
