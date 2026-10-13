// Mobile menu functionality
const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileSidebar = document.getElementById('mobile-sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');

mobileMenuButton.addEventListener('click', () => {
    updateDarkModeButtons();
    toggleSidebar();
});

function toggleSidebar() {
  mobileSidebar.classList.toggle('-translate-x-full');
  sidebarOverlay.classList.toggle('hidden');
}

sidebarOverlay.addEventListener('click', toggleSidebar);

//toggle dark mode
const toggleButton = document.getElementById('toggleDarkMode');
const btnActivateDark = document.getElementById('btnActivateDark');
const btnActivateLight = document.getElementById('btnActivateLight');
const darkModeIcon = document.getElementById('darkModeIcon');

toggleButton.addEventListener('click', () => {
  const isDarkMode = document.documentElement.classList.contains('dark');

  if (isDarkMode) {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
    darkModeIcon.innerHTML = sun;
    updateDarkModeButtons();
    updateChartColors(myChart);
  } else {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
    darkModeIcon.innerHTML = moon;
    updateDarkModeButtons();
    updateChartColors(myChart);
  }
});

btnActivateLight.addEventListener('click', () => {
  document.documentElement.classList.remove('dark');
  localStorage.setItem('theme', 'light');
  updateDarkModeButtons();
  updateChartColors(myChart);
});

btnActivateDark.addEventListener('click', () => {
  document.documentElement.classList.add('dark');
  localStorage.setItem('theme', 'dark');
  updateDarkModeButtons();
  updateChartColors(myChart);
});

const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
  document.documentElement.classList.add('dark');
  darkModeIcon.innerHTML = moon;
} else {
  document.documentElement.classList.remove('dark');
  darkModeIcon.innerHTML = sun;
}