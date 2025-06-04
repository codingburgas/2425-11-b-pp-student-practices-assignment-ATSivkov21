document.addEventListener("DOMContentLoaded", () => {
  console.log("Ad Predictor JS loaded.");

  // Example: highlight active nav link
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === path) {
      link.classList.add('active');
    }
  });
});
