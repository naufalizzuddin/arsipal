document.addEventListener("DOMContentLoaded", function () {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('a[data-path]');

  navLinks.forEach(link => {
    const path = link.getAttribute('data-path');
    if (currentPath.includes(path)) {
      link.classList.remove("after:duration-300", "after:scale-x-0", "after:scale-x-95");
      link.classList.add("scale-x-100");
    }
  });
});

document.getElementById("profile-button").addEventListener("click", function(event) {
  const dropdownMenu = document.getElementById("dropdown-menu");
  dropdownMenu.classList.toggle("hidden");
});

document.addEventListener("click", function(event) {
  const dropdownMenu = document.getElementById("dropdown-menu");
  const profileButton = document.getElementById("profile-button");

  if (!dropdownMenu.contains(event.target) && !profileButton.contains(event.target)) {
    dropdownMenu.classList.add("hidden");
  }
});

function updateButtonText(element) {
  const button = document.getElementById("dropdown-button");
  button.textContent = element.getAttribute("value") + " >";
  toggleDropdown();
}

document.getElementById('logout-btn').addEventListener('click', function(event) {
  event.preventDefault();
  const isDarkMode = (localStorage.getItem('theme') === 'dark');

  Swal.fire({
    title: 'Apakah anda yakin?',
    text: 'Anda akan logout dari sesi ini.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Ya',
    cancelButtonText: 'Tidak',
    confirmButtonColor: '#243FED',
    cancelButtonColor: '#FF0000',
    reverseButtons: true,
    background: isDarkMode ? "#344C64" : "#fff",
    color: isDarkMode ? "#fff" : "#000"
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = this.href;
    }
  });
});
